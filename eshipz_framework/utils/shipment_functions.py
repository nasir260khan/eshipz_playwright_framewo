import json
import pdfplumber
import time
import re


def load_shipment_data():
    with open("data/oshipmentsdata.json") as f:
        return json.load(f)


def generate_customer_reference():
    return f"AUTO-{int(time.time()*1000)}"


def create_shipment(page, data, shipment_type, courier_purpose):

    customer_reference = generate_customer_reference()

    print(f"\n🚀 Shipment → {shipment_type} | {courier_purpose}")
    print(f"Customer Reference: {customer_reference}")

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
    page.locator(f"li[data-value='{seller['country']}']").click()

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
    page.locator(f"li[data-value='{customer['country']}']").click()

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

    page.locator("#box-quantity").fill(box["qty"])
    page.locator("#box-weight").fill(box["weight"])
    page.locator("#box-height").fill(box["height"])
    page.locator("#box-width").fill(box["width"])
    page.locator("#box-length").fill(box["length"])

    print("🔍 Fetching courier services...")

    page.locator("span:has-text('Fetch Now')").click()

    page.wait_for_selector("input[type='radio'][name='courier']", timeout=10000)

    page.locator("input[type='radio'][name='courier']").first.click()

    page.wait_for_timeout(1000)

    page.locator("text=DomesticPriority").click()

    print("🚚 DomesticPriority Selected")

    page.wait_for_timeout(2000)

    page.locator("span:has-text('Ship Order')").click()

    print("📦 Shipment Created")

    page.wait_for_timeout(5000)


def download_and_validate_label(page, data):

    page.wait_for_selector("span:has-text('Download Label')")

    with page.expect_download() as download_info:
        page.locator("span:has-text('Download Label')").click()

    download = download_info.value
    download.save_as("shipment_label.pdf")

    print("\n📄 Label Downloaded Successfully")

    label_text = ""

    with pdfplumber.open("shipment_label.pdf") as pdf:
        for p in pdf.pages:
            text = p.extract_text()
            if text:
                label_text += text

    label_text_lower = label_text.lower()

    print("\n🔎 Validating JSON Data Against Label\n")

    awb_match = re.search(r'\b\d{10,15}\b', label_text)

    if awb_match:
        print("\n📦 AWB NUMBER:", awb_match.group())
    else:
        print("\n⚠ AWB number not detected")

    print("\n🎉 LABEL VALIDATION COMPLETED\n")


def open_three_dot_menu(page):
    page.locator("svg.lucide-ellipsis-vertical").first.click()


def shipment_action(page, action_name):
    open_three_dot_menu(page)
    page.locator(f"text={action_name}").click()


def clone_shipment(page):

    shipment_action(page, "Clone Shipment")

    page.get_by_role("button", name="Yes").click()

    print("Clone confirmed")

    page.wait_for_timeout(3000)

    page.locator("span:has-text('Fetch Now')").click()

    page.wait_for_selector("input[type='radio'][name='courier']")

    page.locator("input[type='radio'][name='courier']").first.click()

    page.locator("text=DomesticPriority").click()

    page.wait_for_timeout(2000)

    page.locator("span:has-text('Ship Order')").click()

    print("📦 Cloned Shipment Created")

    page.wait_for_timeout(5000)


def download_label_from_menu(page):

    open_three_dot_menu(page)

    with page.expect_download() as download_info:
        page.locator("text=Label Download").click()

    download = download_info.value

    print(f"Label downloaded: {download.suggested_filename}")


def download_invoice(page):

    open_three_dot_menu(page)

    with page.context.expect_page() as new_page_info:
        page.locator("text=Invoice Download").click()

    invoice_page = new_page_info.value

    invoice_page.wait_for_load_state()

    print("Invoice page opened")

    invoice_page.close()

    page.bring_to_front()

    print("Returned to Shipments page")


def download_manifest(page):

    shipment_action(page, "Manifest")

    print("Opening Manifest Page")

    page.wait_for_url("**/v2/manifest")

    page.locator("button:has-text('Create Manifest')").click()

    page.wait_for_selector("text=Download Manifest")

    page.locator("button:has-text('Download Manifest')").click()

    page.wait_for_timeout(3000)

    page.goto("https://uat.eshipz.com:444/v2/fulfillment/shipment/all")


def select_bulk_shipments(page):

    checkbox = page.locator("button[role='checkbox']").first
    checkbox.click()

    page.wait_for_timeout(1000)


def open_bulk_actions(page):

    page.locator("text=Bulk Actions").click()
    page.wait_for_timeout(1000)


# def bulk_label_download(page):
#
#     open_bulk_actions(page)
#     page.locator("text=Label Download").click()
#     page.wait_for_timeout(4000)
def bulk_label_download(page):

    print("Bulk label download")

    open_bulk_actions(page)

    with page.expect_download() as download_info:
        page.get_by_role("menuitem", name="Label Download", exact=True).click()

    download = download_info.value

    # server filename (very long)
    original_name = download.suggested_filename

    # create short filename
    filename = f"bulk_labels_{int(time.time())}.pdf"

    download.save_as(f"downloads/{filename}")

    print(f"📄 Bulk Label PDF Downloaded: {filename}")
    print(f"Original filename from server: {original_name}")


def bulk_invoice_download(page):

    print("Bulk invoice download")

    open_bulk_actions(page)

    with page.context.expect_page() as new_page_info:
        page.get_by_role("menuitem", name="Invoice Download", exact=True).click()

    invoice_page = new_page_info.value

    invoice_page.wait_for_load_state()

    invoice_url = invoice_page.url

    print(f"📄 Bulk Invoice URL: {invoice_url}")

    # save invoice pdf
    filename = f"bulk_invoice_{int(time.time())}.pdf"

    invoice_page.pdf(path=f"downloads/{filename}")

    print(f"📄 Bulk Invoice PDF Saved: {filename}")

    invoice_page.close()

    page.bring_to_front()

    print("Returned to shipments page")


def bulk_add_notes(page):

    open_bulk_actions(page)

    page.locator("text=Bulk Shipment Note").click()

    page.wait_for_selector("textarea")

    page.locator("textarea").fill("Automation bulk note")

    page.locator("button:has-text('Add Notes')").click()

    page.wait_for_timeout(2000)