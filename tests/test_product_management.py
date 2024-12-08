import sys
sys.path.append("E:\Testing Subject")
import time
from mydriver.mydriver import Driver
from pages.login_page import LoginPage
from pages.product_management_page import ProductManagementPage

class TestProductManagement(Driver):
    def test_search_for_exact_product_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.search_product("Tri Ân Thầy Cô 2")
        time.sleep(1)
        assert "Tri Ân Thầy Cô 2" in driver.page_source
    
    def test_search_by_keyword_product_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.search_product("29")
        time.sleep(1)
        assert "29" in driver.page_source

    def test_search_with_special_characters(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.search_product("**%%**")
        time.sleep(1)
        assert "Không có dữ liệu" in driver.page_source

    def test_search_name_with_space(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.search_product("  Tri Ân Thầy Cô 2  ")
        time.sleep(1)
        assert "Tri Ân Thầy Cô 2" in driver.page_source

    def test_search_name_with_uppercase(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.search_product("TRI ÂN THẦY CÔ 2")
        time.sleep(1)
        assert "Tri Ân Thầy Cô 2" in driver.page_source

    def test_search_name_with_lowercase(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.search_product("tri ân thầy cô 2")
        time.sleep(1)
        assert "Tri Ân Thầy Cô 2" in driver.page_source

    def test_add_product_success(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("test1", "290000", "100", "cà phê", "cà phê")
        time.sleep(1)
        success_message = product_management_page.get_success_message()
        assert success_message == "Khởi tạo dữ liệu thành công"

    def test_add_product_with_empty_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("", "290000", "100", "cà phê", "cà phê")
        time.sleep(1)
        warning_message = product_management_page.get_warning_name_message()
        assert warning_message == "Trường tên không được bỏ trống."

    def test_add_product_with_empty_price(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("test", "", "100", "cà phê", "cà phê")
        time.sleep(1)
        warning_message = product_management_page.get_warning_name_message()
        assert warning_message == "Trường giá không được bỏ trống."

    def test_add_product_with_empty_vol(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("test", "290000", "", "cà phê", "cà phê")
        time.sleep(1)
        warning_message = product_management_page.get_warning_name_message()
        assert warning_message == "Trường khối lượng không được bỏ trống."

    def test_add_product_with_empty_description(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("test", "290000", "100", "", "cà phê")
        time.sleep(1)
        warning_message = product_management_page.get_warning_name_message()
        assert warning_message == "Trường mô tả không được bỏ trống."

    def test_add_product_with_empty_content(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("test", "290000", "100", "cà phê", "")
        time.sleep(1)
        warning_message = product_management_page.get_warning_name_message()
        assert warning_message == "Trường nội dung không được bỏ trống."

    def test_add_product_with_exist_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("Tri Ân Thầy Cô 2", "290000", "100", "cà phê", "cà phê")
        time.sleep(1)
        assert "Duplicate entry" in driver.page_source

    def test_add_product_with_special_characters_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("%%&&", "290000", "100", "cà phê", "cà phê")
        time.sleep(1)
        warning_message = product_management_page.get_warning_message()
        assert warning_message == "Trường tên không được chứa ký tự đặc biệt."

    def test_delete_product(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.delete_product()
        time.sleep(1)
        success_message = product_management_page.get_success_message()
        assert success_message == "Xóa thành công!"

    def test_update_success_product(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.navigate_to_update_product()
        product_management_page.fill_form_update_product("demo")
        time.sleep(1)
        success_message = product_management_page.get_success_message()
        assert success_message == "Cập nhật dữ liệu thành công!"

    def test_update_empty_name_product(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.navigate_to_update_product()
        product_management_page.fill_form_update_product("")
        time.sleep(1)
        warning_message = product_management_page.get_warning_message()
        assert warning_message == "Trường tên không được bỏ trống."

    def test_update_exist_name_product(self, driver):
        login_page = LoginPage(driver)  
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.navigate_to_update_product()
        product_management_page.fill_form_update_product("Tri Ân Thầy Cô 2")
        time.sleep(1)
        assert "Duplicate entry" in driver.page_source

    def test_update_special_characters_product(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "123")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.navigate_to_update_product()
        product_management_page.fill_form_update_product("**%%**")
        warning_message = product_management_page.get_warning_message()
        assert warning_message == "Trường tên không được chứa ký tự đặc biệt."