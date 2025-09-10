from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

def find_element_by_xpath(xpath, timeout=20):
    time_wait_as_of_now = 0
    element = None
    while not element:
        try:
            element = driver.find_element(By.XPATH, xpath)
        except:
            time.sleep(0.5)
            time_wait_as_of_now += 0.5
        if element or time_wait_as_of_now == timeout:
            break
    return element

def send_keys(element, keys, delay=0.1):
    for symbol in str(keys):
        element.send_keys(symbol)
        time.sleep(delay)

def scroll_to_we(target_element):
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                          target_element)


# === Configuration ===
URL = "url"  # Replace with your actual login URL
USERNAME = "testgvccl-UTKLVJ"
PASSWORD = "Qwerty19"

# === Setup WebDriver ===
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)  # You can also use Firefox(), Edge(), etc.

# Open the login page
driver.get(URL)
driver.maximize_window()
time.sleep(20)

login_button = find_element_by_xpath('.//*[@data-testid="signin"]')
login_button.click()
time.sleep(5)

username_field = find_element_by_xpath('.//*[@name="username"]')
send_keys(username_field, USERNAME)

password_field = find_element_by_xpath( './/*[@name="password"]')
send_keys(password_field, PASSWORD)

login_button = find_element_by_xpath(".//button[contains(@class, 'login')]")
login_button.click()
time.sleep(10)

profile_icon = find_element_by_xpath('.//*[@title="theme-avatar"]')
assert profile_icon, "Login Failed"

time.sleep(5)  # Wait for navigation/load

profile_icon.click()
