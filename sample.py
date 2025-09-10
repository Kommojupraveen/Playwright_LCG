from playwright.sync_api import sync_playwright
import datetime
import time

with sync_playwright() as p:
    # Launch browser
    iphone = p.devices['iPhone 15 Pro Max']
    browser = p.chromium.launch(headless=False).new_context(**iphone)
    #browser = p.chromium.launch(headless=False) # normal browser
    page = browser.new_page()

    # Open site
    page.goto("https://beta-www.coral.co.uk/en/sports", wait_until="load")
    page.wait_for_timeout(10000)
    page.get_by_role("button", name="Allow All").click()
    login_button = page.locator("//span[text()='LOG IN']")
    try:
        login_button.wait_for(state="visible", timeout=10000)
        # page.wait_for_load_state("domcontentloaded")
        time.sleep(5)
        login_button.click()
    except TimeoutError:
        print("Login button did not appear in time.")
    page.fill("input[name='username']", "testgvccl-DBMKOE")
    page.fill("input[name='password']", "Qwerty19")
    page.locator("//span[text()=' Log in ']").click()
    page.wait_for_load_state("load")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"C:/Users/kpraveen/PycharmProjects/Playwright/screenshot//s_{timestamp}.png"
    page.wait_for_selector('//div[@class="user-balance"]')
    balance = page.locator('//div[@class="user-balance"]').inner_text()
    if page.get_by_role("button", name="OK, THANKS").is_visible():
        page.get_by_role("button", name="OK, THANKS").click()
    page.locator('(//span[@data-crlat="oddsPrice"])[1]').click()
    if iphone.get('is_mobile'):
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
    print("bet receipt id: "+ bet_receipt_id)
    page.screenshot(path=filename)
    print(balance)
    browser.close()
