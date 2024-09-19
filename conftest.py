import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def setup():
    chrome_options = Options()
    # Убираем headless режим, чтобы окно браузера было видно
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Создаем экземпляр веб-драйвера
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Устанавливаем начальный URL
    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager")

    # Ожидание, чтобы страница полностью загрузилась
    driver.implicitly_wait(10)

    yield driver  # Возвращаем драйвер для использования в тестах

    driver.quit()  # Закрываем драйвер после завершения теста
