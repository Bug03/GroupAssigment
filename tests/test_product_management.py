import sys
sys.path.append("D:/myproject/test/coffee_testing")
import time
from mydriver.mydriver import Driver
from pages.login_page import LoginPage
from pages.product_management_page import ProductManagementPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestProductManagement(Driver):
    def test_search_for_exact_product_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
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

    def test_add_product_and_check_in_list(self, driver):
        # Đăng nhập vào hệ thống
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        
        # Điều hướng đến trang thêm sản phẩm
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        
        # Thêm sản phẩm mới
        product_management_page.fill_form_add_product("tui3", "290000", "100", "cà phê", "cà phê")
        time.sleep(1)
        
        # Kiểm tra thông báo thành công
        success_message = product_management_page.get_success_message()
        assert success_message == "Khởi tạo dữ liệu thành công"
        
        # Điều hướng đến danh sách sản phẩm
        product_management_page.navigate_to_product_list_page()
        time.sleep(2)
    
        product_management_page.navigate_to_last_page()
        time.sleep(2)

        # Kiểm tra nếu sản phẩm mới có trong danh sách sản phẩm
        product_list = product_management_page.get_product_list()
        assert "tui3" in product_list, "Sản phẩm vừa tạo không có trong danh sách."

    def test_add_product_invalid_format(self, driver):
        # Đăng nhập vào hệ thống
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)

        # Điều hướng đến trang thêm sản phẩm
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()

        # Trường hợp kiểm tra
        invalid_inputs = [
            {"product_name": "test1", "price": "abc", "weight": "100", "expected_error": "Trường giá phải là một số nguyên."},
            {"product_name": "test2", "price": "-100", "weight": "100","expected_error": "Trường giá phải tối thiểu là 1."},
            {"product_name": "test3", "price": "0", "weight": "100", "expected_error": "Trường giá phải tối thiểu là 1."},
            {"product_name": "test4", "price": "%%%%", "weight": "100", "expected_error": "Trường giá phải là một số nguyên."},
            {"product_name": "test5", "price": "290000", "weight": "-100", "expected_error": "Trường khối lượng phải tối thiểu là 1."},
            {"product_name": "test6", "price": "290000", "weight": "0", "expected_error": "Trường khối lượng phải tối thiểu là 1."},
        ]

        for inputs in invalid_inputs:
            # Điền form với dữ liệu không hợp lệ
            product_management_page.fill_form_add_product(
                inputs["product_name"], 
                inputs["price"], 
                inputs["weight"],
                "test content", 
                "test description"
            )
            time.sleep(2)
            # Lấy thông báo lỗi
            error_message = product_management_page.get_success_message()
            
            # Kiểm tra thông báo lỗi khớp với mong đợi
            assert error_message == inputs["expected_error"], f"Lỗi không đúng mong đợi: {inputs['expected_error']}"

            # Reset hoặc điều hướng lại nếu cần
            driver.get("http://127.0.0.1:8000/admin/product/create")

    def test_add_product_invalid_weight(self, driver):
        # Bước 1: Đăng nhập
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()

        # Bước 2: Điều hướng đến trang thêm sản phẩm
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        
        # Bước 3: Tìm ô input "Giá tiền"
        weight_input = driver.find_element(By.CSS_SELECTOR, "#app > div > div.main-content > section > div.section-body > div > div > div > div.card-body > form > div:nth-child(6) > input")
        
        # Bước 4: Nhập dữ liệu không hợp lệ (text thay vì số)
        weight_input.clear()
        weight_input.send_keys("e")  # Nhập chuỗi không hợp lệ
        weight_input.send_keys(Keys.TAB)  # Chuyển focus để trigger validation

        # Bước 5: Lấy thông báo lỗi từ trình duyệt
        validation_message = driver.execute_script("return arguments[0].validationMessage;", weight_input)

        # Bước 6: Kiểm tra thông báo
        assert validation_message == "Please enter a number.", \
            f"Expected 'Please enter a number.', but got '{validation_message}'"

    def test_add_product_with_empty_form(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()

        invalid_inputs = [
            {"product_name": "", "price": "290000", "weight": "100", "content": "test content", "description": "test description","expected_error": "Trường tên không được bỏ trống."},
            {"product_name": "test1", "price": "", "weight": "100", "content": "test content", "description": "test description","expected_error": "Trường giá không được bỏ trống."},
            {"product_name": "test2", "price": "290000", "weight": "", "content": "test content", "description": "test description","expected_error": "Trường khối lượng không được bỏ trống."},
            {"product_name": "test3", "price": "290000", "weight": "100", "content": "", "description": "test description","expected_error": "Trường mô tả không được bỏ trống."},
            {"product_name": "test4", "price": "290000", "weight": "100", "content": "test content", "description": "","expected_error": "Trường nội dung không được bỏ trống."},
        ]

        for inputs in invalid_inputs:
            # Điền form với dữ liệu không hợp lệ
            product_management_page.fill_form_add_product(
                inputs["product_name"], 
                inputs["price"], 
                inputs["weight"],
                inputs["content"], 
                inputs["description"]
            )
            time.sleep(2)
            # Lấy thông báo lỗi
            error_message = product_management_page.get_success_message()
            
            # Kiểm tra thông báo lỗi khớp với mong đợi
            assert error_message == inputs["expected_error"], f"Lỗi không đúng mong đợi: {inputs['expected_error']}"

            # Reset hoặc điều hướng lại nếu cần
            driver.get("http://127.0.0.1:8000/admin/product/create")


    def test_add_product_with_exist_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_add_product_page()
        product_management_page.fill_form_add_product("Tri Ân Thầy Cô 2", "290000", "100", "cà phê", "cà phê")
        time.sleep(1)
        assert "Trường tên đã có trong cơ sở dữ liệu" in driver.page_source

    def test_add_product_with_special_characters_name(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.navigate_to_update_product()
        product_management_page.fill_form_update_product("Tri Ân Thầy Cô", "", "", "", "")
        time.sleep(1)
        success_message = product_management_page.get_success_message()
        assert success_message == "Cập nhập dữ liệu thành công!"

        # Điều hướng đến danh sách sản phẩm
        product_management_page.navigate_to_product_list_page()
        time.sleep(2)
        
        # Kiểm tra nếu sản phẩm mới có trong danh sách sản phẩm
        product_list = product_management_page.get_product_list()
        assert "Tri Ân Thầy Cô" in product_list, "Sản phẩm vừa cập nhật không có trong danh sách."

    def test_update_empty_name_product(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
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
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.navigate_to_update_product()
        product_management_page.fill_form_update_product("Tri Ân Thầy Cô 2")
        time.sleep(1)
        assert "Trường tên đã có trong cơ sở dữ liệu." in driver.page_source

    def test_update_special_characters_product(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("admin@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        product_management_page = ProductManagementPage(driver)
        product_management_page.navigate_to_product_page()
        product_management_page.navigate_to_update_product()
        product_management_page.fill_form_update_product("**%%**")
        warning_message = product_management_page.get_warning_message()
        assert warning_message == "Trường tên không được chứa ký tự đặc biệt."