import json
import logging
import random
import time
import threading
import pymorphy2

from bs4 import BeautifulSoup
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

username = settings.LOGIN
password = settings.PASSWORD

url = "https://mp24.bitrix24.ru/marketplace/app/10/?any=10%2F&current_fieldset=SOCSERV"
# executable_path =r"C:\A_programming\Dev\workshop\bitrix_parser\chromedriver.exe"


class IndexPageView(TemplateView):
    template_name = "index.html"


def update_settings(request):
    # Загрузка данных из файла
    try:
        with open('settings.json',  'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'interval_start': None,
                'interval_end': None,
                'stop_word': None}

    if request.method == 'POST':
        # Обновление данных из формы
        data['interval_start'] = request.POST.get('interval-start')
        data['interval_end'] = request.POST.get('interval-end')
        data['stop_word'] = request.POST.get('stop-word')

        # Сохранение данных в файл
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

    # Заполнение формы значениями из файла
    form_data = {'interval_start': data['interval_start'],
                 'interval_end': data['interval_end'],
                 'stop_word': data['stop_word']}

    return form_data


def analyze_new_leads(driver, stop_words):
    morph = pymorphy2.MorphAnalyzer()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lead = soup.find('tr', {'class': 'main-grid-row main-grid-row-body'})
    if not lead:
        return 'No leads found.'
    lead_text = lead.find('span', {
        'class': 'partner-application-b24-list-description-inner js-description-inner'}).text.lower()
    for word in lead_text.split():
        parsed_word = morph.parse(word)[0]
        if parsed_word.normal_form in stop_words:
            return True
    return False


def update_leads(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_settings':
            form_data = update_settings(request)
            return render(request, 'index.html', {'form_data': form_data})
        interval_start = int(request.POST.get('interval-start'))
        interval_end = int(request.POST.get('interval-end'))
        stop_word = request.POST.get('stop-word')
        stop_word_list = [word.strip() for word in stop_word.split('\r\n') if word.strip()]

    # options
    options = webdriver.FirefoxOptions()

    # user-agent
    options.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

    # disable webdriver mode
    options.set_preference("dom.webdriver.enabled", False)

    driver = webdriver.Firefox(
        executable_path=
    r'C:\A_programming\Dev\workshop\bitrix_parser\geckodriver.exe',
    options=options)

    try:
        actions = ActionChains(driver)
        driver.get(url)
        time.sleep(1)

        # Ввод логина
        username_field = driver.find_element(By.ID, "login")
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(3)

        login_button = driver.find_element(By.CLASS_NAME,
                                           "b24-network-auth-form-btn")
        login_button.click()
        time.sleep(2)
        logging.info('Введен логин пользователем: %s', request.user.email)


        # Ввод пароля
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        time.sleep(2)

        password_button = driver.find_element(By.CLASS_NAME,
                                              "b24-network-auth-form-btn")
        password_button.click()
        time.sleep(10)
        logging.info('Введен пароль пользователем: %s', request.user.email)


        #Нажатие на кнопку фильтр

        element = driver.find_element(By.CLASS_NAME, 'app-frame')
        driver.switch_to.frame(element)

        iframe = driver.find_element(By.CLASS_NAME, 'partner-application-install-select-country-iframe')
        driver.switch_to.frame(iframe)

        filter = driver.find_element(By.CLASS_NAME,
                                     'partner-application-b24-item-b24')
        filter.click()

        btn = driver.find_element(By.ID, 'b24_partner_application_filter_search')
        btn.send_keys('Битрикс24')
        time.sleep(2)

        # btn = driver.find_element(By.CLASS_NAME, 'main-ui-select-name')
        # btn.click()
        # time.sleep(2)
        #
        # btn_b24 = driver.find_element(By.CLASS_NAME, "main-ui-checked")
        # btn_b24.click()
        # time.sleep(2)

        # search = driver.find_element(By.CLASS_NAME, "ui-btn ui-btn-primary ui-btn-icon-search main-ui-filter-field-button main-ui-filter-find")
        # search.click()

        logging.info('Кнопка нажата')

        # filter = driver.find_element(By.XPATH,
        #             "//span[@class='main-ui-item-icon main-ui-search']")
        # # ActionChains(driver).move_to_element(filter).perform()
        # # driver.implicitly_wait(10)
        # filter.click()

        def background_thread():
            while True:
                analyze_new_leads(driver, stop_word_list)
                time.sleep(60)

        threading.Thread(target=background_thread, daemon=True).start()

        while True:
            # Запускаем обновления заявок с периодничность указанной
            # указанной в переменной интервал
            # bt24 = driver.find_element(By.CLASS_NAME,
            # "b24-statistic-table-head-btn-selected")
            # bt24.click()
            interval = random.randint(interval_start, interval_end)
            search_leads = driver.find_element(By.CLASS_NAME, "main-ui-search")
            search_leads.click()
            logging.info('Заявки обновлены')

            time.sleep(interval)

    except Exception as ex:
        print(ex)

    finally:

        driver.close()
        driver.quit()
    return redirect('index')


def logs(request):
    with open('output.log', 'r') as log_file:
        log_content = log_file.read()
    return render(request, 'logs.html', {'log_content': log_content})


def analyze_lead_text(driver, stop_word):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lead_text = soup.find('span', {'class':
    'partner-application-b24-list-description-inner js-description-inner'}).text.lower()
    if stop_word not in lead_text:
        return True # Взять в работу
    else:
        return False # Не брать заявку в работу











































    # #Ввод логина и пароля
    # username_field = driver.find_element(By.ID, "login")
    # username_field.send_keys(username)
    #
    # login_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
    # login_button.click()
    #
    # # Нажимаем кнопку войти
    # password_field = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "password"))
    # )
    # # password_field = driver.find_element(By.ID, "password")
    # password_field.send_keys(password1)
    #
    #
    # # Нажимаем кнопку войти
    # password_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
    # password_button.click()
    #
    # # Вводим в фильтр Bitrix24
    # filter_bitrix = driver.find_element(By.CLASS_NAME,
    # "b24-statistic-table-head-btn-inner")
    # filter_bitrix.click()
    #
    # #Запускаем фильтр обновления заявок
    # while True:
    #
    #     search_leads = driver.find_element(By.CLASS_NAME,
    #                                        "main-ui-item-icon main-ui-search")
    #     search_leads.click()
    #     #Ожидаем заданный интервал времени
    #     time.sleep(interval)
    #
    #
    # driver.close()
