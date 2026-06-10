from utils.config import BASE_URL, UAT_URL, UAT_EMAIL, UAT_PASSWORD, PROD_EMAIL, PROD_PASSWORD
from utils.config import BASE_URL, UAT_URL, UAT_EMAIL, UAT_PASSWORD, PROD_EMAIL, PROD_PASSWORD


def login(page):

    page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded")

    # choose credentials based on environment
    if BASE_URL == UAT_URL:
        email = UAT_EMAIL
        password = UAT_PASSWORD
    else:
        email = PROD_EMAIL
        password = PROD_PASSWORD

    # login fields
    page.locator("#email").fill(email)
    page.locator("#password").fill(password)

    page.locator("#login-submit").click()

    # page.wait_for_load_state("networkidle")
    page.wait_for_load_state("domcontentloaded")