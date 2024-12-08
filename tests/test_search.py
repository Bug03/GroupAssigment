import random
import time

import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from urllib.parse import unquote

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSearchFunction:

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request):
        driver = webdriver.Chrome()
        driver.maximize_window()
        request.cls.driver = driver
        yield
        driver.quit()

    def format_string(self, input_str):
        words = input_str.split()
        filtered_words = [word for word in words if not word.isdigit()]
        if len(filtered_words) <= 1:
            return "".join(filtered_words)
        return "+".join(filtered_words)

    def test_search_exactly_name(self, setup_class):
        keyword = "Bộ Quà Tặng Trung Nguyên Legend 27"

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        search_icon = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(3)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        decoded_url = unquote(self.driver.current_url)
        assert "search="+ self.format_string(keyword) in decoded_url, "URL không chứa `search=7`"

        products = self.driver.find_elements(By.CLASS_NAME, "item")

        assert len(products) > 0, "Không có sản phẩm nào hiển thị"

        for product in products:
            product_name = product.find_element(By.CLASS_NAME,"quickView").text.lower()
            assert keyword.lower() in product_name, f"Sản phẩm không chứa `7`: {product_name}"

    def test_search_keyword(self, setup_class):
        keyword = "7"

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        search_icon = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(3)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        decoded_url = unquote(self.driver.current_url)
        assert "search="+ self.format_string(keyword) in  decoded_url, "URL không chứa `search=7`"

        products = self.driver.find_elements(By.CLASS_NAME, "item")

        assert len(products) > 0, "Không có sản phẩm nào hiển thị"

        for product in products:
            product_name = product.find_element(By.CLASS_NAME,"quickView").text.lower()
            assert keyword.lower() in product_name, f"Sản phẩm không chứa `7`: {product_name}"

    def test_search_empty_keyword(self, setup_class):
        keyword = ""

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(2)

        search_icon = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(2)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

        decoded_url = unquote(self.driver.current_url)
        assert "search= " not in decoded_url, "URL vẫn chứa chứa `search= `"

        products = self.driver.find_elements(By.CLASS_NAME, "item")
        assert len(products) > 0, "Không có sản phẩm hiển thị"

    def test_search_keyword_contain_special_characters(self):
        keyword = "Bộ Quà Tặng Trung Nguyên Legend 27"
        special_characters = "@#$"
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(2)

        search_icon = self.driver.find_element(By.CSS_SELECTOR, "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(2)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword + " " + special_characters)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

        decoded_url = unquote(self.driver.current_url)
        assert "search="+ self.format_string(keyword) in decoded_url, "URL vẫn chứa chứa search="+ keyword + " " + special_characters

        products = self.driver.find_elements(By.CLASS_NAME, "item")
        assert len(products) > 0, "Không có sản phẩm nào hiển thị"

        for product in products:
            product_name = product.find_element(By.CLASS_NAME, "quickView").text
            assert keyword.lower() in product_name.lower(), f"Sản phẩm không chứa từ khóa " + keyword

    def test_search_special_characters(self, setup_class):
        #keyword = "Bộ Quà Tặng Trung Nguyên Legend 27"
        special_characters = "@#$"
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(2)

        search_icon = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(2)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(special_characters)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

        decoded_url = unquote(self.driver.current_url)
        assert "search="+ self.format_string(special_characters)  in decoded_url, "URL vẫn chứa chứa search="+special_characters

        products = self.driver.find_elements(By.CLASS_NAME, "item")
        assert len(products) <= 0, "Không có sản phẩm nào hiển thị"

    def test_lower_product(self, setup_class):
        keyword = "Bộ Quà Tặng Trung Nguyên Legend 27".lower()
        param_string = keyword.lower()
        param_string = param_string.replace(" ", "+")

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        search_icon = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(3)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        decoded_url = unquote(self.driver.current_url)
        assert "search="+ self.format_string(keyword) in decoded_url, "URL không chứa search=" +  param_string

        products = self.driver.find_elements(By.CLASS_NAME, "item")

        assert len(products) > 0, "Không có sản phẩm nào hiển thị"

        for product in products:
            product_name = product.find_element(By.CLASS_NAME, "quickView").text.lower()
            assert keyword.lower() in product_name.lower(), f"Sản phẩm không chứa: {keyword}"

    def test_upper_product(self, setup_class):
        keyword = "Bộ Quà Tặng Trung Nguyên Legend 27".upper()
        param_string = keyword.upper()
        param_string = param_string.replace(" ", "+")

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        search_icon = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(3)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        decoded_url = unquote(self.driver.current_url)
        assert "search="+ self.format_string(keyword) in decoded_url, "URL không chứa search=" +  param_string

        products = self.driver.find_elements(By.CLASS_NAME, "item")

        assert len(products) > 0, "Không có sản phẩm nào hiển thị"

        for product in products:
            product_name = product.find_element(By.CLASS_NAME, "quickView").text.lower()
            assert keyword.lower() in product_name.lower(), f"Sản phẩm không chứa: {keyword}"

    def test_surround_space_product(self, setup_class):
        keyword = " Bộ Quà Tặng Trung Nguyên Legend 27 "
        param_string = keyword.strip()
        param_string = param_string.replace(" ", "+")

        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        search_icon = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(3)

        search_box = self.driver.find_element(By.CSS_SELECTOR, "#searchTerm")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        decoded_url = unquote(self.driver.current_url)
        assert "search="+ self.format_string(param_string) in decoded_url, "URL không chứa search=" +  param_string

        products = self.driver.find_elements(By.CLASS_NAME, "item")

        assert len(products) > 0, "Không có sản phẩm nào hiển thị"

        for product in products:
            product_name = product.find_element(By.CLASS_NAME, "quickView").text.lower()
            assert keyword.lower().strip() in product_name.lower(), f"Sản phẩm không chứa: {keyword}"

    def test_filter_category(self, setup_class):
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        search_icon = self.driver.find_element(By.CSS_SELECTOR,
                                               "body > div.header.header-sticky > div > div > div > div.col-lg-4.col-md-4.col-sm-5.col-5 > div.general_head_right > ul > li:nth-child(3) > a")
        search_icon.click()
        time.sleep(3)

        categories = [
            {"value": "ca-phe-dong-goi", "expected_text": "TRI ÂN THẦY CÔ"},
            {"value": "qua-tang-cao-cap", "expected_text": "BỘ QUÀ TẶNG TRUNG NGUYÊN"},
            {"value": "vat-pham-ban-le", "expected_text": "PHIN NHÔM VĨ NHÂN"}
        ]

        random_category = random.choice(categories)

        category_dropdown = self.driver.find_element(By.NAME, "categorySlug")
        select = Select(category_dropdown)
        select.select_by_value(random_category["value"])

        time.sleep(5)

        products = self.driver.find_elements(By.CSS_SELECTOR,
                                             "body > section > div > div.row.align-items-center > div:nth-child(2) > div > form > div > div.woo_title > h4 > a")

        for product in products:
            product_name = product.text
            assert random_category["expected_text"] in product_name, f"Sản phẩm '{product_name}' bao hàm '{random_category['expected_text']}'"







