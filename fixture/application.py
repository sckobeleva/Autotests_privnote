from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pyperclip


class Application:

    def __init__(self, browser, url):
        if browser == "firefox":
            self.driver = webdriver.Firefox()
        elif browser == "chrome":
            self.driver = webdriver.Chrome()
        elif browser == "ie":
            self.driver = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.url = url
        self.driver.implicitly_wait(5)

    def copy_note_text(self):
        driver = self.driver
        driver.find_element_by_css_selector("#select_text").click()
        driver.find_element_by_css_selector("#note_contents").send_keys(Keys.CONTROL, 'c')


    def create_note(self, inputtext):
        driver = self.driver
        driver.find_element_by_css_selector("#note_raw").send_keys(inputtext)
        driver.find_element_by_css_selector("#encrypt_note").click()

    def create_note_with_scrolling(self, inputtext):
        driver = self.driver
        driver.find_element_by_css_selector("#note_raw").send_keys(inputtext)
        button = driver.find_element_by_css_selector("#encrypt_note")
        driver.execute_script("return arguments[0].scrollIntoView(true);", button)
        button.click()

    def destroy(self):
        self.driver.quit()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def open_home_page(self):
        driver = self.driver
        driver.get('https://privnote.com/')

    def read_text_from_file(self):
        file = open('C:/QA/Autotests_Privnote/text.txt', 'r')
        outputtext = file.read()
        file.close()
        return outputtext

    def write_text_in_file(self):
        file = open('C:/QA/Autotests_Privnote/text.txt', 'w')
        file.write(pyperclip.paste())
        file.close()
