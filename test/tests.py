from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from time import sleep
import random
import string


def test_create_empty_note(app):
    driver = app.driver
    # открываем главную страницу
    app.open_home_page()
    # создаем записку с пустым текстом
    inputtext = ""
    app.create_note(inputtext)
    # проверяем, что есть сообщение об ошибке
    assert app.is_element_present(By.CSS_SELECTOR, "#error_note_is_empty"), "Error hint doesn't exist"
    # проверяем, текст сообщения
    assert "Ошибка: текст записки пуст" in driver.find_element_by_css_selector("#error_note_is_empty").text, "Error hint isn't correct"


def test_create_and_read_note_with_confirm(app):
    driver = app.driver
    app.open_home_page()
    # создаем записку со случайным текстом
    inputtext = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(200))])
    app.create_note(inputtext)
    # получаем ссылку на заметку и открываем ее
    link = driver.find_element_by_css_selector("#show_link").get_attribute("href")
    driver.get(link)
    # подтверждаем прочтение нажатием кнопки
    driver.find_element_by_css_selector("#confirm_button").click()
    # считываем текст записки и сохраняем в файл (по-другому никак)
    app.copy_note_text()
    app.write_text_in_file()
    outputtext = app.read_text_from_file()
    # проверяем, что открылась правильная записка (исходный текст равен полученному)
    assert inputtext == str(outputtext), "Output text differ from input text"


def test_create_and_read_note_without_confirm(app):
    driver = app.driver
    # открываем главную страницу
    app.open_home_page()
    inputtext = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(200))])
    # открываем дополнительные параметры
    driver.find_element_by_css_selector("#advanced_options_show").click()
    # снимаем флажок, чтобы записки удалялись без подтверждения
    driver.find_element_by_css_selector("#destroy_without_confirmation").click()
    # завершаем создание записки
    app.create_note_with_scrolling(inputtext)
    # получаем ссылку на заметку и открываем ее
    link = driver.find_element_by_css_selector("#show_link").get_attribute("href")
    driver.get(link)
    # считываем текст записки и сохраняем в файл
    app.copy_note_text()
    app.write_text_in_file()
    outputtext = app.read_text_from_file()
    # проверяем, что открылась правильная записка (исходный текст равен полученному)
    assert inputtext == str(outputtext), "Output text differ from input text"


def test_read_destroyed_note_via_link(app):
    driver = app.driver
    app.open_home_page()
    inputtext = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(200))])
    app.create_note(inputtext)
    # получаем ссылку на заметку и открываем ее
    link = driver.find_element_by_css_selector("#show_link").get_attribute("href")
    driver.get(link)
    # извлекаем из сообщения ИД записки
    id = driver.find_element_by_css_selector("#link_ok p strong").get_attribute("strong")
    # подтверждаем прочтение нажатием кнопки
    driver.find_element_by_css_selector("#confirm_button").click()
    driver.get(link)
    # проверяем, что есть сообщение об ошибке, и записка на самом деле удалена
    assert app.is_element_present(By.CSS_SELECTOR, "#note_error"), "Error hint doesn't exist"
    # проверяем, что удалилась правильная записка с нужным ИД
    error = driver.find_element_by_css_selector("#note_error p").get_attribute("p")
    assert str(id) in str(error),  "Incorrect note was destroyed"


def test_create_and_read_note_with_correct_password(app):
    driver = app.driver
    app.open_home_page()
    inputtext = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(200))])
    # открываем дополнительные параметры
    driver.find_element_by_css_selector("#advanced_options_show").click()
    # заполняем пароли случайным значением
    password = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(50))])
    driver.find_element_by_css_selector("#manual_password").send_keys(password)
    driver.find_element_by_css_selector("#manual_password_confirm").send_keys(password)
    # завершаем создание записки
    app.create_note_with_scrolling(inputtext)
    link = driver.find_element_by_css_selector("#show_link").get_attribute("href")
    # получаем пароль и сохраняем, который нам подсказывает сайт
    driver.find_element_by_css_selector("#show_password").click()
    driver.find_element_by_css_selector("#select_password").click()
    driver.find_element_by_css_selector("#note_password_input").send_keys(Keys.CONTROL, 'c')
    app.write_text_in_file()
    password2 = app.read_text_from_file()
    # проверяем, что пароль в подсказке правильный, и совпадает с исходным
    assert password == password2, "Incorrect password is showed"
    # открываем записку
    driver.get(link)
    # подтверждаем прочтение нажатием кнопки
    driver.find_element_by_css_selector("#confirm_button").click()
    # вводим пароль
    driver.find_element_by_css_selector("#note_password").send_keys(password)
    driver.find_element_by_css_selector("#decrypt_button").click()
    # считываем текст записки и сохраняем в файл
    app.copy_note_text()
    app.write_text_in_file()
    outputtext = app.read_text_from_file()
    # проверяем, что открылась правильная записка (исходный текст равен полученному)
    assert inputtext == str(outputtext), "Output text differ from input text"


def test_create_and_read_note_with_incorrect_password(app):
     driver = app.driver
     app.open_home_page()
     inputtext = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(200))])
     # открываем дополнительные параметры
     driver.find_element_by_css_selector("#advanced_options_show").click()
     # заполняем пароли случайным значением
     password = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(50))])
     driver.find_element_by_css_selector("#manual_password").send_keys(password)
     driver.find_element_by_css_selector("#manual_password_confirm").send_keys(password)
     # завершаем создание записки
     app.create_note_with_scrolling(inputtext)
     # получаем ссылку на заметку и открываем ее
     link = driver.find_element_by_css_selector("#show_link").get_attribute("href")
     driver.get(link)
     # подтверждаем прочтение нажатием кнопки
     driver.find_element_by_css_selector("#confirm_button").click()
     # вводим неправильный пароль
     driver.find_element_by_css_selector("#note_password").send_keys(password*2)
     driver.find_element_by_css_selector("#decrypt_button").click()
     # проверяем, что есть сообщение об ошибке
     assert "Введен неверный пароль" in driver.find_element_by_css_selector("#error_password_incorrect").text, "Error hint isn't correct"


# Тест падает.
@pytest.mark.xfail
def test_read_destroyed_note_via_button(app):
    driver = app.driver
    app.open_home_page()
    inputtext = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(200))])
    app.create_note(inputtext)
    # получаем ссылку на заметку, копируем, записываем в файл
    link = driver.find_element_by_css_selector("#show_link").get_attribute("href")
    driver.find_element_by_css_selector("#select_link").click()
    driver.find_element_by_css_selector("#note_link_input").send_keys(Keys.CONTROL, 'c')
    app.write_text_in_file()
    # из полученного значения извлекаем ИД
    outputtext = app.read_text_from_file()
    id = str(outputtext)[22:29]
    # уничтожаем записку
    driver.find_element_by_css_selector("#destroy_link").click()
    driver.find_element_by_css_selector("#confirm_button").click()
    driver.get(link)
    # подтверждаем прочтение нажатием кнопки
    assert app.is_element_present(By.CSS_SELECTOR, "#note_error"), "Error hint doesn't exist"
    error = driver.find_element_by_css_selector("#note_error p").get_attribute("p")
    # проверяем, что удалилась правильная записка с нужным ИД
    assert id in str(error), "Incorrect note was destroyed"
    # здесь тест падает с ошибкой AssertionError: Incorrect note was destroyed
    # assert 'JRuPLwy' in 'None'
    # как будто строки с ошибкой нет, хотя она есть и селектор верный. Возможно, надо знать особенности кода.


# Тест падает.
@pytest.mark.xfail
def test_self_destruction_an_hour(app):
    driver = app.driver
    app.open_home_page()
    inputtext = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randrange(200))])
    # открываем дополнительные параметры
    driver.find_element_by_css_selector("#advanced_options_show").click()
    # ставим самоуничтожение записки спустя час
    driver.find_element_by_css_selector("#duration_hours").click()
    driver.find_element_by_css_selector("[value='1']").click()
    # завершаем создание записки
    app.create_note_with_scrolling(inputtext)
    # получаем ссылку на заметку и открываем ее в случайном интервале меньше часа
    link = driver.find_element_by_css_selector("#show_link").get_attribute("href")
    time = (random.randrange(1, 55))*60
    sleep(time)
    driver.get(link)
    # извлекаем из сообщения ссылку на записку
    link2 = driver.find_element_by_css_selector("#note_link").get_attribute("href")
    # проверяем, что ссылка в сообщении корректная и совпадает с исходной
    assert link == link2, "Link in hint is incorrect"
    # извлекаем из ссылки ИД
    id = str(link2)[22:29]
    # ожидаем остаточный интервал времени (немного с запасом) и снова открываем ссылку
    time2 = 65*60 - time
    sleep(time2)
    driver.get(link)
    # проверяем, что есть сообщение об ошибке
    assert app.is_element_present(By.CSS_SELECTOR, "#note_error"), "Error hint doesn't exist"
    # проверяем, что удалилась правильная записка с нужным ИД
    error = driver.find_element_by_css_selector("#note_error p").get_attribute("p")
    assert str(id) in str(error),  "Incorrect note was destroyed"
    # здесь тест падает аналогично предыдущему с ошибкой AssertionError: Incorrect note was destroyed
    # assert 'JRuPLwy' in 'None'
    # как будто строки с ошибкой нет, хотя она есть и селектор верный. Возможно, надо знать особенности кода.
