from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    #avatar_input = driver.find_element(By.NAME, "noibiz_avatar")
    #avatar_input.send_keys("D:/124142142.PNG")
    wait = WebDriverWait(driver, 10)    
    gender_select_element = wait.until(EC.visibility_of_element_located((By.NAME, "noibiz_gender")))
    gender_select = Select(gender_select_element)
    gender_select.select_by_visible_text("Женский")

    driver.find_element(By.NAME, "noibiz_date_start").send_keys("01012020")
    driver.find_element(By.NAME, "noibiz_hobby").send_keys("Волейбол")
    driver.find_element(By.NAME, "noibiz_name1").send_keys("Пользюк")
    driver.find_element(By.NAME, "noibiz_surname1").send_keys("Юзеров")
    wait = WebDriverWait(driver, 10)
    visible_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.form-control.numberfilter")))
    visible_input.send_keys("Юзерович")
    driver.find_element(By.NAME, "noibiz_cat").send_keys("да")
    driver.find_element(By.NAME, "noibiz_dog").send_keys("да")
    driver.find_element(By.NAME, "noibiz_parrot").send_keys("да")
    driver.find_element(By.NAME, "noibiz_cavy").send_keys("нет")
    driver.find_element(By.NAME, "noibiz_hamster").send_keys("нет")
    driver.find_element(By.NAME, "noibiz_squirrel").send_keys("нет")
    driver.find_element(By.NAME, "noibiz_phone").send_keys("89999998811")
    driver.find_element(By.NAME, "noibiz_adres").send_keys("Московский скворечник, д2")
    driver.find_element(By.NAME, "noibiz_inn").send_keys("872193842")
    driver.find_element(By.NAME, "act_create").click()


def test_create_and_verify_user():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        driver.execute_script("document.charset = 'UTF-8';")
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
        wait = WebDriverWait(driver, 20)

        fio_value = driver.find_element(By.XPATH, "//tr[td[1]='ФИО']/td[2]").text
        assert fio_value == "Test User", f"Expected 'Test User', but got '{fio_value}'"

        email_value = driver.find_element(By.XPATH, "//tr[td[1]='Email']/td[2]").text
        assert email_value == "testuser@example.com", f"Expected 'testuser@example.com', but got '{email_value}'"

        birthday_value = driver.find_element(By.XPATH, "//tr[td[1]='Дата рождения']/td[2]").text
        assert birthday_value == "1990-01-01", f"Expected '1990-01-01', but got '{birthday_value}'"
        
        gender_value = driver.execute_script("""
            var element = document.evaluate("//tr[td[1]='Пол']/td[2]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            return element ? element.innerText : '';
        """).strip()
        gender_value_cleaned = ' '.join(gender_value.split()).replace('\n', '').replace('  ', ' ')
        assert 'Женский' in gender_value_cleaned, f"Expected 'Женский', but got '{gender_value_cleaned}'"

        date_start_value = driver.find_element(By.XPATH, "//tr[td[text()='Начал работать в компании']]/td[2]").text
        assert date_start_value == "2020-01-01", f"Expected '2020-01-01', but got '{date_start_value}'"
        
        hobby_value = driver.find_element(By.XPATH, "//tr[td[text()='Хобби']]/td/textarea[@name='hobby']").text
        assert hobby_value == "Волейбол", f"Expected 'Волейбол', but got '{hobby_value}'"
        
        name1_value = driver.find_element(By.XPATH, "//tr[td[text()='имя1']]/td[2]").text
        assert name1_value == "Пользюк", f"Expected 'Пользюк', but got '{name1_value}'"
        
        surname1_value = driver.find_element(By.XPATH, "//tr[td[text()='фамилия1']]/td[2]").text
        assert surname1_value == "Юзеров", f"Expected 'Юзеров', but got '{surname1_value}'"
        
        patronymic_value = driver.find_element(By.XPATH, "//tr[td[text()='отчество1']]/td[2]").text
        assert patronymic_value == "Юзерович", f"Expected 'Юзерович', but got '{patronymic_value}'"
        
        cat_value = driver.find_element(By.XPATH, "//tr[td[text()='Кошечка']]/td[2]").text
        assert cat_value == "да", f"Expected 'да', but got '{cat_value}'"
        
        dog_value = driver.find_element(By.XPATH, "//tr[td[text()='Собачка']]/td[2]").text
        assert dog_value == "да", f"Expected 'да', but got '{dog_value}'"
        
        parrot_value = driver.find_element(By.XPATH, "//tr[td[text()='Попугайчик']]/td[2]").text
        assert parrot_value == "да", f"Expected 'да', but got '{parrot_value}'"
        
        cavy_value = driver.find_element(By.XPATH, "//tr[td[text()='Морская свинка']]/td[2]").text
        assert cavy_value == "нет", f"Expected 'нет', but got '{cavy_value}'"
        
        hamster_value = driver.find_element(By.XPATH, "//tr[td[text()='Хомячок']]/td[2]").text
        assert hamster_value == "нет", f"Expected 'нет', but got '{hamster_value}'"
        
        squirrel_value = driver.find_element(By.XPATH, "//tr[td[text()='Белочка']]/td[2]").text
        assert squirrel_value == "нет", f"Expected 'нет', but got '{squirrel_value}'"
        
        phone_value = driver.find_element(By.XPATH, "//tr[td[text()='Телефон']]/td[2]").text
        assert phone_value == "89999998811", f"Expected '89999998811', but got '{phone_value}'"
        
        address_value = driver.find_element(By.XPATH, "//tr[td[text()='Адрес']]/td[2]").text
        assert address_value == "Московский скворечник, д2", f"Expected 'Московский скворечник, д2', but got '{address_value}'"
        
        inn_value = driver.find_element(By.XPATH, "//tr[td[text()='ИНН']]/td[2]").text
        assert inn_value == "872193842", f"Expected '872193842', but got '{inn_value}'"

        # Шаг 5: Удаление пользователя
        login(driver, "manager@mail.ru", "1")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Test User")
        search_box.send_keys(Keys.RETURN)
        driver.find_element(By.LINK_TEXT, "Удалить").click()
    finally:
        driver.quit()


if __name__ == "__main__":
    test_create_and_verify_user()
