import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Запуск  python -m unittest .\lesson2_step13.py

def test(link):
    try:
        browser = webdriver.Chrome()
        browser.get(link)

        first_name = browser.find_element(By.XPATH, "//div[@class='first_block']/div[1]/input")
        first_name.send_keys("Ivan")

        last_name = browser.find_element(By.XPATH, "//div[@class='first_block']/div[2]/input")
        last_name.send_keys("Ivanov")

        email = browser.find_element(By.XPATH, "//div[@class='first_block']/div[3]/input")
        email.send_keys("Ivanov@ivan.com")

        button = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-default")
        button.click()

        time.sleep(1)

        welcome_text_elt = browser.find_element(By.TAG_NAME, "h1")
        welcome_text = welcome_text_elt.text

        return welcome_text

    finally:
        time.sleep(4)
        browser.quit()

class Test(unittest.TestCase):

    def test_registration1(self):
        self.assertEqual(test("http://suninjuly.github.io/registration1.html"), "Congratulations! You have successfully registered!")

    def test_registration2(self):
        self.assertEqual(test("http://suninjuly.github.io/registration2.html"), "Congratulations! You have successfully registered!")


if __name__ == "__main__":
    unittest.main()
