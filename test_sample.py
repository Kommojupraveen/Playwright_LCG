import pytest
import datetime
from playwright.sync_api import sync_playwright, TimeoutError
import time

mobile = False

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture
def browser_context(playwright_instance):
    global mobile
    iphone = None
    mobile = False
    # iphone = playwright_instance.devices['iPhone 15 Pro Max']
    # mobile = iphone.get('is_mobile')

    if mobile:
        browser = playwright_instance.chromium.launch(headless=False).new_context(**iphone)
    else:
        browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

def test_place_bet(playwright_instance, browser_context):
    v_filename = "C:/Users/kpraveen/PycharmProjects/Playwright/recording"
    context = browser_context.new_context(record_video_dir=v_filename)
    page = context.new_page()

    # Open site
    page.goto("url", wait_until="load")
    page.wait_for_timeout(10000)  # Wait for 10 seconds
    page.get_by_role("button", name="Allow All").click()

    login_button = page.locator("//span[text()='LOG IN']")
    try:
        login_button.wait_for(state="visible", timeout=10000)
        time.sleep(5)
        login_button.click()
    except TimeoutError:
        pytest.fail("Login button did not appear in time.")

    page.fill("input[name='username']", "testgvccl-DBMKOE")
    page.fill("input[name='password']", "Qwerty19")
    page.locator("//span[text()=' Log in ']").click()
    page.wait_for_load_state("load")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"C:/Users/kpraveen/PycharmProjects/Playwright/screenshot/s_{timestamp}.png"

    page.wait_for_selector('//div[@class="user-balance"]')
    balance = page.locator('//div[@class="user-balance"]').inner_text()

    # page.get_by_role("button", name="OK, THANKS").click()
    page.locator('(//span[@data-crlat="oddsPrice"])[1]').click()

    # Detect if running mobile emulator based on context
    if mobile:
        page.locator('//input[@placeholder="Stake"]').click()
        page.locator('//div[@data-value="0"]').click()
        page.locator('//div[@data-value="."]').click()
        page.locator('//div[@data-value="0"]').click()
        page.locator('//div[@data-value="1"]').click()
        page.locator("//span[text()='Place Bet']").click()
        page.locator('//div[@class="bet-details"]').is_visible()
        page.locator('//div[@class="bet-details"]').click()
    else:
        page.fill('input[id="singleStake-0"]', "0.01")
        page.locator("//span[text()='Place Bet']").click()

    bet_receipt = page.locator("//*[@data-uat='betId']")
    bet_receipt.wait_for(state="visible", timeout=10000)
    bet_receipt_id = bet_receipt.inner_text()
    print("bet receipt id: " + bet_receipt_id)

    page.screenshot(path=filename)
    print(balance)
