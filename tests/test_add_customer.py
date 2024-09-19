import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Добавление клиентов")
@allure.story("Добавление нового клиента")
def test_add_customer(setup):
    driver = setup
    wait = WebDriverWait(driver, 20)

    with allure.step("Переход на страницу добавления клиента"):
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager/addCust")

    with allure.step("Заполнение формы добавления клиента"):
        first_name_input = driver.find_element(By.XPATH, "//input[@ng-model='fName']")
        last_name_input = driver.find_element(By.XPATH, "//input[@ng-model='lName']")
        post_code_input = driver.find_element(By.XPATH, "//input[@ng-model='postCd']")

        first_name = "John"
        last_name = "Doe"
        post_code = "12345"

        first_name_input.send_keys(first_name)
        last_name_input.send_keys(last_name)
        post_code_input.send_keys(post_code)

    with allure.step("Нажатие на кнопку 'Add Customer'"):
        add_customer_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        add_customer_button.click()

    with allure.step("Подтверждение добавления клиента"):
        # Ожидание появления модального окна с подтверждением
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        assert "Customer added successfully" in alert_text, "Сообщение об успешном добавлении клиента не отображается"

    with allure.step("Проверка, что клиент был добавлен"):
        # Переход к списку клиентов и ожидание его загрузки
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Customers')]"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-bordered table-striped']")))

        # Поиск нового клиента в таблице
        customer_rows = driver.find_elements(By.XPATH,
                                             "//table[@class='table table-bordered table-striped']//tbody//tr")

        # Проверка по первому имени клиента
        found_first_name = any(first_name in row.find_element(By.XPATH, ".//td[1]").text for row in customer_rows)

        assert found_first_name, f"Клиент с именем {first_name} не найден в таблице"
