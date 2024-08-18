from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def wait_for_element(driver, by, value, timeout=10):
    for _ in range(timeout):
        try:
            element = driver.find_element(by, value)
            return element
        except:
            driver.refresh()
            time.sleep(1)
    raise Exception(f"Element not found: {by}={value}")


def open_login_page(driver):
    # Открытие страницы входа
    driver.get("http://users.bugred.ru/user/login/index.html")
    wait_for_element(driver, By.NAME, "login")


def login(driver, email, password):
    # Авторизация
    open_login_page(driver)
    driver.find_element(By.NAME, "login").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Авторизоваться']").click()


def create_user(driver):
    driver.find_element(By.LINK_TEXT, "Добавить пользователя").click()
    driver.find_element(By.NAME, "noibiz_name").send_keys("Test User")
    driver.find_element(By.NAME, "noibiz_email").send_keys("testuser@example.com")
    driver.find_element(By.NAME, "noibiz_password").send_keys("password")
    driver.find_element(By.NAME, "noibiz_birthday").send_keys("01011990")
    driver.find_element(By.NAME, "act_create").click()


def test_create_and_verify_user():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        # Шаг 1: Вход под менеджером
        login(driver, "manager@mail.ru", "1")
        # Шаг 2: Создание нового пользователя
        create_user(driver)
        # Шаг 3: Логин новым пользователем
        login(driver, "testuser@example.com", "password")
        # Шаг 4: Поиск пользователя и проверка данных
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Test User")
        search_box.send_keys(Keys.RETURN)
        driver.find_element(By.LINK_TEXT, "Посмотреть").click()
        # Сравнение введенных данных с отображаемыми
        fio_value = driver.find_element(By.XPATH, "//tr[td[1]='ФИО']/td[2]").text
        assert fio_value == "Test User", f"Expected 'Test User', but got '{fio_value}'"
        # Шаг 5: Удаление пользователя
        login(driver, "manager@mail.ru", "1")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Test User")
        search_box.send_keys(Keys.RETURN)
        driver.find_element(By.LINK_TEXT, "Удалить").click()
    finally:
        driver.quit()


#if name == "main":
#    test_create_and_verify_user()

if __name__ == "__main__":
    test_create_and_verify_user()
