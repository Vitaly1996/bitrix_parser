from django.shortcuts import render
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from django.conf import settings
from django.shortcuts import redirect
import time
import random
import json
import logging
import os
import sys

username = settings.LOGIN
password = settings.PASSWORD

url = "https://mp24.bitrix24.ru/marketplace/app/10/"
executable_path =r"C:\A_programming\Dev\workshop\bitrix_parser\chromedriver.exe"


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

    return render(request, 'index.html', {'form_data': form_data})


def update_leads(request, *args):
    if request.method == 'POST':
        interval_start = request.POST.get('interval-start')
        interval_end = request.POST.get('interval-end')
        stop_word = request.POST.get('stop-word')

    driver = webdriver.Chrome(executable_path=executable_path)
    try:
        driver.get(url)
        time.sleep(1)


        # Ввод логина
        username_field = driver.find_element(By.ID, "login")
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(3)

        login_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
        login_button.click()
        time.sleep(2)
        logging.info('Введен логин пользователем: %s', request.user.email)


        # Вводим пароль
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        time.sleep(2)

        password_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
        password_button.click()
        time.sleep(25)
        logging.info('Введен пароль пользователем: %s', request.user.email)

        #когда зашли на главную страницу

        table = driver.find_element(By.ID, "workarea")

        div2 = driver.find_element(By.ID, "workarea-content")

        div3 = driver.find_element(By.CLASS_NAME, "workarea-content-paddings")

        ActionChains(driver).move_to_element(div3).perform()
        driver.implicitly_wait(10)
        div3.click()

        filer = driver.find_element(By.CLASS_NAME, "main-ui-filter-search")
        ActionChains(driver).move_to_element(filer).perform()
        driver.implicitly_wait(10)
        filer.click()

        while True:
            # Запускаем фильтр обновления заявок
            search_leads = driver.find_element(By.CLASS_NAME,
                                               "main-ui-item-icon.main-ui-search")
            interval = random.randint(interval_start, interval_end)
            search_leads.click()

            # Ожидаем период времени
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
