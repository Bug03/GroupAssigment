import time
import random
import re

import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAddToCart:
    """Test chức năng Add to Cart."""

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

        username_field.send_keys("user@gmail.com")
        password_field.send_keys("123")

        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "#loginAcc")
        submit_btn.click()
        time.sleep(1)

        sc_btn = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled")
        sc_btn.click()
        time.sleep(3)

    def get_random_product(self, length=None):
        product_names = [
            "Phin Nhôm Vĩ Nhân 11",
            "Phin Nhôm Vĩ Nhân 12",
            "Phin Nhôm Vĩ Nhân 15",
            "Phin Nhôm Vĩ Nhân 17",
            "Phin Nhôm Vĩ Nhân 19",
            "Phin Nhôm Vĩ Nhân 11",
            "Phin Nhôm Vĩ Nhân 20",
            "Phin Nhôm Vĩ Nhân 25",
            "Phin Nhôm Vĩ Nhân 29",
            "Phin Nhôm Vĩ Nhân 0"
        ]

        if length is None:
            return random.choice(product_names)
        else:

            return random.sample(product_names, min(length, len(product_names)))

    def search(self, keyword):
        time.sleep(3)
        search_icon = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(4) > a")
        search_icon.click()
        time.sleep(3)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

    def is_product_in_cart(self, product_name, expected_quantity):

        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_selected_single")


        for item in cart_items:
            product_title = item.find_element(By.CLASS_NAME, "product_title").text.strip()

            quantity_text = item.find_element(By.CLASS_NAME, "numberof_item").text.strip()
            quantity = int(quantity_text.split(":")[-1].strip())

            if product_title == product_name and quantity == expected_quantity:
                return True

        return False

    def clear_cart(self):
        try:

            cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_selected_single")

            while cart_items:

                delete_button = cart_items[0].find_element(By.CLASS_NAME, "btn-cart-del")
                delete_button.click()

                WebDriverWait(self.driver, 10).until(
                    EC.staleness_of(cart_items[0])
                )
                cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_selected_single")

        except Exception as e:
            print(f"Lỗi khi xóa sản phẩm: {e}")

    def test_add_one_product_to_cart(self, setup):
        expected_quantity = 1
        product = self.get_random_product()

        self.search(product)

        add_btn = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div.row.align-items-center > div > div > form > div > div.woo_price > a")
        self.driver.execute_script("arguments[0].scrollIntoView();", add_btn)
        time.sleep(1)
        add_btn.click()
        time.sleep(1)

        alert_sc = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-start.swal2-backdrop-show > div")
        time.sleep(1)

        assert alert_sc.is_displayed(), "Phần tử không hiển thị"

        self.driver.get("http://127.0.0.1:8000/cart")
        time.sleep(3)

        is_product_found = self.is_product_in_cart(product, expected_quantity)

        assert is_product_found, f"Sản phẩm '{product}' với số lượng {expected_quantity} không có trong giỏ hàng!"

        self.clear_cart()

    def test_add_multi_product_to_cart(self, setup):
        expected_quantity = random.randint(2, 6)
        product = self.get_random_product()
        for i in range(expected_quantity):
            self.search(product)

            add_btn = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div.row.align-items-center > div > div > form > div > div.woo_price > a")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_btn)
            time.sleep(1)
            add_btn.click()
            time.sleep(1)

            alert_sc = self.driver.find_element(By.CSS_SELECTOR, "body > div.swal2-container.swal2-top-start.swal2-backdrop-show > div")
            time.sleep(1)

            assert alert_sc.is_displayed(), "Phần tử không hiển thị"

            time.sleep(1)
            self.driver.get("http://127.0.0.1:8000/")

        self.driver.get("http://127.0.0.1:8000/cart")
        time.sleep(3)

        is_product_found = self.is_product_in_cart(product, expected_quantity)

        assert is_product_found, f"Sản phẩm '{product}' với số lượng {expected_quantity} không có trong giỏ hàng!"

        self.clear_cart()

    def test_add_different_product(self, setup):
        expected_quantity = 1
        random_products = self.get_random_product(3)
        for i in range(3):
            self.search(random_products[i])

            add_btn = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > section > div > div.row.align-items-center > div > div > form > div > div.woo_price > a")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_btn)
            time.sleep(1)
            add_btn.click()
            time.sleep(1)

            alert_sc = self.driver.find_element(By.CSS_SELECTOR,
                                                "body > div.swal2-container.swal2-top-start.swal2-backdrop-show > div")
            time.sleep(1)

            assert alert_sc.is_displayed(), "Phần tử không hiển thị"

            time.sleep(1)
            self.driver.get("http://127.0.0.1:8000/")

        self.driver.get("http://127.0.0.1:8000/cart")
        time.sleep(3)

        for i in range(3):
            is_product_found = self.is_product_in_cart(random_products[i], expected_quantity)
            assert is_product_found, f"Sản phẩm '{random_products[i]}' với số lượng {expected_quantity} không có trong giỏ hàng!"

        self.clear_cart()

    def test_add_invalid_quantiy(self, setup):

        invalid_qty = [0, "ankcndsk", 1000000]
        product = self.get_random_product()
        for i in range(3):
            self.search(product)

            product_link = self.driver.find_element(By.CSS_SELECTOR, "body > section > div > div.row.align-items-center > div > div > form > div > div.woo_title > h4 > a")
            self.driver.execute_script("arguments[0].scrollIntoView();", product_link)
            time.sleep(1)
            product_link.click()
            time.sleep(1)

            input_qty = self.driver.find_element(By.CSS_SELECTOR, "#view-product > div > div > div:nth-child(2) > form > div:nth-child(7) > div > input")
            input_qty.clear()
            input_qty.send_keys(invalid_qty[i])
            time.sleep(1)

            add_btn = self.driver.find_element(By.CSS_SELECTOR, "#addCart")
            add_btn.click()
            time.sleep(1)

            self.driver.get("http://127.0.0.1:8000/cart")
            alert_er = self.driver.find_elements(By.CSS_SELECTOR, "body > div.swal2-container.swal2-center.swal2-backdrop-show > div")
            assert len(alert_er) > 0, "Không tìm thấy alert!"

            time.sleep(1)
            self.driver.get("http://127.0.0.1:8000/")

    def test_compute_total(self, setup):
        random_products = self.get_random_product(3)
        list_expected_quantity = [random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)]
        for i in range(3):
            self.search(random_products[i])
            self.driver.find_element(By.XPATH, "/html/body/section/div/div[3]/div/div/form/div/div[1]/h4/a").click()
            time.sleep(2)
            ## update quantity
            quantity = list_expected_quantity[i]
            self.driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div/div/div[2]/form/div[4]/div/input").clear()
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[9]/div/div/div/div/div[2]/form/div[4]/div/input").send_keys(
                quantity)
            ## click button add to cart
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[9]/div/div/div/div/div[2]/form/div[5]/div/button").click()
            time.sleep(2)
            self.driver.get("http://127.0.0.1:8000/")

        self.driver.get("http://127.0.0.1:8000/cart")
        time.sleep(2)

        for i in range(3):
            is_product_found = self.is_product_in_cart(random_products[i], list_expected_quantity[i])
            assert is_product_found, f"Sản phẩm '{random_products[i]}' với số lượng {list_expected_quantity[i]} không có trong giỏ hàng!"

        prices = self.driver.find_elements(By.CSS_SELECTOR,
                                           "#cart > div.cart_select_items > div > div.cart_selected_single_caption > strong")

        quantities = self.driver.find_elements(By.CSS_SELECTOR,
                                               "#cart > div.cart_select_items > div > div.cart_selected_single_caption > span")

        total_expected = 0

        total_actual = self.driver.find_element(By.CSS_SELECTOR,
                                                "#cart > div.cart_subtotal.priceTotal > h6:nth-child(3) > span")

        total_actual = int(re.sub(r'[^\d]', '', total_actual.text))

        for i in range(len(prices)):
            price_text = prices[i].text
            price = int(re.sub(r'[^\d]', '', price_text))

            quantity_text = quantities[i].text
            quantity = int(re.sub(r'[^\d]', '', quantity_text))

            total_expected += price * quantity

        assert total_expected == total_actual, "Giá không bằng nhau"

        self.clear_cart()

    def test_compute_total_after_delete(self, setup):
        random_products = self.get_random_product(3)
        list_expected_quantity = [random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)]
        for i in range(3):
            self.search(random_products[i])
            self.driver.find_element(By.XPATH, "/html/body/section/div/div[3]/div/div/form/div/div[1]/h4/a").click()
            time.sleep(2)
            ## update quantity
            quantity = list_expected_quantity[i]
            self.driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div/div/div[2]/form/div[4]/div/input").clear()
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[9]/div/div/div/div/div[2]/form/div[4]/div/input").send_keys(
                quantity)
            ## click button add to cart
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[9]/div/div/div/div/div[2]/form/div[5]/div/button").click()
            time.sleep(2)
            self.driver.get("http://127.0.0.1:8000/")

        self.driver.get("http://127.0.0.1:8000/cart")
        time.sleep(2)

        for i in range(3):
            is_product_found = self.is_product_in_cart(random_products[i], list_expected_quantity[i])
            assert is_product_found, f"Sản phẩm '{random_products[i]}' với số lượng {list_expected_quantity[i]} không có trong giỏ hàng!"

        prices = self.driver.find_elements(By.CSS_SELECTOR,
                                           "#cart > div.cart_select_items > div > div.cart_selected_single_caption > strong")

        quantities = self.driver.find_elements(By.CSS_SELECTOR,
                                               "#cart > div.cart_select_items > div > div.cart_selected_single_caption > span")

        total_expected = 0

        total_actual = self.driver.find_element(By.CSS_SELECTOR,
                                                "#cart > div.cart_subtotal.priceTotal > h6:nth-child(3) > span")

        total_actual = int(re.sub(r'[^\d]', '', total_actual.text))

        for i in range(len(prices)):
            price_text = prices[i].text
            price = int(re.sub(r'[^\d]', '', price_text))

            quantity_text = quantities[i].text
            quantity = int(re.sub(r'[^\d]', '', quantity_text))

            total_expected += price * quantity

        assert total_expected == total_actual, "Giá không bằng nhau"

        delete_button = self.driver.find_element(By.CSS_SELECTOR, '#delItemCart')

        assert delete_button.is_displayed(), "Không tồn tại sản phẩm nào"

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",  delete_button)

        delete_button.click()

        time.sleep(2)

        prices = self.driver.find_elements(By.CSS_SELECTOR,
                                           "#cart > div.cart_select_items > div > div.cart_selected_single_caption > strong")

        quantities = self.driver.find_elements(By.CSS_SELECTOR,
                                               "#cart > div.cart_select_items > div > div.cart_selected_single_caption > span")

        total_expected = 0

        total_actual = self.driver.find_element(By.CSS_SELECTOR,
                                                "#cart > div.cart_subtotal.priceTotal > h6:nth-child(3) > span")

        total_actual = int(re.sub(r'[^\d]', '', total_actual.text))

        for i in range(len(prices)):
            price_text = prices[i].text
            price = int(re.sub(r'[^\d]', '', price_text))

            quantity_text = quantities[i].text
            quantity = int(re.sub(r'[^\d]', '', quantity_text))

            total_expected += price * quantity

        assert total_expected == total_actual, "Giá không bằng nhau"

        self.clear_cart()

    def test_add_product_with_random_quantity(self, setup):
        random_products = self.get_random_product(3)
        list_expected_quantity = [random.randint(2, 6), random.randint(2, 6), random.randint(2, 6)]
        for i in range(3):
            self.search(random_products[i])
            self.driver.find_element(By.XPATH, "/html/body/section/div/div[3]/div/div/form/div/div[1]/h4/a").click()
            time.sleep(2)
            ## update quantity
            quantity = list_expected_quantity[i]
            self.driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div/div/div[2]/form/div[4]/div/input").clear()
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[9]/div/div/div/div/div[2]/form/div[4]/div/input").send_keys(
                quantity)
            ## click button add to cart
            self.driver.find_element(By.XPATH,
                                     "/html/body/div[9]/div/div/div/div/div[2]/form/div[5]/div/button").click()
            time.sleep(2)
            self.driver.get("http://127.0.0.1:8000/")

        self.driver.get("http://127.0.0.1:8000/cart")
        time.sleep(2)

        for i in range(3):
            is_product_found = self.is_product_in_cart(random_products[i],list_expected_quantity[i])
            assert is_product_found, f"Sản phẩm '{random_products[i]}' với số lượng {list_expected_quantity[i]} không có trong giỏ hàng!"

        self.clear_cart()