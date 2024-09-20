import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def setup():
    chrome_options = Options()

    # Включаем режим headless для CI/CD
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Указываем разрешение экрана (особенно важно для безголового режима)
    chrome_options.add_argument("window-size=1920,1080")

    # Создаем экземпляр веб-драйвера с автоматической установкой ChromeDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Устанавливаем начальный URL
    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager")

    # Устанавливаем ожидание для полной загрузки страницы
    driver.implicitly_wait(10)

    yield driver  # Возвращаем драйвер для использования в тестах

    driver.quit()  # Закрываем драйвер после завершения теста
