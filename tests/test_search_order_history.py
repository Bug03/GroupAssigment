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

class TestSearchOrderHistory:

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

        username_field.send_keys("user@gmail.com")
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

    def test_filter_category(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")

        select_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.form-control.form-select.shadow-none.power_grid"))
        )

        select = Select(select_element)

        options = select.options

        valid_options = [option for option in options if option.get_attribute("value") != ""]

        random_option = random.choice(valid_options)
        select.select_by_value(random_option.get_attribute("value"))

        selected_option = select.first_selected_option
        selected_value = selected_option.get_attribute("value").strip()
        selected_text = selected_option.text.strip()

        time.sleep(2)

        span_elements = self.driver.find_elements(By.XPATH,
                                                  "/html/body/section/div/div/div/div/div/div[2]/div/div[2]/div/table/tbody/tr[2]/td[5]/span/div/span")

        span_texts = [span.text for span in span_elements]

        if selected_value == "":
            valid_statuses = [
                "Đang chờ xử lý",
                "Đã xác nhận và sẵn sàng giao hàng",
                "Đang giao hàng",
                "Đã giao hàng",
                "Đã hủy"
            ]
            for status in valid_statuses:
                assert any(status in span_text for span_text in
                           span_texts), f"Không tìm thấy trạng thái '{status}' trong kết quả!"
        else:

            assert all(selected_text in span_text for span_text in
                       span_texts), f"Kết quả không khớp với trạng thái '{selected_text}'!"

    def test_seach_valid_phone(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(2)

        phone_numbers = [
            "0334202221",
            "0329859916",
            "0343754517",
        ]

        phone_expected = random.choice(phone_numbers)

        input_search = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(phone_expected)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        phone_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > span > div"))
        )

        assert len(phone_elements) >= 1, "Kết quả tìm kiếm có sự sai sót"

        found = True
        for phone in phone_elements:
            if phone_expected not in phone.text:
                found = False
                break

        assert found, "Kết quả tìm kiếm có sự sai sót"

    def test_seach_valid_phone_not_in_db(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(2)

        phone_expected = "0931369846"

        input_search = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(phone_expected)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(3) > td > span")
        message_expected = "Không có dữ liệu"

        assert message_actual.is_displayed(), "Thông báo không xuất hiện"

        assert message_actual.text == message_expected, "Kết quả tìm kiếm có sự sai sót"

    def test_seach_phone_not_full(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(2)

        phone_numbers = [
            "03342",
            "03298",
            "03437",
        ]

        phone_expected = random.choice(phone_numbers)

        input_search = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(phone_expected)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        phone_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > span > div"))
        )

        assert len(phone_elements) >= 1, "Kết quả tìm kiếm có sự sai sót"

        found = True
        for phone in phone_elements:
            if phone_expected not in phone.text:
                found = False
                break

        assert found, "Kết quả tìm kiếm có sự sai sót"

    def test_seach_phone_have_string(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(2)

        phone_numbers = [
            "03342",
            "03298",
            "03437",
        ]

        phone_expected = random.choice(phone_numbers) + self.random_alphabet_string(5)

        input_search = self.driver.find_element(By.CSS_SELECTOR,
                                                "body > section > div > div > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(phone_expected)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        message_actual = self.driver.find_element(By.CSS_SELECTOR,
                                                  "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(3) > td > span")
        message_expected = "Không có dữ liệu"

        assert message_actual.is_displayed(), "Thông báo không xuất hiện"

        assert message_actual.text == message_expected, "Kết quả tìm kiếm có sự sai sót"

    def test_seach_phone_sql_injection(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(2)

        phone_numbers = [
            "0334202221",
            "0329859916",
            "0343754517",
        ]

        phone_expected = random.choice(phone_numbers) + " OR '1' = 1"

        input_search = self.driver.find_element(By.CSS_SELECTOR,
                                                "body > section > div > div > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(phone_expected)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        message_actual = self.driver.find_element(By.CSS_SELECTOR,
                                                  "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(3) > td > span")
        message_expected = "Không có dữ liệu"

        assert message_actual.is_displayed(), "Thông báo không xuất hiện"

        assert message_actual.text == message_expected, "Kết quả tìm kiếm có sự sai sót"

    def test_seach_phone_have_space(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(2)

        phone_numbers = [
            "0334 202 221",
            " 0334202221",
            "0334202221 ",
            " 0334202221 "
        ]

        phone_expected = random.choice(phone_numbers)

        input_search = self.driver.find_element(By.CSS_SELECTOR,
                                                "body > section > div > div > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        input_search.send_keys(phone_expected)
        input_search.send_keys(Keys.ENTER)

        time.sleep(2)

        phone_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > span > div"))
        )

        assert len(phone_elements) >= 1, "Kết quả tìm kiếm có sự sai sót"

        found = True
        for phone in phone_elements:
            if phone_expected.replace(" ", "") not in phone.text:
                found = False
                break

        assert found, "Kết quả tìm kiếm có sự sai sót"


    def test_sort_price(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(3)

        sort_btn = self.driver.find_element(By.CSS_SELECTOR,
                                            "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > thead > tr > th:nth-child(3)")
        sort_btn.click()
        time.sleep(2)

        price_increase = self.driver.find_elements(By.CSS_SELECTOR,
                                                   "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > span > div")

        list_prices_increase = []
        for element in price_increase:
            text = element.text.strip()
            price = int(text)
            list_prices_increase.append(price)

        increase = sorted(list_prices_increase)

        assert list_prices_increase == increase, "Sắp xếp thành công"

        time.sleep(2)

        sort_btn.click()
        time.sleep(2)

        price_decrease = self.driver.find_elements(By.CSS_SELECTOR,
                                                   "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > span > div")

        list_price_decrease = []
        for element in price_decrease:
            text = element.text.strip()
            price = int(text)
            list_price_decrease.append(price)

        decrease = sorted(list_price_decrease, reverse=True)

        assert list_price_decrease == decrease, "Sắp xếp thành công"

    def test_sort_date(self, setup):
        self.driver.get("http://127.0.0.1:8000/orders")
        time.sleep(3)

        sort_btn = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > thead > tr > th:nth-child(6)")
        sort_btn.click()
        time.sleep(2)

        date_increase = self.driver.find_elements(By.CSS_SELECTOR,
                                                  "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td:nth-child(6) > span")

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
                                                    "body > section > div > div > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td:nth-child(6) > span")

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







