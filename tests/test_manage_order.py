import string
from datetime import datetime
import random
import time


import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestManageOrder:
    """Test chức năng Add to Cart."""

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, request):
        driver = webdriver.Chrome()
        driver.maximize_window()
        request.cls.driver = driver
        self.login()
        yield
        driver.quit()

    def login(self):

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(2)

        account_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        login_btn = self.driver.find_element(By.CSS_SELECTOR,"body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(1)")
        login_btn.click()
        time.sleep(1)

        username_field = self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > form > div:nth-child(3) > input")
        password_field = self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > form > div:nth-child(5) > input")

        username_field.send_keys("admin@gmail.com")
        password_field.send_keys("123")

        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "#loginAcc")
        submit_btn.click()
        time.sleep(1)

        sc_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
        sc_btn.click()
        time.sleep(2)

    def random_special_characters(self, length):
        special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\`~"
        return ''.join(random.choice(special_chars) for _ in range(length))

    def random_alphabet_string(sefl, length):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def test_update_payment(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(5)

        sort_payment = self.driver.find_element(By.XPATH,
                                                '//*[@id="app"]/div/div[3]/section/div[2]/div/div/div/div[2]/div/div[2]/div/table/thead/tr/th[4]')

        sort_payment.click()
        time.sleep(2)

        checkboxes = self.driver.find_elements(By.CSS_SELECTOR, ".custom-switch-input.change-payment-status")

        assert len(checkboxes) > 0, "Không tìm thấy checkboxes nào"

        random_checkbox = random.choice(checkboxes)

        ActionChains(self.driver).move_to_element(random_checkbox).click().perform()
        time.sleep(2)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Cập nhật không thành công"

        time.sleep(2)

    def test_update_status(self):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(5)

        td_elements = self.driver.find_elements(By.XPATH, '//td[.//select[@name="order_status"]]')
        assert len(td_elements) > 0, "Không tìm thấy cột nào chứa <select>!"

        random_td = random.choice(td_elements)
        select_element = random_td.find_element(By.XPATH, './/select[@name="order_status"]')

        select = Select(select_element)
        current_value = select.first_selected_option.get_attribute("value")
        print("Giá trị hiện tại của <select>: ", current_value)

        options = select.options
        assert len(options) > 1, "Không đủ tùy chọn trong <select> để thay đổi!"

        new_option = random.choice([opt for opt in options if opt.get_attribute("value") != current_value])
        new_value = new_option.get_attribute("value")

        select.select_by_value(new_value)
        time.sleep(2)


        alert_sc = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div"))
        )
        assert alert_sc.is_displayed(), "Cập nhật không thành công"

        btn_sc = self.driver.find_element(By.CSS_SELECTOR,
                                          "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
        btn_sc.click()


        WebDriverWait(self.driver, 10).until(
            EC.staleness_of(select_element)
        )

        select_element = self.driver.find_element(By.XPATH, './/select[@name="order_status"]')
        select = Select(select_element)
        updated_value = select.first_selected_option.get_attribute("value")
        assert updated_value != new_value, "Giá trị <select> không được cập nhật thành công!"
        print("Giá trị <select> đã được cập nhật thành công!")

    def test_sort_price(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        sort_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > thead > tr > th:nth-child(3)")
        sort_btn.click()
        time.sleep(2)

        price_increase = self.driver.find_elements(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr > td:nth-child(3) > span > div")

        list_prices_increase = []
        for element in  price_increase:
            text = element.text.strip()
            price = int(text)
            list_prices_increase.append(price)

        increase = sorted(list_prices_increase)

        assert list_prices_increase == increase, "Sắp xếp thành công"

        time.sleep(2)

        sort_btn.click()
        time.sleep(2)

        price_decrease = self.driver.find_elements(By.CSS_SELECTOR,
                                                   "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr > td:nth-child(3) > span > div"
                                                   )

        list_price_decrease = []
        for element in  price_decrease:
            text = element.text.strip()
            price = int(text)
            list_price_decrease.append(price)

        decrease = sorted(list_price_decrease, reverse = True)

        assert list_price_decrease ==  decrease, "Sắp xếp thành công"

    def test_sort_date(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        sort_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > thead > tr > th:nth-child(6)")
        sort_btn.click()
        time.sleep(2)

        date_increase = self.driver.find_elements(By.CSS_SELECTOR,
                                                  "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr > td:nth-child(6) > span > div"
                                                  )


        list_date_increase = []
        for element in date_increase:
            date_text = element.text.strip()
            try:

                date_obj = datetime.strptime(date_text, "%d/%m/%Y %H:%M:%S")
                list_date_increase.append(date_obj)
            except ValueError as e:
                print(f"Lỗi định dạng ngày: {date_text}")

        increase = sorted(list_date_increase)

        assert list_date_increase == increase, "Sắp xếp thành công"

        time.sleep(2)

        sort_btn.click()
        time.sleep(2)

        date_decrease = self.driver.find_elements(By.CSS_SELECTOR,
                                                    "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr > td:nth-child(6) > span > div")

        list_date_decrease = []
        for element in date_decrease:
            date_text = element.text.strip()
            try:

                date_obj = datetime.strptime(date_text, "%d/%m/%Y %H:%M:%S")
                list_date_decrease.append(date_obj)
            except ValueError as e:
                print(f"Lỗi định dạng ngày: {date_text}")

        decrease = sorted(list_date_decrease, reverse = True)

        assert list_date_decrease ==  decrease, "Sắp xếp thành công"

    def test_search_valid_phone(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        phone_numbers = [
            "0334202221",
            "0329859916",
            "0343754517",
        ]

        random_phone = random.choice(phone_numbers)

        input_search = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(random_phone)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        phones = self.driver.find_elements(
            By.CSS_SELECTOR,
            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr > td:nth-child(2) > span > div"
        )

        assert len(phones) >= 1, "Kết quả tìm kiếm có sự sai sót"

        found = True
        for phone in phones:
            phone = phone.text.strip()
            if random_phone not in phone:
                found = False
                break

        assert found, f"Số điện thoại {random_phone} tìm kiếm bị lỗi"

    def test_search_phone_not_full(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        phone_numbers = [
            "03342",
            "03298",
            "03437",
        ]

        random_phone = random.choice(phone_numbers)

        input_search = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(random_phone)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        phones = self.driver.find_elements(
            By.CSS_SELECTOR,
            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr > td:nth-child(2) > span > div"
        )

        assert len(phones) >= 1, "Kết quả tìm kiếm có sự sai sót"

        found = True
        for phone in phones:
            phone = phone.text.strip()
            if random_phone not in phone:
                found = False
                break

        assert found, f"Số điện thoại {random_phone} tìm kiếm bị lỗi"

    def test_search_phone_special_character(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        phone_numbers = [
            "03342",
            "03298",
            "03437",
        ]

        random_phone = random.choice(phone_numbers) + self.random_special_characters(5)

        input_search = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(random_phone)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        message = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(3) > td > span")

        message_expected = "Không có dữ liệu"

        assert message.is_displayed(), "Message không hiển thị"

        assert message.text == message_expected, "Thông tin hiển thị không chính xác"

    def test_search_phone_have_alphabet(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        phone_numbers = [
            "03342",
            "03298",
            "03437",
        ]

        random_phone = random.choice(phone_numbers) + self.random_alphabet_string(5)

        input_search = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(random_phone)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        message = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(3) > td > span")

        message_expected = "Không có dữ liệu"

        assert message.is_displayed(), "Message không hiển thị"

        assert message.text == message_expected, "Thông tin hiển thị không chính xác"

    def test_search_phone_sql_injection(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        phone_numbers = [
            "0334202221",
            "0329859916",
            "0343754517",
        ]

        random_phone = random.choice(phone_numbers) + " OR '1' = 1"

        input_search = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(random_phone)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        message = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(3) > td > span")

        message_expected = "Không có dữ liệu"

        assert message.is_displayed(), "Message không hiển thị"

        assert message.text == message_expected, "Thông tin hiển thị không chính xác"

    def test_search_phone_have_space(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/order")
        time.sleep(3)

        phone_numbers = [
            "0334 202 221",
            " 0334202221",
            "0334202221 ",
            " 0334202221 "
        ]

        random_phone = random.choice(phone_numbers)

        input_search = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(random_phone)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        phones = self.driver.find_elements(
            By.CSS_SELECTOR,
            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr > td:nth-child(2) > span > div"
        )

        assert len(phones) >=1 , "Kết quả tìm kiếm có sự sai sót"

        found = True
        for phone in phones:
            phone = phone.text.strip()
            if random_phone.replace(" ", "") not in phone:
                found = False
                break

        assert found == True, f"Số điện thoại {random_phone} tìm kiếm bị lỗi"





