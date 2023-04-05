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
from selenium.webdriver.common.by import By

from leads.config import url, executable_path, user_agent


class IndexPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_data = update_settings(self.request)
        context[
            'form_data'] = form_data  # добавляем словарь в контекст шаблона
        return context


def update_settings(request):
    # Загрузка данных из файла
    try:
        with open('settings.json',  'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'interval_start': None,
                'interval_end': None,
                'stop_word': ''}

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


def analyze_new_leads(driver, stop_words, analyzed_leads):
    morph = pymorphy2.MorphAnalyzer()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    lead = soup.find('tr', {'class': 'main-grid-row main-grid-row-body'})
    if not lead:
        return 'No leads found.'

    lead_id = lead.get('data-id')
    if lead_id in analyzed_leads:
        # Заявка уже анализирована, пропускаем ее
        return False

    lead_text = lead.find('span', {
        'class': 'partner-application-b24-list-description-inner js-description-inner'}).text.lower()
    for word in lead_text.split():
        parsed_word = morph.parse(word)[0]
        if parsed_word.normal_form in stop_words:
            logging.info('Заявка содержит стоп-сллово и не может быть взята в работу')

    take_lead_button = lead.find('span', {
        'class': 'js-partner-submit-application'})
    if take_lead_button:
        driver.execute_script("arguments[0].click();", take_lead_button)
        logging.info('Заявка взята в работу')

    logging.info('Данную заявку нельзя взять в работу')

    # Добавляем заявку в список анализированных заявок
    analyzed_leads[lead_id] = True

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
    options.set_preference("general.useragent.override", user_agent)


    # disable webdriver mode
    options.set_preference("dom.webdriver.enabled", False)

    driver = webdriver.Firefox(executable_path=executable_path,
                               options=options)

    try:

        driver.get(url)
        time.sleep(1)

        # Ввод логина
        username_field = driver.find_element(By.ID, "login")
        username_field.clear()
        username_field.send_keys(settings.LOGIN)
        time.sleep(3)

        login_button = driver.find_element(By.CLASS_NAME,
                                           "b24-network-auth-form-btn")
        login_button.click()
        time.sleep(2)
        logging.info('Введен логин пользователем: %s', request.user.email)


        # Ввод пароля
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(settings.PASSWORD)
        time.sleep(2)
        password_button = driver.find_element(By.CLASS_NAME,
                                              "b24-network-auth-form-btn")
        password_button.click()
        time.sleep(10)
        logging.info('Введен пароль пользователем: %s', request.user.email)


        #Переключаемя по фреймам и нажимаем на кнопку "Битрикс24"
        #для установления фильтра

        element = driver.find_element(By.CLASS_NAME, 'app-frame')
        driver.switch_to.frame(element)

        iframe = driver.find_element(By.CLASS_NAME,
                        'partner-application-install-select-country-iframe')
        driver.switch_to.frame(iframe)

        filter = driver.find_element(By.CLASS_NAME,
                                     'partner-application-b24-item-b24')
        filter.click()
        time.sleep(2)
        logging.info('Кнопка фильтра нажата')

        def background_thread():
            while True:
                analyze_new_leads(driver, stop_word_list, analyzed_leads)
                time.sleep(interval)

        analyzed_leads = {}
        threading.Thread(target=background_thread, daemon=True).start()

        #Запускаем нажатие на кнопку обновления заявок с рандомным числом
        #из заданного интервала
        while True:
            interval = random.randint(interval_start,
                                      interval_end)
            search_leads = driver.find_element(By.CLASS_NAME, "main-ui-search")
            search_leads.click()
            logging.info('Заявки обновлены')

            time.sleep(interval)

    except Exception as ex:
        print(ex)

    finally:

        driver.close()
        driver.quit()
        context = update_settings(request)
    return render(request, 'index.html', context=context)


def logs(request):
    with open('output.log', 'r') as log_file:
        log_content = log_file.read()
    return render(request, 'logs.html', {'log_content': log_content})
