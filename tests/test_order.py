import sys
sys.path.append("E:\Testing Subject")
import time
from mydriver.mydriver import Driver
from pages.login_page import LoginPage
from pages.order_page import OrderPage

class TestOrder(Driver):
    def test_search_order_with_exact_phone(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        order_page = OrderPage(driver)
        order_page.navigate_to_order_page()
        order_page.search_phone_order("0937237984")
        assert "0937237984" in driver.page_source

    def test_search_order_with_keyword_phone(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        order_page = OrderPage(driver)
        order_page.navigate_to_order_page()
        order_page.search_phone_order("093")
        assert "093" in driver.page_source

    def test_search_order_with_special_characters(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        order_page = OrderPage(driver)
        order_page.navigate_to_order_page()
        order_page.search_phone_order("%%%")
        assert "Không có dữ liệu" in driver.page_source

    def test_search_order_with_space(self, driver):
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.fill_login_form("user@gmail.com", "11111111")
        login_page.close_alert()
        time.sleep(3)
        order_page = OrderPage(driver)
        order_page.navigate_to_order_page()
        order_page.search_phone_order(" 0937237984 ")
        assert "0937237984" in driver.page_source

    

    