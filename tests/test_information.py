import sys
sys.path.append("E:\Testing Subject")
import time
from mydriver.mydriver import Driver
from pages.login_page import LoginPage
from pages.information_page import InformationPage

class TestInformation(Driver):
    """Test chức năng quản lý (cập nhật) thông tin tài khoản"""
    def test_change_password_success(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "12345678")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_password_form("12345678", "11111111", "11111111")
        success_message = information_page.get_success_message()
        assert success_message == "Cập nhập thành công"
        time.sleep(1)
    
    def test_change_password_too_short(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_password_form("11111111", "1234", "1234")
        warning_message = information_page.get_warning_password_message()
        assert warning_message == "Trường mật khẩu phải có tối thiểu 8 kí tự."
        time.sleep(1)

    def test_change_password_not_match(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_password_form("11111111", "12345678", "012345678")
        warning_message = information_page.get_warning_password_message()
        assert warning_message == "Giá trị xác nhận trong trường mật khẩu không khớp."
        time.sleep(1)

    def test_invalid_old_password(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_password_form("1234", "12345678", "12345678")
        warning_message = information_page.get_waning_old_password_message()
        assert warning_message == "Mật khẩu không đúng."

    def test_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_password_form("", "", "")
        warning_message = information_page.get_warning_old_password_message()
        warning_message1 = information_page.get_warning_password_message()
        assert warning_message == "Trường mật khẩu hiện tại không được bỏ trống."
        assert warning_message1 == "Trường mật khẩu không được bỏ trống."

    def test_update_phone_success(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_info_form("Người dùng", "user@gmail.com", "0123456789")
        time.sleep(2)
        success_message = information_page.get_success_message()
        assert success_message == "Cập nhật thành công"
        time.sleep(1)

    def test_update_empty_phone(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_info_form("Người dùng", "user@gmail.com", "")
        warning_message = information_page.get_warning_phone_message()
        assert warning_message == "Trường số điện thoại phải là một số."

    def test_update_invalid_phone(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        information_page = InformationPage(driver)
        information_page.navigate_to_information_page()
        information_page.fill_info_form("Người dùng", "user@gmail.com", "0")
        warning_message = information_page.get_warning_phone_message()
        assert warning_message == "Trường số điện thoại không hợp lệ."
