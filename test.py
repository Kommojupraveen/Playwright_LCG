import pytest
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

mobile = False


@pytest.fixture(scope="session")
def selenium_driver():
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_place_bet(selenium_driver):
    driver = selenium_driver

    # Open site
    driver.get("url")
    time.sleep(10)  # Wait for 10 seconds

    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='LOG IN']"))
        )
        time.sleep(15)
        login_button.click()
    except TimeoutException:
        pytest.fail("Login button did not appear in time.")

    driver.find_element(By.NAME, "username").send_keys("testgvccl-DBMKOE")
    time.sleep(15)
    driver.find_element(By.NAME, "password").send_keys("Qwerty19")
    time.sleep(15)
    driver.find_element(By.XPATH, "//span[text()=' Log in ']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="user-balance"]'))
    )

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"C:/Users/kpraveen/PycharmProjects/Playwright/screenshot/s_{timestamp}.png"

    balance = driver.find_element(By.XPATH, '//div[@class="user-balance"]').text
    driver.find_element(By.XPATH, '(//span[@data-crlat="oddsPrice"])[1]').click()

    # Handle mobile emulator based on context
    if mobile:
        driver.find_element(By.XPATH, '//input[@placeholder="Stake"]').click()
        driver.find_element(By.XPATH, '//div[@data-value="0"]').click()
        driver.find_element(By.XPATH, '//div[@data-value="."]').click()
        driver.find_element(By.XPATH, '//div[@data-value="0"]').click()
        driver.find_element(By.XPATH, '//div[@data-value="1"]').click()
        driver.find_element(By.XPATH, "//span[text()='Place']").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="bet-details"]'))
        )
        driver.find_element(By.XPATH, '//div[@class="bet-details"]').click()
    else:
        time.sleep(10)
        driver.find_element(By.ID, 'singleStake-0').send_keys("0.01")
        driver.find_element(By.XPATH, "//span[contains(text(),'Place Bet')]").click()
    time.sleep(10)
    bet_receipt = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@data-uat='betId']"))
    )
    bet_receipt_id = bet_receipt.text
    print("bet receipt id: " + bet_receipt_id)

    driver.save_screenshot(filename)
    print(balance)