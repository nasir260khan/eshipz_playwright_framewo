import os
import re
import csv
import random
from pathlib import Path
from playwright.sync_api import sync_playwright


BASE_URL = "https://uat.eshipz.com:444"
EMAIL = "madhuraki27@gmail.com"
PASSWORD = "password"

BULK_COUNT = 5

CSV_PATH = Path(
    r"C:\Automationscripts\eshipz_playwright_framework\downloadedfiles\Trackingexcel\tracking_upload.csv"
)


def login(page):
    page.goto(f"{BASE_URL}/login")
    page.get_by_role("textbox", name="Enter your email").fill(EMAIL)
    page.get_by_role("textbox", name="Enter your password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")


def get_tracking_credit(page):
    page.goto(f"{BASE_URL}/v2/home")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    page_text = page.locator("body").inner_text()

    print("========== HOME PAGE TEXT ==========")
    print(page_text)
    print("====================================")

    match = re.search(
        r"Tracking Credit\s*.*?AVAILABLE\s*(\d+)\s*pts",
        page_text,
        re.I | re.S
    )

    assert match, "❌ Tracking Credit AVAILABLE count not found"

    tracking_credit = int(match.group(1))

    print(f"✅ Tracking Credit Available: {tracking_credit}")

    return tracking_credit


def create_filled_tracking_csv(csv_path, count):
    rows = []

    assert csv_path.exists(), f"CSV file not found: {csv_path}"

    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        assert headers is not None, "CSV headers not found"

        for i in range(count):

            row = next(reader, None)

            if row is None:
                row = {header: "" for header in headers}

            random_order_id = f"AUTO{random.randint(100000, 999999)}"
            random_awb = f"9{random.randint(1000000000, 9999999999)}"
            random_phone = f"98{random.randint(10000000, 99999999)}"

            if "order_id" in row:
                row["order_id"] = random_order_id

            if "awb" in row:
                row["awb"] = random_awb

            if "shipment_type" in row:
                row["shipment_type"] = "forward"

            if "first_name" in row:
                row["first_name"] = f"Test{i + 1}"

            if "last_name" in row:
                row["last_name"] = "User"

            if "phone" in row:
                row["phone"] = random_phone

            if "email" in row:
                row["email"] = f"test{i + 1}@gmail.com"

            rows.append(row)

    new_file_name = f"tracking_upload_{count}_forward_shipments.csv"

    new_csv_path = csv_path.parent / new_file_name

    with open(new_csv_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Filled CSV Created: {new_file_name}")
    print(f"📁 File Path: {new_csv_path}")

    return new_csv_path


def upload_tracking_csv(page, csv_path):
    page.goto(f"{BASE_URL}/v2/fulfillment/shipment")
    page.wait_for_load_state("networkidle")

    page.get_by_role("button", name=re.compile("Upload Tracking", re.I)).click()

    page.get_by_text("Upload Excel File").click()

    page.locator("input[type='file']").set_input_files(str(csv_path))

    page.wait_for_timeout(3000)

    upload_button = page.get_by_role(
        "button",
        name=re.compile("Upload|Submit|Import", re.I)
    )

    if upload_button.count() > 0:
        upload_button.first.click()

    page.wait_for_timeout(7000)

    print(f"✅ Uploaded File: {csv_path.name}")


def is_headless_mode():
    return os.getenv("CI", "").lower() in {"1", "true", "yes"} or os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}


def test_tracking_credit_deduction():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=is_headless_mode(),
            slow_mo=0 if is_headless_mode() else 500
        )

        context = browser.new_context()

        page = context.new_page()

        login(page)

        before_credit = get_tracking_credit(page)

        print(f"📌 Before Tracking Credit: {before_credit}")

        filled_csv_path = create_filled_tracking_csv(
            CSV_PATH,
            BULK_COUNT
        )

        upload_tracking_csv(
            page,
            filled_csv_path
        )

        after_credit = get_tracking_credit(page)

        print(f"📌 After Tracking Credit: {after_credit}")

        expected_credit = before_credit - BULK_COUNT

        print(f"📌 Expected Tracking Credit: {expected_credit}")

        assert after_credit == expected_credit, (
            f"❌ Tracking credit deduction failed.\n"
            f"Before Credit: {before_credit}\n"
            f"Uploaded Shipments: {BULK_COUNT}\n"
            f"Expected Credit: {expected_credit}\n"
            f"Actual Credit: {after_credit}"
        )

        print("✅ Tracking Credit Deducted Successfully")

        context.close()
        browser.close()