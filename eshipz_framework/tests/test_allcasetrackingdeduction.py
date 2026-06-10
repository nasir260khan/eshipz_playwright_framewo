import re
import time
import pytest

from utils.config import BASE_URL
from utils.login import login
from utils.functions import load_orders, create_order, create_shipment as create_order_shipment
from utils.shipment_functions_v2 import load_shipment_data, create_shipment
from utils.navigation import go_to_reverse_create_page

from utils.customfunction import create_shipmentcus

from tests.test_importorderexcel import ship_order_with_retry
from utils.generated_excel import generate_excel_file


def get_shipment_credit(page):
    page.goto(f"{BASE_URL}/v2/home")

    page.wait_for_timeout(3000)

    body_text = page.locator("body").inner_text()

    match = re.search(
        r"Shipment Credit\s*.*?AVAILABLE\s*(\d+)\s*pts",
        body_text,
        re.I | re.S
    )

    assert match, f"❌ Shipment Credit not found. Page text:\n{body_text}"

    credit = int(match.group(1))
    print(f"✅ Shipment Credit Available: {credit}")
    return credit


def validate_shipment_credit(before_credit, after_credit, created_count, flow_name):
    expected_credit = before_credit - created_count

    print(f"\n===== CREDIT VALIDATION: {flow_name} =====")
    print(f"Before Credit  : {before_credit}")
    print(f"Created Count  : {created_count}")
    print(f"Expected Credit: {expected_credit}")
    print(f"Actual Credit  : {after_credit}")

    assert after_credit == expected_credit, (
        f"❌ Shipment credit not deducted for {flow_name}. "
        f"Before: {before_credit}, Created: {created_count}, "
        f"Expected: {expected_credit}, Actual: {after_credit}"
    )

    print(f"✅ Shipment credit deducted correctly for {flow_name}")


@pytest.fixture(scope="session")
def orders_data():
    return load_orders("data/orders.json")


def test_order_import_shipment_credit_deduction(page, orders_data):
    login(page)

    before_credit = get_shipment_credit(page)

    page.locator("img[alt='box']").first.click()
    page.wait_for_selector("span:has-text('Order')")
    page.locator("span:has-text('Order')").click()

    ref = "ORD" + str(int(time.time()))
    orders_data["reference_no"] = ref

    create_order(page, orders_data)

    page.wait_for_selector("button[role='checkbox']")
    create_order_shipment(page)

    page.wait_for_timeout(8000)

    after_credit = get_shipment_credit(page)

    validate_shipment_credit(
        before_credit=before_credit,
        after_credit=after_credit,
        created_count=1,
        flow_name="Order Import Shipment"
    )


def test_forward_shipment_credit_deduction(logged_in_page):
    page = logged_in_page
    data = load_shipment_data()

    shipment_cases = [
        ("Document", "Personal"),
        ("Document", "Commercial"),
        ("Parcel", "Personal"),
        ("Parcel", "Commercial"),
    ]

    before_credit = get_shipment_credit(page)

    created_count = 0

    for shipment_type, courier_purpose in shipment_cases:
        print(f"\n===== Running Case: {shipment_type} | {courier_purpose} =====")

        page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")
        page.wait_for_load_state("networkidle")

        create_shipment(page, data, shipment_type, courier_purpose)

        created_count += 1
        page.wait_for_timeout(3000)

    after_credit = get_shipment_credit(page)

    validate_shipment_credit(
        before_credit=before_credit,
        after_credit=after_credit,
        created_count=created_count,
        flow_name="Forward Shipment"
    )


def test_reverse_shipment_credit_deduction(page):
    login(page)

    page.set_default_timeout(60000)

    data = load_shipment_data()

    shipment_type = "Document"
    courier_purpose = "Personal"

    before_credit = get_shipment_credit(page)

    go_to_reverse_create_page(page)

    create_shipment(page, data, shipment_type, courier_purpose)

    page.wait_for_timeout(8000)

    after_credit = get_shipment_credit(page)

    validate_shipment_credit(
        before_credit=before_credit,
        after_credit=after_credit,
        created_count=1,
        flow_name="Reverse Shipment"
    )


def test_forward_shipment_credit_deductioncus(logged_in_page):
    page = logged_in_page
    data = load_shipment_data()

    shipment_cases = [

        ("Parcel", "Commercial"),
    ]

    before_credit = get_shipment_credit(page)

    created_count = 0

    for shipment_type, courier_purpose in shipment_cases:
        print(f"\n===== Running Case: {shipment_type} | {courier_purpose} =====")

        page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")


        create_shipmentcus(page, data, shipment_type, courier_purpose)

        created_count += 1
        page.wait_for_timeout(3000)

    after_credit = get_shipment_credit(page)

    validate_shipment_credit(
        before_credit=before_credit,
        after_credit=after_credit,
        created_count=created_count,
        flow_name="Forward Shipment"
    )

from pathlib import Path
@pytest.mark.bulk
def test_forward_shipment_credit_deductionimportorder(logged_in_page):

    page = logged_in_page

    # ==========================================
    # CREDIT BEFORE
    # ==========================================

    before_credit = get_shipment_credit(page)

    created_count = 0

    # ==========================================
    # NAVIGATION
    # ==========================================

    page.get_by_role(
        "heading",
        name="Create New Order"
    ).click()

    page.get_by_role(
        "button",
        name="Bulk"
    ).click()

    # ==========================================
    # EXCEL UPLOAD
    # ==========================================

    excel_file, order_refs = generate_excel_file()

    page.set_input_files(
        "input[type='file']",
        excel_file
    )

    page.locator(
        "//button[normalize-space()='Import your orders']"
    ).click()

    page.wait_for_timeout(5000)

    # ==========================================
    # SELECT IMPORTED ORDERS
    # ==========================================

    for order_ref in order_refs:

        row = page.locator(
            f"//tr[.//text()[normalize-space()='{order_ref}']]"
        )

        checkbox = row.locator(
            "xpath=.//button[@role='checkbox']"
        )

        checkbox.wait_for(
            state="visible",
            timeout=15000
        )

        if checkbox.get_attribute(
                "aria-checked"
        ) != "true":

            checkbox.click()

    # ==========================================
    # CREATE SHIPMENTS
    # ==========================================

    page.get_by_role(
        "button",
        name="Bulk Actions"
    ).click()

    page.get_by_role(
        "menuitem",
        name="Create Shipments"
    ).click()

    page.wait_for_timeout(5000)

    page.get_by_role(
        "button",
        name="Custom Ship"
    ).click()

    page.wait_for_timeout(3000)

    # ==========================================
    # SHIP ORDER
    # ==========================================

    ship_order_with_retry(page)

    created_count = len(order_refs)

    page.wait_for_timeout(3000)

    # ==========================================
    # DOWNLOAD LABEL
    # ==========================================

    download_dir = Path("downloads")

    download_dir.mkdir(exist_ok=True)

    with page.expect_download(timeout=60000) as download_info:

        page.get_by_role(
            "button",
            name="Download Label"
        ).click()

    download = download_info.value

    label_path = (
        download_dir /
        download.suggested_filename
    )

    download.save_as(label_path)

    assert label_path.exists()

    print("✅ LABEL DOWNLOADED SUCCESSFULLY")

    # ==========================================
    # CREDIT VALIDATION
    # ==========================================

    after_credit = get_shipment_credit(page)

    validate_shipment_credit(
        before_credit=before_credit,
        after_credit=after_credit,
        created_count=created_count,
        flow_name="Forward Shipment Import Order"
    )

    print("✅ Credit deduction validated successfully")
