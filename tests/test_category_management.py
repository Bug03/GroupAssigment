import sys
sys.path.append("E:\Testing Subject")
import time
from mydriver.mydriver import Driver
from pages.login_page import LoginPage
from pages.category_management_page import CategoryManagementPage

class TestCategoryManagement(Driver):
    def test_search_for_exact_category_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.search_category("Cà phê đóng gói")
        time.sleep(1)
        assert "Cà phê đóng gói" in driver.page_source
    
    def test_search_by_keyword_category_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.search_category("v")
        time.sleep(1)
        assert "V" in driver.page_source

    def test_search_with_special_characters(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.search_category("**%%**")
        time.sleep(1)
        assert "Không có dữ liệu" in driver.page_source

    def test_search_name_with_space(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.search_category("  Cà phê đóng gói  ")
        time.sleep(1)
        assert "Cà phê đóng gói" in driver.page_source

    def test_search_name_with_uppercase(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.search_category("CÀ PHÊ ĐÓNG GÓI")
        time.sleep(1)
        assert "Cà Phê đóng gói" in driver.page_source

    def test_search_name_with_lowercase(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.search_category("cà phê đóng gói")
        time.sleep(1)
        assert "Cà Phê đóng gói" in driver.page_source

    def test_add_category_success(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_add_category_page()
        category_management_page.fill_form_add_category("Trái cây")
        time.sleep(1)
        success_message = category_management_page.get_success_message()
        assert success_message == "Khởi tạo dữ liệu thành công"

    def test_add_category_empty_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_add_category_page()
        category_management_page.fill_form_add_category("")
        time.sleep(1)
        warning_message = category_management_page.get_warning_message()
        assert warning_message == "Trường tên không được bỏ trống."

    def test_add_category_exist_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_add_category_page()
        category_management_page.fill_form_add_category("Cà phê đóng gói")
        time.sleep(1)
        assert "Duplicate entry" in driver.page_source

    def test_add_category_special_characters(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_add_category_page()
        category_management_page.fill_form_add_category("**%%**")
        warning_message = category_management_page.get_warning_message()
        assert warning_message == "Trường tên không được chứa ký tự đặc biệt."

    def test_delete_category(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.delete_category()
        time.sleep(1)
        success_message = category_management_page.get_success_message()
        assert success_message == "Xóa thành công!"
    
    def test_update_success_category(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.navigate_to_update_category()
        category_management_page.fill_form_update_category("demo")
        time.sleep(1)
        success_message = category_management_page.get_success_message()
        assert success_message == "Cập nhật dữ liệu thành công!"

    def test_update_empty_name_category(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.navigate_to_update_category()
        category_management_page.fill_form_update_category("")
        time.sleep(1)
        warning_message = category_management_page.get_warning_message()
        assert warning_message == "Trường tên không được bỏ trống."

    def test_update_exist_name_category(self, driver):
        login_page = LoginPage(driver)  
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.navigate_to_update_category()
        category_management_page.fill_form_update_category("Cà phê đóng gói")
        time.sleep(1)
        assert "Duplicate entry" in driver.page_source

    def test_update_special_characters_category(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        category_management_page = CategoryManagementPage(driver)
        category_management_page.navigate_to_category_page()
        category_management_page.navigate_to_update_category()
        category_management_page.fill_form_update_category("**%%**")
        warning_message = category_management_page.get_warning_message()
        assert warning_message == "Trường tên không được chứa ký tự đặc biệt."




    
    
    
                                   