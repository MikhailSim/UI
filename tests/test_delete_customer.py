import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_customer_names(driver, wait):
    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager")

    # Ожидание загрузки страницы и кнопки "Customers"
    customers_button_xpath = "//button[@ng-click='showCust()']"
    wait.until(EC.element_to_be_clickable((By.XPATH, customers_button_xpath))).click()

    # Ожидание таблицы клиентов
    customer_table_xpath = "//table[@class='table table-bordered table-striped']"
    wait.until(EC.visibility_of_element_located((By.XPATH, customer_table_xpath)))

    # Найти все имена в таблице
    customer_names_elements = driver.find_elements(By.XPATH, "//table[@class='table table-bordered table-striped']//tbody//tr//td[1]")
    customer_names = [element.text for element in customer_names_elements]

    if not customer_names:
        pytest.fail("Не удалось найти клиентов в таблице")

    return customer_names

def calculate_average_length(names):
    lengths = [len(name) for name in names]
    if not lengths:
        return 0
    return sum(lengths) / len(lengths)

def find_closest_name(names, average_length):
    # Найти имя, длина которого ближе всего к среднему
    closest_name = min(names, key=lambda name: abs(len(name) - average_length))
    return closest_name

def delete_customer(driver, wait, customer_name):
    # Ожидание таблицы клиентов
    customer_table_xpath = "//table[@class='table table-bordered table-striped']"
    wait.until(EC.visibility_of_element_located((By.XPATH, customer_table_xpath)))

    # Найти строку с клиентом для удаления
    customer_rows = driver.find_elements(By.XPATH, "//table[@class='table table-bordered table-striped']//tbody//tr")
    for row in customer_rows:
        name_element = row.find_element(By.XPATH, ".//td[1]")
        if name_element.text == customer_name:
            delete_button = row.find_element(By.XPATH, ".//button[@ng-click='deleteCust(cust)']")
            driver.execute_script("arguments[0].scrollIntoView(true);", delete_button)  # Прокрутить до кнопки
            delete_button.click()  # Нажать на кнопку удаления
            print(f"Клиент '{customer_name}' успешно удален.")
            break
    else:
        pytest.fail(f"Не удалось найти клиента с именем {customer_name} для удаления")

@allure.feature("Удаление клиентов")
@allure.story("Удаление клиента по средней длине имени")
def test_delete_customer(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    with allure.step("Получение списка клиентов"):
        customer_names = get_customer_names(driver, wait)

    with allure.step("Рассчитываем среднюю длину имени"):
        average_length = calculate_average_length(customer_names)

    with allure.step("Находим клиента с длиной имени ближе всего к средней"):
        closest_name = find_closest_name(customer_names, average_length)

    with allure.step("Удаляем клиента с найденным именем"):
        delete_customer(driver, wait, closest_name)

    with allure.step("Проверка, что клиент был удален"):
        remaining_names = get_customer_names(driver, wait)
        assert closest_name not in remaining_names, f"Клиент {closest_name} не был удален"
