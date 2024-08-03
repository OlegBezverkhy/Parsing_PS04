import os
import subprocess
import platform
from selenium import webdriver


def get_browser_driver():
    # Определяем текущую операционную систему
    system = platform.system()

    # Ищем установленный браузер
    if system == "Windows":
        # Проверяем наличие Chrome
        chrome_installed = subprocess.call("where chrome", shell=True) == 0
        # Проверяем наличие Firefox
        firefox_installed = subprocess.call("where firefox", shell=True) == 0
    elif system == "Linux":
        chrome_installed = subprocess.call("which google-chrome", shell=True) == 0
        firefox_installed = subprocess.call("which firefox", shell=True) == 0
    elif system == "Darwin":  # MacOS
        chrome_installed = subprocess.call("which google-chrome", shell=True) == 0
        firefox_installed = subprocess.call("which firefox", shell=True) == 0
    else:
        raise Exception("Unsupported OS")

    # Запускаем соответствующий драйвер
    if chrome_installed:
        print("Запускаем Chrome...")
        driver = webdriver.Chrome()  # Убедитесь, что Chromedriver установлен и доступен в PATH
    elif firefox_installed:
        print("Запускаем Firefox...")
        driver = webdriver.Firefox()  # Убедитесь, что Geckodriver установлен и доступен в PATH
    else:
        raise Exception("Не найден установленный браузер (Chrome или Firefox).")

    return driver

def main():
    driver = get_browser_driver()
    driver.get("https://www.google.com")

if __name__ == '__main__':
    main()