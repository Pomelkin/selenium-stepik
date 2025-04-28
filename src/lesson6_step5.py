import math

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


LOGIN = ""
PASSWORD = ""

LESSON_LINKS = [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1",
]


@pytest.fixture(scope="function")
def browser():
    print("\nЗапуск Firefox браузера для теста...")
    # Настройка Firefox опций
    firefox_options = Options()
    # firefox_options.add_argument("--headless")  # раскомментируйте для запуска в фоновом режиме
    firefox_options.profile = webdriver.FirefoxProfile(
        "/home/pomelk1n/.mozilla/firefox/0i9o7iyc.default-release-1/"
    )
    # Инициализация Firefox браузера
    service = Service()  # укажите путь к geckodriver, если он не в PATH
    firefox_browser = webdriver.Firefox(service=service, options=firefox_options)

    firefox_browser.implicitly_wait(10)
    firefox_browser.maximize_window()

    yield firefox_browser

    print("\nЗакрытие браузера...")
    firefox_browser.quit()


def login(browser):
    login_button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navbar__auth_login"))
    )
    login_button.click()

    WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.NAME, "login"))
    ).send_keys(LOGIN)
    browser.find_element(By.NAME, "password").send_keys(PASSWORD)

    browser.find_element(By.CSS_SELECTOR, "button.sign-form__btn").click()

    WebDriverWait(browser, 15).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.sign-form"))
    )


@pytest.mark.parametrize("link", LESSON_LINKS)
def test_stepik_answer_feedback(browser, link):
    browser.get(link)
    login(browser)

    textarea = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
    )
    assert textarea.get_attribute("value") == "", (
        "Поле ввода должно быть пустым перед вводом"
    )

    answer = str(math.log(int(time.time())))
    textarea.send_keys(answer)

    browser.find_element(By.CLASS_NAME, "submit-submission").click()

    feedback = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".smart-hints__hint"))
    )

    feedback_text = feedback.text
    assert feedback_text == "Correct!", (
        f"Фидбек не совпадает с 'Correct!': {feedback_text}"
    )
