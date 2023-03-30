from django.shortcuts import render
from django.views.generic import TemplateView
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
import time

username = settings.LOGIN
password1 = settings.PASSWORD
driver = webdriver.Chrome()

class IndexPageView(TemplateView):
    template_name = "index.html"


def authorization():


def update_leads(request, *args):
    interval = 5
    driver = webdriver.Chrome()

    driver.get("https://mp24.bitrix24.ru/marketplace/app/10/")

    # Ввод логина
    username_field = driver.find_element(By.ID, "login")
    username_field.send_keys(username)

    # Нажимаем кнопку "войти"
    login_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
    login_button.click()

    # # Ожидаем загрузку страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, "password")))

    time.sleep(2)

    # Вводим пароль
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password1)

    # Нажимаем кнопку "войти"
    password_button = driver.find_element(By.CLASS_NAME, "b24-network-auth-form-btn")
    password_button.click()

    time.sleep(10)
    # Ожидаем загрузку страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "b24-statistic-table-head-btn-inner")))

    # Вводим в фильтр Bitrix24
    filter_bitrix = driver.find_element(By.XPATH,
    "//div[@class='partner-application-b24-statistic-table-head-btn-inner'][contains(text(), 'Битрикс24')]")

    filter_bitrix.click()

    time.sleep(6)

    # Ожидаем загрузку страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "main-ui-item-icon.main-ui-search")))

    while True:
        # Запускаем фильтр обновления заявок
        search_leads = driver.find_element(By.CLASS_NAME,
                                           "main-ui-item-icon.main-ui-search")
        search_leads.click()

        # Ожидаем период времени
        time.sleep(interval)

    driver.close()
















































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
