import sys
sys.path.append("E:\Testing Subject")
import time
from mydriver.mydriver import Driver
from pages.navigation_page import NavigationPage

class TestNavigation(Driver):
    """Test chức năng Navigation điều hướng."""
    # #Điều hướng tới trang cà phê đóng gói
    def test_navigation_to_coffee(self, driver):
        navigation_page = NavigationPage(driver)
        navigation_page.navigate_to_category()
        navigation_page.navigate_to_coffee()
        time.sleep(3)
        expected_url = "http://127.0.0.1:8000/product?category=ca-phe-dong-goi"
        assert driver.current_url == expected_url

    #Điều hướng tới trang quà tặng cao cấp
    def test_navigation_to_gift(self, driver):
        navigation_page = NavigationPage(driver)
        navigation_page.navigate_to_category()
        navigation_page.navigate_to_gift()
        time.sleep(3)
        expected_url = "http://127.0.0.1:8000/product?category=qua-tang-cao-cap"
        assert driver.current_url == expected_url

    #Điều hướng tới trang vật phẩm bán lẻ
    def test_navigation_to_prescription(self, driver):
        navigation_page = NavigationPage(driver)
        navigation_page.navigate_to_category()
        navigation_page.navigate_to_prescription()
        time.sleep(3)
        expected_url = "http://127.0.0.1:8000/product?category=vat-pham-ban-le"
        assert driver.current_url == expected_url

    #Điều hướng tới trang tất cả sản phẩm
    def test_navigation_to_all_products(self, driver):
        navigation_page = NavigationPage(driver)
        navigation_page.navigate_to_category()
        navigation_page.navigate_to_all_products()
        time.sleep(3)
        expected_url = "http://127.0.0.1:8000/product"
        assert driver.current_url == expected_url
    


        
