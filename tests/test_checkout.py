import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
from pypdf import PdfReader

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": os.getcwd(),  # Tải file về thư mục hiện tại
        "plugins.always_open_pdf_externally": True  # Mở file PDF bằng trình xem PDF mặc định
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def download_pdf(driver, order_id):
    # Điều hướng tới trang cần tải PDF
    driver.get(f"http://127.0.0.1:8000/orders/{order_id}")  # Thay URL phù hợp

    # # Chờ và click vào nút "Download PDF"
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.LINK_TEXT, "Download PDF"))
    # ).click()
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download PDF"))
        ).click()
    except:
        print("Không tìm thấy nút 'Download PDF'.")



    # # Chờ vài giây để file PDF được tải xuống
    # time.sleep(6)

def read_last_pdf_file_and_return_details():
    directory = r"E:\Testing Subject"
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")]

    if not files:
        raise Exception("Không tìm thấy file PDF nào.")
    
    # Đọc file PDF cuối cùng
    pdf = PdfReader(files[-1])
    details = {
        "thanh_tien": None,
        "phi_van_chuyen": None,
        "tong_cong": None
    }

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text is None:
            continue  # Bỏ qua trang nếu không có nội dung

        # Trích xuất thông tin "Thành tiền"
        if "Thành tiền :" in page_text:
            try:
                details["thanh_tien"] = page_text.split("Thành tiền :")[1].split("\n")[0].strip()
            except IndexError:
                raise Exception("Không tìm thấy thông tin 'Thành tiền' trong trang PDF.")
        
        # Trích xuất thông tin "Phí vận chuyển"
        if "Phí vận chuyển :" in page_text:
            try:
                details["phi_van_chuyen"] = page_text.split("Phí vận chuyển :")[1].split("\n")[0].strip()
            except IndexError:
                raise Exception("Không tìm thấy thông tin 'Phí vận chuyển' trong trang PDF.")
        
        # Trích xuất thông tin "Tổng cộng"
        if "Tổng cộng :" in page_text:
            try:
                details["tong_cong"] = page_text.split("Tổng cộng :")[1].split("\n")[0].strip()
            except IndexError:
                raise Exception("Không tìm thấy thông tin 'Tổng cộng' trong trang PDF.")
    
    # Kiểm tra nếu tất cả các thông tin đã được tìm thấy
    if not all(details.values()):
        raise Exception("Không đủ thông tin cần thiết trong file PDF.")
    
    return details


    
def add_random_product_to_cart(driver):
    """
    Thêm một sản phẩm ngẫu nhiên vào giỏ hàng
    """
    time.sleep(2)
    # Tìm danh sách các nút "Thêm vào giỏ hàng"
    add_cart_buttons = driver.find_elements(By.CLASS_NAME, "add-cart")

    if not add_cart_buttons:
        raise Exception("Không tìm thấy nút 'Thêm vào giỏ hàng' nào.")

    # Chọn ngẫu nhiên một sản phẩm
    random_button = random.choice(add_cart_buttons)

    # Cuộn đến phần tử để đảm bảo nó hiển thị
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_button)
    time.sleep(1)

    # Đảm bảo rằng phần tử có thể click
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "add-cart")))

    try:
        # Click vào nút thêm sản phẩm
        random_button.click()
        # Đợi một chút để sản phẩm được thêm vào giỏ hàng
        time.sleep(2)
    except Exception as e:
        raise Exception(f"Lỗi khi click vào nút 'Thêm vào giỏ hàng': {e}")

def is_cart_empty(driver):
    """
    Kiểm tra xem giỏ hàng có sản phẩm hay không
    """
    try:
        cart_quantity_element = driver.find_element(By.ID, "header-cart-quantity")
        cart_quantity = int(cart_quantity_element.text.strip())
        return cart_quantity == 0  # Trả về True nếu giỏ hàng trống
    except Exception:
        return True  # Nếu không tìm thấy phần tử, coi như giỏ hàng trống

def log_in(driver):
    """
    Đăng nhập vào hệ thống với thông tin hợp lệ
    """
    driver.find_element(By.CLASS_NAME, "dropdown-user").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "dropdown-item").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "emailAcc").send_keys("admin@gmail.com")
    driver.find_element(By.CLASS_NAME, "passwordAcc").send_keys("123")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button#loginAcc.btn.btn-md.btn-theme").click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "swal2-confirm").click()

def fill_checkout_form(driver, name, phone, email, province, district, ward, address):

    """
    Điền thông tin vào biểu mẫu thanh toán
    """
    time.sleep(3)
    cart_element = driver.find_element(By.XPATH, "//a[@class='border-icon' and .//span[@id='header-cart-quantity']]")
    time.sleep(1)
    cart_element.click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='name']").clear()
    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='name']").send_keys(name)

    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='phone']").clear()
    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='phone']").send_keys(phone)

    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='email']").clear()
    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='email']").send_keys(email)
    if province != '':
        # Chọn Tỉnh/Thành phố nếu được cung cấp
        Select(driver.find_element(By.CSS_SELECTOR, "select.input_search.province[name='province']")).select_by_visible_text(province)
        time.sleep(2)

        if district != '':
            # Chọn Quận/Huyện nếu được cung cấp
            Select(driver.find_element(By.CSS_SELECTOR, "select.input_search.district[name='district']")).select_by_visible_text(district)
            time.sleep(2)

            if ward != '':
                # Chọn Phường/Xã nếu được cung cấp
                Select(driver.find_element(By.CSS_SELECTOR, "select.input_search.ward[name='ward']")).select_by_visible_text(ward)
                time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='address']").clear()
    driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='address']").send_keys(address)
    

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)

# THT_01: Thông tin hợp lệ
def test_valid_checkout_information(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    time.sleep(2)
    ## scroll to total price
    scroll_to_element(driver, driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[2]/div[1]/div[1]/h6[2]/span"))         
    ## expect total price 
    expected_total_price = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[2]/div[1]/div[1]/h6[2]/span").text
    ## convert to int
    expected_total_price = int(expected_total_price.replace("đ", "").replace(".", "").strip())
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    time.sleep(2)
    success_message = driver.find_element(By.CSS_SELECTOR, "h2.swal2-title#swal2-title").text 
    driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled").click()
    
    # Sử dụng assert để kiểm tra thông báo
    assert success_message == "Thanh toán thành công", f"Expected: 'Thanh toán thành công', Found: '{success_message}'"
    time.sleep(2)
    # vào lịch sử đơn hàng so sánh tổng tiền
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[3]/div[1]/ul/li[1]/a").click()
    time.sleep(2)
    ## vô lịch sử đơn hàng
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[3]/div[1]/ul/li[1]/div/ul/li[3]").click()
    time.sleep(2)
    ## scroll to sort by date
    scroll_to_element(driver, driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/div[2]/div/div[2]/div/table/thead/tr/th[6]"))
    ## click sort by date 
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/div[2]/div/div[2]/div/table/thead/tr/th[6]").click()
    time.sleep(3)
    ## lấy tổng tiền đơn hàng đầu tiên
    total_price_element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/div[2]/div/div[2]/div/table/tbody/tr[2]/td[3]/span/div")
    actual_total_price = total_price_element.text
    assert expected_total_price == actual_total_price, f"Expected: '{expected_total_price}', Found: '{actual_total_price}'"
    

def test_valid_checkout_information_pdf(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    time.sleep(2)
    ## scroll to total price
    scroll_to_element(driver, driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[2]/div[1]/div[1]/h6[2]/span"))         
    ## lấy tổng đơn hàng, phí vận chuyển, tổng tiền
    expected_total_price = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[2]/div[1]/div[1]/h6[2]/span").text
    expected_shipping_fee = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[2]/div[1]/div[1]/div/h6/span").text
    expected_total_amount = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[2]/div[1]/div[1]/h6[1]/span").text
    # convert to int
    expected_total_price = int(expected_total_price.replace("đ", "").replace(".", "").strip())
    expected_shipping_fee = int(expected_shipping_fee.replace("đ", "").replace(".", "").strip())
    expected_total_amount = int(expected_total_amount.replace("đ", "").replace(".", "").strip())
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    time.sleep(2)
    success_message = driver.find_element(By.CSS_SELECTOR, "h2.swal2-title#swal2-title").text 
    driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled").click()
    
    # Sử dụng assert để kiểm tra thông báo
    assert success_message == "Thanh toán thành công", f"Expected: 'Thanh toán thành công', Found: '{success_message}'"
    time.sleep(2)
    # vào lịch sử đơn hàng so sánh tổng đơn hàng, phí vận chuyển, tổng tiền
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[3]/div[1]/ul/li[1]/a").click()
    time.sleep(2)
    ## vô lịch sử đơn hàng
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[3]/div[1]/ul/li[1]/div/ul/li[3]").click()
    time.sleep(2)
    ## scroll to sort by date
    scroll_to_element(driver, driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/div[2]/div/div[2]/div/table/thead/tr/th[6]"))
    ## click sort by date 
    driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/div[2]/div/div[2]/div/table/thead/tr/th[6]").click()
    time.sleep(3)
    ## lấy id đơn hàng đầu tiên
    order_id_element = driver.find_element(By.XPATH, "/html/body/section/div/div/div/div/div/div[2]/div/div[2]/div/table/tbody/tr[2]/td[1]")
    order_id = order_id_element.text
    ## download pdf
    # total_amount = download_and_read_pdf(driver, order_id)
    # print(total_amount)
    download_pdf(driver, order_id)
    # time.sleep(2)
    details = read_last_pdf_file_and_return_details()
    actual_total_amount = int(details["thanh_tien"])
    actual_shipping_fee = int(details["phi_van_chuyen"])
    actual_total_price = int(details["tong_cong"])

    assert expected_total_amount == actual_total_amount, f"Expected: '{expected_total_amount}', Found: '{actual_total_amount}'"
    assert expected_shipping_fee == actual_shipping_fee, f"Expected: '{expected_shipping_fee}', Found: '{actual_shipping_fee}'"
    assert expected_total_price == actual_total_price, f"Expected: '{expected_total_price}', Found: '{actual_total_price}'"

    time.sleep(10)


# THT_02: Họ tên vượt quá 255 ký tự
def test_name_exceeds_255_characters(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "A"*256, "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[1]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Trường tên không được lớn hơn 255 kí tự."
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"


# THT_03: Họ tên chứa ký tự đặc biệt
def test_name_contains_special_characters(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "@@Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[1]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Trường tên không được chứa kí tự đặc biệt."
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"

# THT_04: SĐT không đủ/chính xác 10 số
def test_phone_number_incorrect_length(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "01234", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[2]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Số điện thoại chỉ bao gồm 10 số"
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"

# THT_05: Email vượt quá 255 ký tự
def test_email_exceeds_255_characters(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "a" * 256 + "@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[3]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Trường email không được lớn hơn 255 kí tự."
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"

# THT_06: Email sai định dạng    
def test_email_invalid_format(driver):
    driver.get("http://127.0.0.1:8000/")  # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)

    # Điền thông tin với email sai định dạng
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "invalid-email-format", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    time.sleep(3)
    # Lấy phần tử input email
    email_input = driver.find_element(By.CSS_SELECTOR, "input.form-control.form-control-sm[name='email']")

    # Sử dụng JavaScript để kiểm tra tính hợp lệ và lấy thông báo lỗi
    is_valid = driver.execute_script("return arguments[0].checkValidity();", email_input)
    validation_message = driver.execute_script("return arguments[0].validationMessage;", email_input)

    # Kiểm tra assert
    assert not is_valid, "Expected the email field to be invalid, but it is valid."
    expected_message = "Please include an '@' in the email address. 'invalid-email-format' is missing an '@'."
    assert validation_message == expected_message, f"Expected: '{expected_message}', Found: '{validation_message}'"


# THT_07: Email bị bỏ trống
def test_email_empty(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[3]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Trường email không được bỏ trống."
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"

# THT_08: Bỏ trống Tỉnh/Thành phố
def test_province_empty(driver):
    driver.get("http://127.0.0.1:8000/")  # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)

    # Điền thông tin nhưng bỏ trống Tỉnh/Thành phố
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "", "", "", "123")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    time.sleep(3)
    # Lấy phần tử select của Tỉnh/Thành phố
    province_select = driver.find_element(By.CSS_SELECTOR, "select.input_search.province[name='province']")

    # Sử dụng JavaScript để kiểm tra tính hợp lệ và lấy thông báo lỗi
    is_valid = driver.execute_script("return arguments[0].checkValidity();", province_select)
    validation_message = driver.execute_script("return arguments[0].validationMessage;", province_select)

    # Kiểm tra assert
    assert not is_valid, "Expected the province field to be invalid, but it is valid."
    expected_message = "Please select an item in the list."
    assert validation_message == expected_message, f"Expected: '{expected_message}', Found: '{validation_message}'"

    
# THT_09: Bỏ trống Quận
def test_district_empty(driver):
    driver.get("http://127.0.0.1:8000/")  # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)

    # Điền thông tin nhưng Bỏ trống Quận
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "", "", "123")
    time.sleep(3)
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Lấy phần tử select của Tỉnh/Thành phố
    district_select = driver.find_element(By.CSS_SELECTOR, "select.input_search.district[name='district']")

    # Sử dụng JavaScript để kiểm tra tính hợp lệ và lấy thông báo lỗi
    is_valid = driver.execute_script("return arguments[0].checkValidity();", district_select)
    validation_message = driver.execute_script("return arguments[0].validationMessage;", district_select)

    # Kiểm tra assert
    assert not is_valid, "Expected the district field to be invalid, but it is valid."
    expected_message = "Please select an item in the list."
    assert validation_message == expected_message, f"Expected: '{expected_message}', Found: '{validation_message}'"

# THT_10: Bỏ trống Phường/Xã
def test_ward_empty(driver):
    driver.get("http://127.0.0.1:8000/")  # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)

    # Điền thông tin nhưng Bỏ trống Phường/Xã
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "", "123")
    time.sleep(3)
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Lấy phần tử select của Tỉnh/Thành phố
    ward_select = driver.find_element(By.CSS_SELECTOR, "select.input_search.ward[name='ward']")

    # Sử dụng JavaScript để kiểm tra tính hợp lệ và lấy thông báo lỗi
    is_valid = driver.execute_script("return arguments[0].checkValidity();", ward_select)
    validation_message = driver.execute_script("return arguments[0].validationMessage;", ward_select)

    # Kiểm tra assert
    assert not is_valid, "Expected the ward field to be invalid, but it is valid."
    expected_message = "Please select an item in the list."
    assert validation_message == expected_message, f"Expected: '{expected_message}', Found: '{validation_message}'"

    
# THT_11: Địa chỉ vượt quá 255 ký tự
def test_address_exceeds_255_characters(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "123"*256)
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[8]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Trường địa chỉ không được lớn hơn 255 kí tự."
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"

# THT_12: Bỏ trống Địa chỉ
def test_address_empty(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[8]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Trường địa chỉ không được bỏ trống."
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"

# THT_13: Địa chỉ chứa ký tự đặc biệt
def test_address_contains_special_characters(driver):
    driver.get("http://127.0.0.1:8000/") # Trang chủ
    log_in(driver)
    time.sleep(3)
    if is_cart_empty(driver):
        add_random_product_to_cart(driver)
    fill_checkout_form(driver, "Nguyễn Văn A", "0123456789", "user@example.com", "Lào Cai", "Huyện Si Ma Cai", "Thị Trấn Si Ma Cai", "273 An Dương Vương @#$%")
    ## scroll to button thanh toán
    scroll_to_element(driver, driver.find_element(By.CLASS_NAME, "btn-checkout"))
    ## click button thanh toán
    driver.find_element(By.CLASS_NAME, "btn-checkout").click()
    # Xác minh thông báo lỗi xuất hiện
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, "/html/body/section/div/form/div/div[1]/div[1]/div[8]/div[2]/span").text
    
    # Kiểm tra assert thông báo lỗi
    expected_message = "Trường địa chỉ không được chứa kí tự đặc biệt."
    assert error_message == expected_message, f"Expected: '{expected_message}', Found: '{error_message}'"