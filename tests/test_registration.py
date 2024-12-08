import sys
sys.path.append("E:\Testing Subject")
import time
from mydriver.mydriver import Driver
from pages.registration_page import RegistrationPage

class TestRegistration(Driver):
    """Test chức năng registration."""
    #Đăng ký thành công
    def test_registration_success(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.navigate_to_registration_page()
        registration_page.fill_registration_form("test2@gmail.com", "0123456789", "12345678", "12345678", "test")
        registration_page.close_registration_form()
        success_message = registration_page.get_success_message()
        assert success_message == "Đăng nhập thành công"
        registration_page.close_alert()
        time.sleep(3)
    
    #Đăng ký với email đã tồn tại, hệ thống hiển thị thông báo "Trường email đã có trong cơ sở dữ liệu."
    def test_registration_email_exist(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.navigate_to_registration_page()
        registration_page.fill_registration_form("user@gmail.com", "0123456789", "12345678", "12345678", "test")
        warning_message = registration_page.get_warning_email_message()
        assert warning_message == "Trường email đã có trong cơ sở dữ liệu."

    #Đăng ký với email trống, hệ thống hiển thị thông báo "Trường email không được bỏ trống."
    def test_registration_empty_email(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.navigate_to_registration_page()
        registration_page.fill_registration_form("", "0123456789", "12345678", "12345678", "test")
        warning_message = registration_page.get_warning_email_message()
        assert warning_message == "Trường email không được bỏ trống."

    #Đăng ký với số điện thoại không hợp lệ, hệ thống hiển thị thông báo "Trường số điện thoại có định dạng không hợp lệ."
    def test_registration_invalid_phone(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.navigate_to_registration_page()
        registration_page.fill_registration_form("test3@gmail.com", "123", "12345678", "12345678", "test")
        warning_message = registration_page.get_warning_phone_message()
        assert warning_message == "Trường số điện thoại có định dạng không hợp lệ."


    #Đăng ký với mật khẩu xác nhận không khớp, hệ thống hiển thị thông báo "Giá trị xác nhận trong trường mật khẩu không khớp."
    def test_registration_confirm_password_not_match(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.navigate_to_registration_page()
        registration_page.fill_registration_form("test4@gmail.com", "0123456789", "12345678", "012345678", "test")
        warning_message = registration_page.get_warning_password_message()
        assert warning_message == "Giá trị xác nhận trong trường mật khẩu không khớp."

    #Đăng ký với mật khẩu quá ngắn, hệ thống hiển thị thông báo "Trường mật khẩu phải có tối thiểu 8 kí tự."
    def test_registration_password_too_short(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.navigate_to_registration_page()
        registration_page.fill_registration_form("test5@gmail.com", "0123456789", "123", "123", "test")
        warning_message = registration_page.get_warning_password_message()
        assert warning_message == "Trường mật khẩu phải có tối thiểu 8 kí tự."

    #Đăng ký với tên đăng nhập trống, hệ thống hiển thị thông báo "Trường tên không được bỏ trống."
    def test_registration_empty_username(self, driver):
        registration_page = RegistrationPage(driver)
        registration_page.navigate_to_registration_page()
        registration_page.fill_registration_form("test6@gmail.com", "0123456789", "12345678", "12345678", "")
        warning_message = registration_page.get_warning_username_message()
        assert warning_message == "Trường tên không được bỏ trống."

    