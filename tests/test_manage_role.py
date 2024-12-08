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

class TestManageRole:
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

        username_field.send_keys("admin@gmail.com")
        password_field.send_keys("123")

        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "#loginAcc")
        submit_btn.click()
        time.sleep(1)

        sc_btn = self.driver.find_element(By.CSS_SELECTOR,
                                          "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
        sc_btn.click()
        time.sleep(2)

    def test_search_exactname(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role")

        keyword_expected = "Supper User"

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
            assert keyword_expected.lower() in cell_text, f"Hàng không chứa keyword: {cell_text}"

    def test_search_have_special_character(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role")

        message_expected = "Không có dữ liệu"
        keyword_expected = "User$%@"

        search_input = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_input.send_keys(keyword_expected)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        message = self.driver.find_element(By.CSS_SELECTOR,
                                    "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(2) > td > span")

        assert message.text == message_expected, "Kết quả trùng khớp"

    def test_search_special_character(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role")

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

    def test_search_keyword(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role")

        keyword_expected = "Us"

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
            assert keyword_expected.lower() in cell_text, f"Hàng không chứa keyword: {cell_text}"

    def test_search_surrounding_space(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role")

        keyword_expected = " User "

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


    def test_create_role_no_permission(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/create")
        time.sleep(2)

        name_expected = "Demo"
        input_name = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(2) > input")
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_des = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_des.send_keys(description_expected)
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        create_btn.click()
        time.sleep(1)

        alert_error = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Thông báo hiển thị không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường quyền không được bỏ trống."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_role_no_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/create")
        time.sleep(2)

        name_expected = ""
        input_name = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(2) > input")
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_des = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_des.send_keys(description_expected)
        time.sleep(1)

        check_box = self.driver.find_element(By.CSS_SELECTOR,
                                             "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div.form-group.container > div > div:nth-child(6) > input[type=checkbox]")
        check_box.click()
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        create_btn.click()
        time.sleep(1)

        alert_error = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Thông báo hiển thị không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được bỏ trống"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_existed_role_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/create")
        time.sleep(2)

        name_expected = "Supper Admin"
        input_name = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(2) > input")
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_des = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_des.send_keys(description_expected)
        time.sleep(1)

        check_box = self.driver.find_element(By.CSS_SELECTOR,
                                             "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div.form-group.container > div > div:nth-child(6) > input[type=checkbox]")
        check_box.click()
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        create_btn.click()
        time.sleep(1)

        alert_error = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Thông báo hiển thị không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Dữ liệu tồn tại trong hệ thống."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_create_role_name_special_characters(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/create")
        time.sleep(2)

        name_expected = "@#@@%#"
        input_name = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(2) > input")
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_des = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_des.send_keys(description_expected)
        time.sleep(1)

        check_box = self.driver.find_element(By.CSS_SELECTOR,
                                             "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div.form-group.container > div > div:nth-child(6) > input[type=checkbox]")
        check_box.click()
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        create_btn.click()
        time.sleep(1)

        alert_error = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Thông báo hiển thị không thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được có ký tự đặc biệt"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_valid_role(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/create")
        time.sleep(2)

        name_expected = "Demo"
        input_name = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(2) > input")
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_des = self.driver.find_element(By.CSS_SELECTOR,
                                             "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_des.send_keys(description_expected)
        time.sleep(1)

        check_box = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div.form-group.container > div > div:nth-child(6) > input[type=checkbox]")
        check_box.click()
        time.sleep(1)

        create_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        create_btn.click()
        time.sleep(1)

        self.driver.get("http://127.0.0.1:8000/admin/role")


        search_input = self.driver.find_element(By.CSS_SELECTOR,
                                                "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div:nth-child(1) > div > div.dt--top-section > div > div.col-12.col-sm-6.d-flex.justify-content-sm-end.justify-content-center.mt-sm-0.mt-3 > div > label > div > input")
        search_input.send_keys(name_expected)
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        rows = self.driver.find_elements(By.CSS_SELECTOR,
                                         "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr")
        for row in rows:
            cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            cell_text = cell.text.lower()
            assert name_expected.lower() in cell_text, f"Hàng không chứa keyword: {cell_text}"

    def test_delete_role(self,setup):
        self.driver.get("http://127.0.0.1:8000/admin/role")
        time.sleep(2)

        delete_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > div > div.table-responsive.col-md-12 > div > table > tbody > tr:nth-child(4) > td:nth-child(5) > span > div > a.btn.btn-danger.ml-2.delete-item")
        delete_btn.click()
        time.sleep(1)

        confirm_delete = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled.swal2-default-outline")
        confirm_delete.click()
        time.sleep(1)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Có hiển thị thông báo"

        time.sleep(1)

        ok_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
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

    def test_update_valid_role(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/3/edit")
        name_expected = "Demo"

        input_name = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_name.clear()
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_description = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(4) > input")
        input_description.clear()
        input_description.send_keys(description_expected)
        time.sleep(1)

        update_btn = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        update_btn.click()
        time.sleep(1)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Thông báo không được hiển thị thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Cập nhật dữ liệu thành công"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_no_permission(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/3/edit")
        name_expected = "Demo"

        input_name = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_name.clear()
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_description = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(4) > input")
        input_description.clear()
        input_description.send_keys(description_expected)
        time.sleep(1)

        check_box = self.driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div.form-group.container > div > div:nth-child(6) > input[type=checkbox]")
        check_box.click()

        update_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        update_btn.click()
        time.sleep(1)

        alert_error = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_error.is_displayed(), "Phát hiện lỗi thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường quyền không được bỏ trống."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_existed_role_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/3/edit")
        name_expected = "Supper Admin"

        input_name = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_name.clear()
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_description = self.driver.find_element(By.CSS_SELECTOR,
                                                     "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(4) > input")
        input_description.clear()
        input_description.send_keys(description_expected)
        time.sleep(1)

        update_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        update_btn.click()
        time.sleep(1)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR,
                                            "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Thông báo không được hiển thị thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Dữ liệu đã tồn tại trong hệ thống"

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_no_name(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/3/edit")
        name_expected = ""

        input_name = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_name.clear()
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_description = self.driver.find_element(By.CSS_SELECTOR,
                                                     "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(4) > input")
        input_description.clear()
        input_description.send_keys(description_expected)
        time.sleep(1)

        update_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        update_btn.click()
        time.sleep(1)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR,
                                            "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Thông báo không được hiển thị thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được bỏ trống."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"

    def test_update_name_special_characters(self, setup):
        self.driver.get("http://127.0.0.1:8000/admin/role/3/edit")
        name_expected = "#@!@$#@"

        input_name = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(3) > input")
        input_name.clear()
        input_name.send_keys(name_expected)
        time.sleep(1)

        description_expected = "Demo role"
        input_description = self.driver.find_element(By.CSS_SELECTOR,
                                                     "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > div:nth-child(4) > input")
        input_description.clear()
        input_description.send_keys(description_expected)
        time.sleep(1)

        update_btn = self.driver.find_element(By.CSS_SELECTOR,
                                              "#app > div > div.main-content > section > div.section-body.container > div > div > div > div.card-body.container > form > button")
        update_btn.click()
        time.sleep(1)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR,
                                            "body > div.swal2-container.swal2-top-end.swal2-backdrop-show > div")

        assert alert_sc.is_displayed(), "Thông báo không được hiển thị thành công"

        message_actual = self.driver.find_element(By.CSS_SELECTOR, "h2.swal2-title")
        message_expected = "Trường tên không được có ký tự đặc biệt."

        assert message_actual.text == message_expected, "Khởi tạo không như mong đợi"








