import json
import os
import pdfplumber
from playwright.sync_api import Page, expect

from utils.config import BASE_URL


# def load_orders(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)
def load_orders(path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, path)

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_popup_message(page):
    try:
        page.wait_for_selector("div[role='alert']", timeout=5000)
        return page.locator("div[role='alert']").inner_text()
    except:
        return "No popup message found"


# ---------- reusable order menu ----------
def open_order_menu(page):
    page.wait_for_selector("button:has(svg.lucide-ellipsis-vertical)")
    page.locator("button:has(svg.lucide-ellipsis-vertical)").first.click()


def create_order(page: Page, orders: dict):

    def fill(selector, value):
        page.locator(selector).fill(str(value))

    # UPDATED SELECT FUNCTION (SAFE FOR UAT + PROD)
    def select(combobox_id, option_name):
        locator = page.locator(f"div[role='combobox']#{combobox_id}, #{combobox_id}")
        locator.wait_for(timeout=30000)
        locator.click()
        page.get_by_role("option", name=option_name).first.click()

    page.locator("button:has-text('Create')").first.click()

    fill("#order-reference", orders["reference_no"])
    select("order-shipment-type", orders["shipment_type"])

    page.get_by_role("combobox", name="Order Status").click()
    page.get_by_role("option", name=orders["order_status"]).click()

    customer = orders["customer"]

    fill("#customer-first-name", customer["first_name"])
    fill("#customer-last-name", customer["last_name"])
    fill("#customer-company-name", customer["company"])
    fill("#customer-address-line", customer["address"])
    fill("#customer-pincode", customer["pincode"])
    fill("#customer-city", customer["city"])
    fill("#customer-phone", customer["phone"])
    fill("#customer-email", customer["email"])

    select("customer-country", customer["country"])
    select("customer-state", customer["state"])

    seller = orders["seller"]

    fill("#seller-first-name", seller["first_name"])
    fill("#seller-last-name", seller["last_name"])
    fill("#seller-company-name", seller["company"])
    fill("#seller-address-line", seller["address"])
    fill("#seller-pincode", seller["pincode"])
    fill("#seller-city", seller["city"])
    fill("#seller-phone", seller["phone"])
    fill("#seller-email", seller["email"])

    select("seller-country", seller["country"])
    select("seller-state", seller["state"])

    item = orders["item"]

    fill("#item-name", item["name"])
    fill("#item-sku", item["sku"])
    fill("#item-hs-code", item["hs_code"])
    fill("#item-value", item["value"])
    fill("#item-quantity", item["qty"])
    fill("#item-weight", item["weight"])
    fill("#item-length", item["length"])
    fill("#item-width", item["width"])
    fill("#item-height", item["height"])

    invoice = orders["invoice"]

    fill("#invoice-number", invoice["number"])
    fill("#invoice-value", invoice["value"])
    fill("#invoice-e-way-bill-number", invoice["eway"])
    fill("#invoice-date", invoice["date"])

    box = orders["box"]

    fill("#box-quantity", box["qty"])
    fill("#box-weight", box["weight"])
    fill("#box-height", box["height"])
    fill("#box-width", box["width"])
    fill("#box-length", box["length"])
    fill("#box-caseNo", box["case_no"])

    page.locator("button:has-text('Save Order')").click()

    msg = page.locator("//div[@role='alert']").text_content()
    return msg


def create_shipment(page: Page):

    page.locator("button[role='checkbox']").nth(1).click()

    page.get_by_role("button", name="Create Shipment").click()

    page.locator("span:has-text('Fetch Now')").click()

    page.locator("input[type='radio'][name='courier']").first.click()

    page.locator("text=DomesticPriority").click()

    page.locator("span:has-text('Ship Order')").click()


# -------- LABEL VALIDATION (UNCHANGED) --------
def download_and_validate_label(page, orders_data):

    ref = orders_data["reference_no"]

    page.wait_for_selector("text=Download Label", timeout=70000)

    with page.expect_download() as download_info:
        page.locator("span:has-text('Download Label')").click()

    download = download_info.value

    path = os.path.join(os.getcwd(), f"{ref}.pdf")

    download.save_as(path)

    print("Label Downloaded:", path)

    with pdfplumber.open(path) as pdf:
        text = ""
        for p in pdf.pages:
            text += p.extract_text() or ""

    text = text.upper()

    for section in orders_data.values():
        if isinstance(section, dict):
            for v in section.values():
                val = str(v).upper()
                if val in text:
                    print(f"✅ {v}")
                else:
                    print(f"❌ {v} NOT FOUND")


# -------- PICK LIST DOWNLOAD ONLY --------
def download_pick_list(download, orders_data):

    ref = orders_data["reference_no"]

    path = os.path.join(os.getcwd(), f"{ref}_picklist.pdf")

    download.save_as(path)

    print("\n=== PICK LIST ===")
    print("Pick List Downloaded:", path)


import time
from datetime import datetime

