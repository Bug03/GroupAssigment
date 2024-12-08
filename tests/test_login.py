import sys
sys.path.append("E:\Testing Subject")
import time
from mydriver.mydriver import Driver
from pages.login_page import LoginPage

class TestLogin(Driver):
    """Test chức năng Login."""
    def test_login_success(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "123")
        success_message = login_page.get_success_message()
        assert success_message == "Đăng nhập thành công"
        login_page.close_alert()
        time.sleep(3)

    def test_login_invalid_email(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user", "123")
        warning_message = login_page.get_warning_message()
        assert warning_message == "Trường email phải là một địa chỉ email hợp lệ."

    def test_login_invalid_password(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "invalidpass")
        warning_message = login_page.get_warning_message()
        assert warning_message == "Thông tin tài khoản không tìm thấy trong hệ thống."

    def test_login_email_not_exist(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail", "123")
        warning_message = login_page.get_warning_message()
        assert warning_message == "Thông tin tài khoản không tìm thấy trong hệ thống."

    def test_login_empty_email(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("", "123")
        warning_message = login_page.get_warning_message()
        assert warning_message == "Trường email không được bỏ trống."
    
    def test_login_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "")
        warning_message = login_page.get_warning_message_2()
        assert warning_message == "Trường mật khẩu không được bỏ trống."
        
    def test_logout(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        login_page.logout()
        success_message = login_page.success_logout()
        time.sleep(3)
        assert success_message == "Đăng xuất thành công"


