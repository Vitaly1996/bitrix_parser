from django.shortcuts import render
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
from django.shortcuts import redirect
import time
import random
import json

username = settings.LOGIN
password1 = settings.PASSWORD
url = "https://mp24.bitrix24.ru/marketplace/app/10/"


class IndexPageView(TemplateView):
    template_name = "index.html"


def update_settings(request):
    # Загрузка данных из файла
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'interval_start': None, 'interval_end': None, 'stop_word': None}

    if request.method == 'POST':
        # Обновление данных из формы
        data['interval_start'] = request.POST.get('interval-start')
        data['interval_end'] = request.POST.get('interval-end')
        data['stop_word'] = request.POST.get('stop-word')

        # Сохранение данных в файл
        with open('settings.json', 'w') as f:
            json.dump(data, f)

    # Заполнение формы значениями из файла
    form_data = {'interval-start': data['interval_start'],
                 'interval-end': data['interval_end'],
                 'stop-word': data['stop_word']}

    return redirect(request, 'index', {'form_data': form_data})


def update_leads(request, *args):
    if request.method == 'POST':
        interval_start = request.POST.get('interval-start')
        interval_end = request.POST.get('interval-end')
        stop_word = request.POST.get('stop-word')

    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(1)
        # Ввод логина
        username_field = driver.find_element(By.ID, "login")
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(3)
        # Нажимаем кнопку "войти"
        login_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
        login_button.click()
        time.sleep(2)
        #
        # # # Ожидаем загрузку страницы
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        #     (By.ID, "password")))
        #
        #
        #
        # Вводим пароль
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password1)
        time.sleep(2)
        # Нажимаем кнопку "войти"
        password_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
        password_button.click()
        time.sleep(20)

        # Вводим в фильтр Bitrix24
        iframe = driver.find_element(By.CSS_SELECTOR,
                                     'iframe[name="partner_application"]' )


        driver.switch_to.frame(iframe)

        time.sleep(20)

        filter_bitrix = driver.find_element(By.XPATH,
                                            "//div[contains(@class,'b24-statistic-table-head-btn')]")
        for element in filter_bitrix:
            if "Битрикс24" in element.text:
                element.click()
                break
        time.sleep(10)
        #
        # filter_and_search = driver.find_element(By.ID, "b24_partner_application_filter_search")
        # filter_and_search.click()
        #
        # choice_item = driver.find_element(By.CLASS_NAME, 'main-ui-control main-ui-select')
        # choice_item.click()
        #
        # bitrix_button = driver.find_element(By.XPATH,
        #                                     "//div[@data-value='{\"NAME\":\"Битрикс24\",\"VALUE\":\"B24\"}']")
        # bitrix_button.click()
        #
        # # Ожидаем загрузку страницы
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        #     (By.CLASS_NAME, "main-ui-item-icon.main-ui-search")))
        #
        # while True:
        #     # Запускаем фильтр обновления заявок
        #     search_leads = driver.find_element(By.CLASS_NAME,
        #                                        "main-ui-item-icon.main-ui-search")
        # interval = random.randint(interval_start, interval_end)
        #     search_leads.click()
        #
        #     # Ожидаем период времени
        #     time.sleep(interval)

    except Exception as ex:
        print(ex)

    finally:

        driver.close()
        driver.quit()
    return redirect('index')
















































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
