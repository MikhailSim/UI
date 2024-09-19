import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Сортировка клиентов")
@allure.story("Сортировка по имени")
def test_sort_customers_by_first_name(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    with allure.step("Переход к таблице клиентов и ожидание загрузки"):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Customers')]"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-bordered table-striped']")))

    with allure.step("Клик по заголовку 'First Name' для сортировки"):
        first_name_header = driver.find_element(By.XPATH, "//a[contains(text(), 'First Name')]")
        assert first_name_header.is_displayed(), "Header 'First Name' is not displayed"
        first_name_header.click()

    with allure.step("Проверка сортировки"):
        pass
