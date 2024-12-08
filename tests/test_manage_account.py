from datetime import datetime

import time

import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class TestManageAccount:

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

    def test_search_exactname(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")

        keyword_expected = "Người dùng tối cao"

        search_input = self.driver.find_element(By.CSS_SELECTOR,
                                                "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_input.send_keys(keyword_expected)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        rows = self.driver.find_elements(By.CSS_SELECTOR,
                                         "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr")

        for row in rows:
            cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            cell_text = cell.text.lower()
            assert keyword_expected.lower() in cell_text, f"Hàng không chứa keyword: {cell_text}"

    def test_search_keyword(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")

        keyword_expected = "n"

        search_input = self.driver.find_element(By.CSS_SELECTOR,
                                                "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_input.send_keys(keyword_expected)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        rows = self.driver.find_elements(By.CSS_SELECTOR,
                                         "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr")

        for row in rows:
            cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            cell_text = cell.text.lower()
            assert keyword_expected.lower() in cell_text, f"Hàng không chứa keyword: {cell_text}"

    def test_search_have_special_character(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")

        message_expected = "Không có dữ liệu"
        keyword_expected = "$%@"

        search_input = self.driver.find_element(By.CSS_SELECTOR,
                                                "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_input.send_keys(keyword_expected)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        message = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td > span")

        assert message.text == message_expected, "Kết quả trùng khớp"

    def test_search_surrounding_space(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")

        keyword_expected = " Người dùng tối cao "

        search_input = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_input.send_keys(keyword_expected)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        rows = self.driver.find_elements(By.CSS_SELECTOR,
                                         "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr")
        for row in rows:
            cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            cell_text = cell.text.lower()
            assert keyword_expected.lower().strip() in cell_text, f"Hàng không chứa keyword: {cell_text}"

    def test_create_valid_account(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR,
                                            "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_sc.is_displayed(), "Không có thông báo xuất hiện"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Khởi tạo dữ liệu thành công"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_pass_under_8_characters(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "1234567"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "1234567"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Thông báo không xuất hiện"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường mật khẩu phải có tối thiểu 8 kí tự."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_pass_not_match(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "1234567"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Thông báo không được hiển thị"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Giá trị xác nhận trong trường mật khẩu không khớp."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"


    def test_create_no_email(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = ""
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Thông báo không được hiển thị đúng"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường email không được bỏ trống."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_invalid_email(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demogmailcom"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Thông báo không được hiển thị đung1"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường email phải là một địa chỉ email hợp lệ."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_special_character_for_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = "!@#@$"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Thông báo hiển thị không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được có ký tự đặc biệt"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_no_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = ""
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Thông báo hiển thị không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được để trống"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_created_email(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/create")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(2) > input")
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Thông báo hiển thị không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường email đã có trong cơ sở dữ liệu."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"


    def test_update_pass_under_8_characters(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/9/edit")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_in.clear()
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        email_in.clear()
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        phone_in.clear()
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "1234567"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "1234567"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")
        assert alert_error.is_displayed(), "Cập nhật tài khoản xảy ra lỗi"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường mật khẩu phải có tối thiểu 8 kí tự."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_valid_account(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/9/edit")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_in.clear()
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                                "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        email_in.clear()
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                                "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        phone_in.clear()
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "1234567"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "1234567"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                                   "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                  "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                                       create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR,
                                                "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Cập nhật thành công tài khoản"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Cập nhật dữ liệu thành công."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_pass_not_match(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/9/edit")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_in.clear()
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "demo@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        email_in.clear()
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        phone_in.clear()
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "123456788"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "123456"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Chặn cập nhật tài khoản không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Cập nhật dữ liệu thành công."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_created_email(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/9/edit")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_in.clear()
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "user@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        email_in.clear()
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        phone_in.clear()
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Chặn cập nhật tài khoản không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường email đã có trong cơ sở dữ liệu."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_no_email(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/9/edit")

        name_expected = "Demo name"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_in.clear()
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = ""
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        email_in.clear()
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        phone_in.clear()
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Chặn cập nhật tài khoản không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường email không được bỏ trống."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_no_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/9/edit")

        name_expected = ""
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_in.clear()
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "nguyenddqui@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        email_in.clear()
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        phone_in.clear()
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Chặn cập nhật tài khoản không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được bỏ trống."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_special_character_for_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user/9/edit")

        name_expected = "@#!$#@"
        name_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(3) > input")
        name_in.clear()
        name_in.send_keys(name_expected)
        time.sleep(1)

        email_expected = "nguyenddqui@gmail.com"
        email_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(4) > input")
        email_in.clear()
        email_in.send_keys(email_expected)
        time.sleep(1)

        phone_expected = "0931368945"
        phone_in = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(5) > input")
        phone_in.clear()
        phone_in.send_keys(phone_expected)
        time.sleep(1)

        pass_expected = "12345678"
        pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(1) > div > input")
        pass_in.send_keys(pass_expected)
        time.sleep(1)

        cfm_pass_expected = "12345678"
        cfm_pass_in = self.driver.find_element(By.CSS_SELECTOR,
                                               "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div.row > div:nth-child(2) > div > input")
        cfm_pass_in.send_keys(cfm_pass_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > button")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", create_btn)
        time.sleep(1)
        create_btn.click()
        time.sleep(2)

        alert_error = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Chặn cập nhật tài khoản không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được chứa ký tự đặc biệt"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_sort_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")
        time.sleep(2)

        sort_btn = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > thead > tr > th:nth-child(2)")
        sort_btn.click()
        time.sleep(2)

        name_increase = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > span > div")

        list_name_increase = []
        for element in name_increase:
            text = element.text.strip()
            list_name_increase.append(text)

        increase = sorted(list_name_increase)

        assert list_name_increase == increase, "Sắp xếp thành công"

        time.sleep(2)

        sort_btn.click()
        time.sleep(2)

        name_decrease = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > span > div")

        list_name_decrease = []
        for element in name_decrease:
            text = element.text.strip()
            list_name_decrease.append(text)

        decrease = sorted(list_name_decrease, reverse=True)

        assert list_name_decrease == decrease, "Sắp xếp thành công"

    def test_sort_email(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")
        time.sleep(2)

        sort_btn = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > thead > tr > th:nth-child(3)")
        sort_btn.click()
        time.sleep(2)

        email_increase = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > span > div")

        list_email_increase = []
        for element in email_increase:
            text = element.text.strip()
            list_email_increase.append(text)

        increase = sorted(list_email_increase)

        assert list_email_increase == increase, "Sắp xếp thành công"

        time.sleep(2)

        sort_btn.click()
        time.sleep(2)

        email_decrease = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > span > div")

        list_email_decrease = []
        for element in email_decrease:
            text = element.text.strip()
            list_email_decrease.append(text)

        decrease = sorted(list_email_decrease, reverse=True)

        assert list_email_decrease == decrease, "Sắp xếp thành công"

    def test_sort_date(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")
        time.sleep(2)

        sort_btn = self.driver.find_element(By.CSS_SELECTOR,
                                            "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > thead > tr > th:nth-child(7)")
        sort_btn.click()
        time.sleep(2)

        date_increase = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(1) > td:nth-child(7) > span > div")

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

        date_decrease = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(1) > td:nth-child(7) > span > div")

        list_date_decrease = []
        for element in date_decrease:
            date_text = element.text.strip()
            try:

                date_obj = datetime.strptime(date_text, "%d/%m/%Y %H:%M:%S")
                list_date_decrease.append(date_obj)
            except ValueError as e:
                print(f"Lỗi định dạng ngày: {date_text}")

        decrease = sorted(list_date_decrease, reverse=True)

        assert list_date_decrease == decrease, "Sắp xếp thành công"

    def test_delete_account(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")
        time.sleep(2)

        delete_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(5) > td:nth-child(8) > span > div > a.btn.btn-danger.ml-2.delete-item")

        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", delete_btn)
        time.sleep(1)
        delete_btn.click()
        time.sleep(1)

        confirm_delete = self.driver.find_element(By.CSS_SELECTOR,
                                                  "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled.swal2-default-outline")
        confirm_delete.click()
        time.sleep(1)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR,
                                            "body > div.swal2-container.swal2-center.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Có hiển thị thông báo"

        time.sleep(1)

        ok_btn = self.driver.find_element(By.CSS_SELECTOR,
                                          "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
        ok_btn.click()
        time.sleep(1)

        message_expected = "Không có dữ liệu"
        search_input = self.driver.find_element(By.CSS_SELECTOR,
                                                "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_input.send_keys("Demo")
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        message = self.driver.find_element(By.CSS_SELECTOR,
                                           "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td > span")

        assert message.text == message_expected, "Kết quả trùng khớp"

    def test_ban_account(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/user")
        time.sleep(2)

        ban_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(4) > td:nth-child(5) > span > div > label > span")
        ban_btn.click()
        time.sleep(1)

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(2)

        account_btn = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        log_out_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > form > li > a")
        log_out_btn.click()
        time.sleep(2)

        account_btn = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > a")
        account_btn.click()
        time.sleep(1)

        login_btn = self.driver.find_element(By.CSS_SELECTOR,
                                             "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(1) > div > ul > li:nth-child(1)")
        login_btn.click()
        time.sleep(1)

        username_field = self.driver.find_element(By.CSS_SELECTOR,
                                                  "#view-product > div > div > form > div:nth-child(3) > input")
        password_field = self.driver.find_element(By.CSS_SELECTOR,
                                                  "#view-product > div > div > form > div:nth-child(5) > input")

        username_field.send_keys("nguyenddqui@gmail.com")
        password_field.send_keys("12345678")

        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "#loginAcc")
        submit_btn.click()
        time.sleep(2)

        message_expected = "Tài khoản của bạn đã bị khoá"
        message = self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > form > div:nth-child(4) > span")

        assert message.text == message_expected, "Tài khoản đã khóa không thành công"


