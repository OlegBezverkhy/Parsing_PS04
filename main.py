from os import path
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from time import sleep
import urllib.parse

URL = 'https://ru.wikipedia.org/wiki/Заглавная_страница'

WORD_IN_URL = 'Википедия'

# Глубина анализа страницы
global depth


def check_browser_and_launch():
    ''' Определяет установленный браузер. Если это не Chrome или Firefox, то
    сообщает об ошибке'''
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
            current_browser = webdriver.Firefox()
            return current_browser
        except WebDriverException as er:
            print(f'Ошибка при запуске Firefox: {er}')
    else:
        print('Ни один из браузеров (Chrome или Firefox) не найден.')
        return None


def get_paragraphs(browser, url, depth):
    ''' Печатает список параграфов на странице'''
    print(f'Промотр параграфов на странице {urllib.parse.unquote(url)}')
    browser.get(url)
    # Пауза для загрузки страницы
    sleep(4)
    if depth == 0:
        cl = 'searchResultImage-text'
        paragraphs = browser.find_elements(By.CLASS_NAME, cl)
    else:
        paragraphs = browser.find_elements(By.TAG_NAME, 'p')
    for i, paragraph in enumerate(paragraphs):
        print(f'Параграф {i + 1}:\n {paragraph.text}\n')
        next_par = input('Нажмите <Enter> для просмотра следующего параграфа или <q> для выхода\n')
        if next_par == 'q':
            break


def get_links(browser, query,depth):
    ''' Находит и возвращает список связанных ссылок на сайте,
    которые содержат текст запроса'''
    links = browser.find_elements(By.TAG_NAME, 'a')
    if depth == 0:
        return [link.get_attribute('href')
                for link in links
                if link.get_attribute('href') and query in link.text]
    else:
        return [link.get_attribute('href')
                for link in links
                if link.get_attribute('href')]


def choice_action():
    ''' Осуществляет выбор пользователем варианта действий из трех возможнных'''
    choices = ('1', '2', '3')
    while True:
        print('Выберите варианты действий:')
        print('1. Листать параграфы текущей статьи')
        print('2. Перейти на одну из связанных страниц')
        print('3. Выйти')
        choice = input(' (1-3) >>>>  ')
        if choice in choices:
            return choice
        else:
            print('Неверный выбор. Попробуйте еще раз.')


def input_query(browser, word):
    '''Проверяет соответсвие фактически открытой странице ожидаемой. Просит
    ввести запрос. Находит поле ввода на сайте, помещает туда текст запроса
    и запускает поиск. В случае ошибки или ввода вместо запоса слова exit
    завершает выполнение программы'''
    if word in browser.title:
        search_query = input('Введите запрос: ')
        if search_query.lower() == 'exit':
            exit(0)
        # Находим окно поиска
        search_box = browser.find_element(By.ID, 'searchInput')
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        return search_query
    else:
        print('Ошибка обработки запроса')
        exit(1)


def list_links(browser, query, depth):
    links = get_links(browser, query, depth)
    if not links:
        print('Нет связанных статей')
        return
    print(f'Найдено {len(links)} связанных статей:')
    for i, link in enumerate(links):
        print(f'{i + 1}. {urllib.parse.unquote(link)}')
    return links


def link_select(browser, links):
    ''' Возвращает выбранную ссылку или текущую если выбор не был сделан'''
    while True:
        linked_choice = input('Введите номер статьи для перехода (или <q> для возврата): ')
        try:
            linked_index = int(linked_choice)-1
            if 0 <= linked_index < len(links):
                url_link = links[linked_index]
                break
            else:
                print('Неверный ввод. Попробуйте снова.')
        except ValueError:
            print('Неверный ввод. Попробуйте снова.')
        if linked_choice.lower() == 'q':
            return browser.current_url
    return url_link


def menu(browser, query, url_link, depth):
    ''' Меню выбора действия пользователя'''
    if depth != 0:
        browser.get(url_link)
    while True:
        choice = choice_action()
        if choice == '1':
            current_url = browser.current_url
            get_paragraphs(browser, current_url, depth)
        elif choice == '2':
            links = list_links(browser, query, depth)
            url_link = link_select(browser,links)
            depth += 1
            menu(browser, query, url_link, depth)
        elif choice == '3':
            depth -= 1
            browser.quit()
            return


def main():
    print('Программа работает только с браузерами Chrome или Firefox. Проверьте их наличие')
    browser = check_browser_and_launch()
    depth = 0
    if browser:
        browser.get(URL)
        while True:
            query = input_query(browser, WORD_IN_URL)
            menu(browser, query, URL, depth)
            return


if __name__ == '__main__':
    main()
