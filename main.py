from os import path
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import time

URL = 'https://ru.wikipedia.org/wiki/Заглавная_страница'


def check_browser_and_launch():
    # Путь к Chrome
    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # Путь к Firefox
    firefox_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

    chrome_installed = path.exists(chrome_path)
    firefox_installed = path.exists(firefox_path)

    if chrome_installed:
        print('Найден браузер Chrome.')
        try:
            # Запуск Chrome через Selenium
            current_browser = webdriver.Chrome()
            return current_browser
        except WebDriverException as er:
            print(f'Ошибка при запуске Chrome: {er}')
    elif firefox_installed:
        print('Найден браузер Firefox.')
        try:
            # Запуск Firefox через Selenium
            current_browser = webdriver.Firefox()  # Убедитесь, что geckodriver доступен в PATH
            return current_browser
        except WebDriverException as er:
            print(f'Ошибка при запуске Firefox: {er}')
    else:
        print('Ни один из браузеров (Chrome или Firefox) не найден.')
        return None


def get_paragraphs(browser, url):
    browser.get(url)
    # Пауза для загрузки страницы
    time.sleep(2)
    paragraphs = browser.find_elements(By.TAG_NAME, 'p')
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}: {paragraph.text}\n")


def get_links(browser):
    links = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/wiki/"]')
    return [link.get_attribute('href') for link in links]


def main():
    print('Программа работает только с браузерами Chrome или Firefox. Проверьте их наличие')
    browser = check_browser_and_launch()
    if browser:
        while True:
            # Переход на сайт Википедии
            browser.get(URL)
            # Проверяем по заголовку, тот ли сайт открылся
            assert "Википедия" in browser.title
            search_query = input('Введите запрос: ')
            if search_query.lower() == 'exit':
                break
            # Находим окно поиска
            search_box = browser.find_element(By.ID, 'searchInput')
            search_box.send_keys(question)
            search_box.send_keys(Keys.RETURN)
            input("Нажмите Enter, чтобы закрыть браузер...")
            browser.quit()


if __name__ == '__main__':
    main()
