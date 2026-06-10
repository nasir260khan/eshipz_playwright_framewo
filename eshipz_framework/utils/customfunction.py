import json
import pdfplumber
import time
import re
import os


from utils.config import BASE_URL




DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def load_shipment_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "oshipmentsdata.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_customer_reference():
    return f"AUTO-{int(time.time()*1000)}"


def open_three_dot_menu(page):
    page.locator("svg.lucide-ellipsis-vertical").first.click()


def shipment_action(page, action_name):
    open_three_dot_menu(page)
    page.locator(f"text={action_name}").click()


def select_bulk_shipments(page):
    page.locator("button[role='checkbox']").first.click()


def open_bulk_actions(page):
    page.locator("text=Bulk Actions").click()


# ---------------- CREATE SHIPMENT ----------------

def create_shipmentcus(page, data, shipment_type, courier_purpose):

    customer_reference = generate_customer_reference()

    print(f"\n🚀 Shipment → {shipment_type} | {courier_purpose}")
    print(f"Customer Reference: {customer_reference}")

    page.wait_for_selector("#customer-reference", state="visible", timeout=60000)

    # page.wait_for_selector("#customer-reference", state="visible", timeout=60000)

    page.locator("#customer-reference").fill(customer_reference)
    page.locator("#parcel-description").fill(data["parcel_description"])

    page.get_by_role("combobox", name="Shipment Type").click()
    page.get_by_role("option", name=shipment_type, exact=True).click()

    page.get_by_role("combobox", name="Courier Purpose").click()
    page.get_by_role("option", name=courier_purpose, exact=True).click()

    seller = data["seller"]

    page.get_by_role("textbox", name="First Name", exact=True).fill(seller["first_name"])
    page.locator("#seller-company-name").fill(seller["company"])
    page.locator("#seller-address-line1").fill(seller["address1"])
    page.locator("#seller-address-line2").fill(seller["address2"])
    page.locator("#seller-address-line3").fill(seller["address3"])

    page.locator("#seller-country").click()

    page.wait_for_selector("ul[role='listbox']", timeout=15000)

    page.locator(f"li[data-value='{seller['country']}']").click()

    # page.locator("#seller-country").click()
    # page.locator(f"li[data-value='{seller['country']}']").click()

    page.locator("#seller-pincode").fill(seller["pincode"])

    page.locator("#seller-state").click()
    page.get_by_role("option", name=seller["state"], exact=True).click()

    page.locator("#seller-city").fill(seller["city"])

    page.locator("#seller-phone").fill(seller["phone"])
    page.locator("#seller-email").fill(seller["email"])

    customer = data["customer"]

    page.get_by_role("textbox", name="First Name *").fill(customer["first_name"])
    page.locator("#customer-company-name").fill(customer["company"])

    page.locator("#customer-address-line1").fill(customer["address1"])
    page.locator("#customer-address-line2").fill(customer["address2"])
    page.locator("#customer-address-line3").fill(customer["address3"])

    page.locator("#customer-country").click()

    page.wait_for_selector("ul[role='listbox']", timeout=15000)

    page.locator(f"li[data-value='{customer['country']}']").click()



    # page.locator("#customer-country").click()
    # page.locator(f"li[data-value='{customer['country']}']").click()

    page.locator("#customer-pincode").fill(customer["pincode"])

    page.locator("#customer-state").click()
    page.get_by_role("option", name=customer["state"], exact=True).click()

    page.locator("#customer-city").fill(customer["city"])

    page.locator("#customer-phone").fill(customer["phone"])
    page.locator("#customer-email").fill(customer["email"])

    invoice = data["invoice"]

    page.get_by_role("textbox", name="Enter invoice number").fill(invoice["number"])
    page.locator("#invoice-value").fill(invoice["value"])

    box = data["box"]

    page.wait_for_selector("#box-package-type", state="visible", timeout=20000)
    # page.locator("#box-package-type").click()
    # page.wait_for_selector("li[role='option']", timeout=10000)
    # page.get_by_role("option", name="Custom").click()
    # page.locator("#box-quantity").fill(box["qty"])
    # page.locator("#box-weight").fill(box["weight"])
    # page.locator("#box-height").fill(box["height"])
    # page.locator("#box-width").fill(box["width"])
    # page.locator("#box-length").fill(box["length"])

    page.get_by_role(
        "button",
        name="Custom Ship"
    ).click()

    page.wait_for_timeout(5000)

    import random

    def select_random_option(page, dropdown_locator, field_name):
        dropdown_locator.click()
        page.wait_for_timeout(2500)

        options = page.locator('[role="option"]:visible')

        invalid_keywords = [
            "select",
            "international",
            "worldwide",
            "export",
            "import"
        ]

        valid_options = []

        for i in range(options.count()):
            text = options.nth(i).inner_text().strip()

            if not text:
                continue

            text_lower = text.lower()

            if any(keyword in text_lower for keyword in invalid_keywords):
                continue

            valid_options.append((i, text))

        if not valid_options:
            raise Exception(f"No valid {field_name} found")

        idx, selected_value = random.choice(valid_options)

        print(f"Selecting {field_name}: {selected_value}")

        options.nth(idx).click()

        page.wait_for_timeout(2000)

        return selected_value

    # =====================================
    # PREPAID MAPPING
    # =====================================

    print("\n===== PREPAID MAPPING =====")

    prepaid_carrier = select_random_option(
        page,
        page.locator("#prepaid-carrier"),
        "Prepaid Carrier"
    )

    prepaid_vendor = select_random_option(
        page,
        page.locator("#prepaid-vendor"),
        "Prepaid Vendor"
    )

    prepaid_service = select_random_option(
        page,
        page.locator("#prepaid-service"),
        "Prepaid Service"
    )

    print("\n===== COD MAPPING =====")

    page.wait_for_timeout(3000)

    cod_carrier = select_random_option(
        page,
        page.locator("#cod-carrier"),
        "COD Carrier"
    )

    cod_vendor = select_random_option(
        page,
        page.locator("#cod-vendor"),
        "COD Vendor"
    )

    page.wait_for_timeout(3000)

    cod_service = select_random_option(
        page,
        page.locator("#cod-service"),
        "COD Service"
    )

    # =====================================
    # FINAL OUTPUT
    # =====================================

    print("\n===== FINAL MAPPING =====")
    print(f"Prepaid Carrier : {prepaid_carrier}")
    print(f"Prepaid Vendor  : {prepaid_vendor}")
    print(f"Prepaid Service : {prepaid_service}")

    print(f"COD Carrier     : {cod_carrier}")
    print(f"COD Vendor      : {cod_vendor}")
    print(f"COD Service     : {cod_service}")

    # =====================================
    # SHIP ORDER
    # =====================================

    page.get_by_role(
        "button",
        name="Ship Order"
    ).click()

    page.wait_for_timeout(5000)

    print("Shipment created successfully")
    print("📦 Shipment Created")

#     import random
#
#     print("\n===== PREPAID MAPPING =====")
#
#     # =====================================
#     # PREPAID CARRIER
#     # =====================================
#
#     page.locator("#prepaid-carrier").click()
#     page.wait_for_timeout(1500)
#
#     options = page.locator('[role="option"]:visible')
#
#     count = options.count()
#
#     if count == 0:
#         raise Exception("No Prepaid Carriers Found")
#
#     idx = random.randint(0, count - 1)
#
#     prepaid_carrier = (
#         options.nth(idx)
#         .inner_text()
#         .strip()
#     )
#
#     options.nth(idx).click()
#
#     print(f"Prepaid Carrier : {prepaid_carrier}")
#
#     page.wait_for_timeout(2000)
#
#     # =====================================
#     # PREPAID VENDOR
#     # =====================================
#
#     page.locator("#prepaid-vendor").click()
#     page.wait_for_timeout(1500)
#
#     options = page.locator('[role="option"]:visible')
#
#     count = options.count()
#
#     if count == 0:
#         raise Exception("No Prepaid Vendors Found")
#
#     idx = random.randint(0, count - 1)
#
#     prepaid_vendor = (
#         options.nth(idx)
#         .inner_text()
#         .strip()
#     )
#
#     options.nth(idx).click()
#
#     print(f"Prepaid Vendor : {prepaid_vendor}")
#
#     page.wait_for_timeout(2000)
#
#     # =====================================
#     # PREPAID SERVICE
#     # =====================================
#
#     page.locator("#prepaid-service").click()
#     page.wait_for_timeout(1500)
#
#     options = page.locator('[role="option"]:visible')
#
#     count = options.count()
#
#     if count == 0:
#         raise Exception("No Prepaid Services Found")
#
#     idx = random.randint(0, count - 1)
#
#     prepaid_service = (
#         options.nth(idx)
#         .inner_text()
#         .strip()
#     )
#
#     options.nth(idx).click()
#
#     print(f"Prepaid Service : {prepaid_service}")
#
#     page.wait_for_timeout(3000)
#
#     print("\n===== COD MAPPING =====")
#
#     # =====================================
#     # COD CARRIER
#     # =====================================
#
#     carrier_dropdown = page.get_by_role(
#         "combobox"
#     ).nth(0)
#
#     carrier_dropdown.click()
#
#     page.wait_for_timeout(1500)
#
#     options = page.locator('[role="option"]:visible')
#
#     count = options.count()
#
#     if count == 0:
#         raise Exception("No COD Carriers Found")
#
#     idx = random.randint(0, count - 1)
#
#     cod_carrier = (
#         options.nth(idx)
#         .inner_text()
#         .strip()
#     )
#
#     options.nth(idx).click()
#
#     print(f"COD Carrier : {cod_carrier}")
#
#     page.wait_for_timeout(2000)
#
#     # =====================================
#     # COD VENDOR
#     # =====================================
#
#     vendor_dropdown = page.get_by_role(
#         "combobox"
#     ).nth(1)
#
#     vendor_dropdown.click()
#
#     page.wait_for_timeout(1500)
#
#     options = page.locator('[role="option"]:visible')
#
#     count = options.count()
#
#     if count == 0:
#         raise Exception("No COD Vendors Found")
#
#     idx = random.randint(0, count - 1)
#
#     cod_vendor = (
#         options.nth(idx)
#         .inner_text()
#         .strip()
#     )
#
#     options.nth(idx).click()
#
#     print(f"COD Vendor : {cod_vendor}")
#
#     page.wait_for_timeout(2000)
#
#     # =====================================
#     # COD SERVICE
#     # =====================================
#
#     service_dropdown = page.get_by_role(
#         "combobox"
#     ).nth(2)
#
#     service_dropdown.click()
#
#     page.wait_for_timeout(1500)
#
#     options = page.locator('[role="option"]:visible')
#
#     count = options.count()
#
#     if count == 0:
#         raise Exception("No COD Services Found")
#
#     idx = random.randint(0, count - 1)
#
#     cod_service = (
#         options.nth(idx)
#         .inner_text()
#         .strip()
#     )
#
#     options.nth(idx).click()
#
#     print(f"COD Service : {cod_service}")
#
#     page.wait_for_timeout(2000)
#
#     print("\n===== FINAL MAPPING =====")
#     print(f"Prepaid Carrier : {prepaid_carrier}")
#     print(f"Prepaid Vendor  : {prepaid_vendor}")
#     print(f"Prepaid Service : {prepaid_service}")
#
#     print(f"COD Carrier     : {cod_carrier}")
#     print(f"COD Vendor      : {cod_vendor}")
#     print(f"COD Service     : {cod_service}")
#
#     page.get_by_role(
#         "button",
#         name="Ship Order"
#     ).click()
#
#     print("Shipment created successfully")
#
#
# print("📦 Shipment Created")

# ---------------- LABEL VALIDATION ----------------

def download_and_validate_label(page, data):

    page.wait_for_selector("span:has-text('Download Label')")

    with page.expect_download() as download_info:
        page.locator("span:has-text('Download Label')").click()

    download = download_info.value
    filename = f"{DOWNLOAD_DIR}/shipment_label_{int(time.time())}.pdf"
    download.save_as(filename)

    print(f"\n📄 Label Downloaded Successfully → {filename}")

    label_text = ""

    with pdfplumber.open(filename) as pdf:
        for p in pdf.pages:
            text = p.extract_text()
            if text:
                label_text += text

    label_text_lower = label_text.lower()

    awb_match = re.search(r'\b\d{10,15}\b', label_text)

    if awb_match:
        print(f"📦 AWB NUMBER: {awb_match.group()}")

    customer = data["customer"]
    invoice = data["invoice"]

    validations = {
        "Customer Name": customer["first_name"],
        "Customer Phone": customer["phone"],
        "Customer City": customer["city"],
        "Customer Pincode": customer["pincode"],
        "Invoice Value": invoice["value"],
    }

    for field, value in validations.items():

        if str(value).lower() in label_text_lower:
            print(f"✔ {field} found in label → {value}")
        else:
            print(f"❌ {field} NOT found in label → {value}")


# ---------------- CLONE ----------------

def clone_shipment(page):

    shipment_action(page, "Clone Shipment")

    page.get_by_role("button", name="Yes").click()

    page.locator("span:has-text('Fetch Now')").click()

    page.wait_for_selector("input[type='radio'][name='courier']")

    page.locator("input[type='radio'][name='courier']").first.click()
    page.locator("text=DomesticPriority").click()

    page.locator("span:has-text('Ship Order')").click()

    print("📦 Cloned Shipment Created")

    page.wait_for_selector("span:has-text('Download Label')")


# ---------------- CASE 3 ----------------

def download_label_from_menu(page):

    open_three_dot_menu(page)

    with page.expect_download() as download_info:
        page.locator("text=Label Download").click()

    download = download_info.value
    filename = f"{DOWNLOAD_DIR}/label_menu_{int(time.time())}.pdf"
    download.save_as(filename)

    print(f"📄 Label downloaded from menu → {filename}")


# ---------------- CASE 4 ----------------

def download_invoice(page):

    open_three_dot_menu(page)

    with page.context.expect_page() as new_page_info:
        page.locator("text=Invoice Download").click()

    invoice_page = new_page_info.value
    invoice_page.wait_for_load_state()

    filename = f"{DOWNLOAD_DIR}/invoice_{int(time.time())}.pdf"
    invoice_page.pdf(path=filename)

    print(f"📄 Invoice PDF saved → {filename}")

    invoice_page.close()
    page.bring_to_front()


# ---------------- SINGLE MANIFEST ----------------

def download_manifest(page):

    print("Single Manifest creation")

    shipment_action(page, "Manifest")

    page.wait_for_url("**/v2/manifest")

    page.locator("button:has-text('Create Manifest')").click()

    page.wait_for_selector("button:has-text('Download Manifest')")

    page.locator("button:has-text('Download Manifest')").click()

    page.wait_for_timeout(3000)

    page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")

    # page.goto("https://uat.eshipz.com:444/v2/fulfillment/shipment/all")


# ---------------- BULK LABEL ----------------

def bulk_label_download(page):

    open_bulk_actions(page)

    with page.expect_download() as download_info:
        page.get_by_role("menuitem", name="Label Download", exact=True).click()

    download = download_info.value
    filename = f"{DOWNLOAD_DIR}/bulk_labels_{int(time.time())}.pdf"
    download.save_as(filename)

    print(f"📄 Bulk Label Downloaded → {filename}")


# ---------------- BULK INVOICE ----------------

def bulk_invoice_download(page):

    open_bulk_actions(page)

    with page.context.expect_page() as new_page_info:
        page.get_by_role("menuitem", name="Invoice Download", exact=True).click()

    invoice_page = new_page_info.value
    invoice_page.wait_for_load_state()

    filename = f"{DOWNLOAD_DIR}/bulk_invoice_{int(time.time())}.pdf"
    invoice_page.pdf(path=filename)

    print(f"📄 Bulk Invoice Saved → {filename}")

    invoice_page.close()
    page.bring_to_front()


# ---------------- BULK NOTES ----------------

def bulk_add_notes(page):

    open_bulk_actions(page)

    page.locator("text=Bulk Shipment Note").click()

    page.wait_for_selector("textarea")

    page.locator("textarea").fill("Automation bulk note")

    page.locator("button:has-text('Add Notes')").click()

    print("✔ Bulk notes added")


# ---------------- BULK MANIFEST ----------------

def bulk_manifest_download(page):

    print("Bulk Manifest creation")

    open_bulk_actions(page)

    page.locator("text=Manifest").click(force=True)

    page.wait_for_url("**/v2/manifest")

    page.locator("button:has-text('Create Manifest')").click()

    page.wait_for_selector("button:has-text('Download Manifest')", timeout=20000)

    page.locator("button:has-text('Download Manifest')").click(force=True)

    page.wait_for_timeout(3000)

    page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")

    # page.goto("https://uat.eshipz.com:444/v2/fulfillment/shipment/all")




from utils.shipment_functions_v2 import generate_customer_reference


def create_shipment_ndr(page, data, shipment_type, courier_purpose):

    customer_reference = generate_customer_reference()

    print(f"\n🚀 Shipment → {shipment_type} | {courier_purpose}")
    print(f"Customer Reference: {customer_reference}")

    page.wait_for_selector("#customer-reference", state="visible", timeout=60000)

    # page.wait_for_selector("#customer-reference", state="visible", timeout=60000)

    page.locator("#customer-reference").fill(customer_reference)
    page.locator("#parcel-description").fill(data["parcel_description"])

    page.get_by_role("combobox", name="Shipment Type").click()
    page.get_by_role("option", name=shipment_type, exact=True).click()

    page.get_by_role("combobox", name="Courier Purpose").click()
    page.get_by_role("option", name=courier_purpose, exact=True).click()

    seller = data["seller"]

    page.get_by_role("textbox", name="First Name", exact=True).fill(seller["first_name"])
    page.locator("#seller-company-name").fill(seller["company"])
    page.locator("#seller-address-line1").fill(seller["address1"])
    page.locator("#seller-address-line2").fill(seller["address2"])
    page.locator("#seller-address-line3").fill(seller["address3"])

    page.locator("#seller-country").click()

    page.wait_for_selector("ul[role='listbox']", timeout=15000)

    page.locator(f"li[data-value='{seller['country']}']").click()

    # page.locator("#seller-country").click()
    # page.locator(f"li[data-value='{seller['country']}']").click()

    page.locator("#seller-pincode").fill(seller["pincode"])

    page.locator("#seller-state").click()
    page.get_by_role("option", name=seller["state"], exact=True).click()

    page.locator("#seller-city").fill(seller["city"])

    page.locator("#seller-phone").fill(seller["phone"])
    page.locator("#seller-email").fill(seller["email"])

    customer = data["customer"]

    page.get_by_role("textbox", name="First Name *").fill(customer["first_name"])
    page.locator("#customer-company-name").fill(customer["company"])

    page.locator("#customer-address-line1").fill(customer["address1"])
    page.locator("#customer-address-line2").fill(customer["address2"])
    page.locator("#customer-address-line3").fill(customer["address3"])

    page.locator("#customer-country").click()

    page.wait_for_selector("ul[role='listbox']", timeout=15000)

    page.locator(f"li[data-value='{customer['country']}']").click()



    # page.locator("#customer-country").click()
    # page.locator(f"li[data-value='{customer['country']}']").click()

    page.locator("#customer-pincode").fill(customer["pincode"])

    page.locator("#customer-state").click()
    page.get_by_role("option", name=customer["state"], exact=True).click()

    page.locator("#customer-city").fill(customer["city"])

    page.locator("#customer-phone").fill(customer["phone"])
    page.locator("#customer-email").fill(customer["email"])

    invoice = data["invoice"]

    page.get_by_role("textbox", name="Enter invoice number").fill(invoice["number"])
    page.locator("#invoice-value").fill(invoice["value"])

    box = data["box"]

    page.wait_for_selector("#box-package-type", state="visible", timeout=20000)
    page.locator("#box-package-type").click()
    page.wait_for_selector("li[role='option']", timeout=10000)
    page.get_by_role("option", name="Custom").click()
    page.locator("#box-quantity").fill(box["qty"])
    page.locator("#box-weight").fill(box["weight"])
    page.locator("#box-height").fill(box["height"])
    page.locator("#box-width").fill(box["width"])
    page.locator("#box-length").fill(box["length"])

    page.locator("span:has-text('Fetch Now')").click()

    # page.wait_for_selector("input[type='radio'][name='courier']", timeout=10000)
    #
    # page.locator("input[type='radio'][name='courier']").first.click()
    # page.locator("text=DomesticPriority").click()
    page.get_by_text("INDIA_POST").click()
    page.get_by_text("speed_prepaid").click()
    time.sleep(2)
    page.get_by_role("button", name="Ship Order").click()





    print("📦 Shipment Created")

    page.wait_for_selector("span:has-text('Download Label')")