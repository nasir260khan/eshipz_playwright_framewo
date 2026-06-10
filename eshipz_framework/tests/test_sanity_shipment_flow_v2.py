import pytest
import random

from utils.config import BASE_URL
from utils.shipment_functions import load_shipment_data


# from utils.config import BASE_URL
from utils.shipment_functions_v2 import *

@pytest.mark.sanity
def test_sanity_shipment_flow(logged_in_page):

    page = logged_in_page
    page.set_default_timeout(60000)

    print("\n===== SANITY FLOW STARTED =====")

    data = load_shipment_data()
    shipment_type = "Document"
    courier_purpose = "Personal"

    try:

        print("\n===== CASE 1 : CREATE SHIPMENT =====")

        page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")
        page.wait_for_load_state("networkidle")

        page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")

        # FIX FOR CI
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector("#customer-reference", timeout=60000)

        create_shipment(page, data, shipment_type, courier_purpose)

        download_and_validate_label(page, data)

        page.keyboard.press("Escape")

        page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")
        page.wait_for_selector("svg.lucide-ellipsis-vertical")

    except Exception as e:

        print(f"❌ CASE 1 Failed : {e}")
        page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")


    try:

        print("\n===== CASE 2 : CLONE SHIPMENT =====")

        page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")
        page.wait_for_selector("svg.lucide-ellipsis-vertical")

        clone_shipment(page)

        download_and_validate_label(page, data)

        page.keyboard.press("Escape")

    except Exception as e:

        print(f"❌ CASE 2 Failed : {e}")


    try:

        print("\n===== CASE 3 : LABEL DOWNLOAD =====")

        page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")
        page.wait_for_selector("svg.lucide-ellipsis-vertical")

        download_label_from_menu(page)

    except Exception as e:

        print(f"❌ CASE 3 Failed : {e}")


    try:

        print("\n===== CASE 4 : INVOICE DOWNLOAD =====")

        page.wait_for_selector("svg.lucide-ellipsis-vertical")

        download_invoice(page)

    except Exception as e:

        print(f"❌ CASE 4 Failed : {e}")


    try:

        print("\n===== CASE 5 : SCHEDULE PICKUP =====")

        shipment_action(page, action_name="Schedule Pickup")

        page.locator("input[name='pickupDate']").fill("2026-03-12T11:00")

        page.locator("button:has(span:has-text('Schedule'))").last.click()

        page.wait_for_selector("svg.lucide-clock", timeout=10000)
        print("✔ Schedule Pickup Successful (clock icon visible)")

    except Exception as e:

        print(f"❌ CASE 5 Failed : {e}")


    try:

        print("\n===== CASE 6 : UPDATE EWAYBILL =====")

        shipment_action(page, action_name="Update eWaybill")

        ewaybill_number = str(random.randint(100000000000, 999999999999))

        page.locator("input[name='ewaybillNo']").fill(ewaybill_number)

        page.locator("div.rounded-xl button:has(span:has-text('Update'))").click()

        page.locator("text=updated").wait_for(timeout=10000)
        print(f"✔ E-Waybill Updated Successfully → {ewaybill_number}")

    except Exception as e:

        print(f"❌ CASE 6 Failed : {e}")


    try:

        print("\n===== CASE 7 : MANIFEST DOWNLOAD =====")

        page.goto(f"{BASE_URL}/v2/fulfillment/shipment/all")
        page.wait_for_selector("svg.lucide-ellipsis-vertical")

        download_manifest(page)

    except Exception as e:

        print(f"❌ CASE 7 Failed : {e}")


    try:

        print("\n===== CASE 8 : BULK LABEL DOWNLOAD =====")

        page.wait_for_selector("button[role='checkbox']")

        select_bulk_shipments(page)

        bulk_label_download(page)

    except Exception as e:

        print(f"❌ CASE 8 Failed : {e}")


    try:

        print("\n===== CASE 9 : BULK INVOICE DOWNLOAD =====")

        page.wait_for_selector("button[role='checkbox']")

        select_bulk_shipments(page)

        bulk_invoice_download(page)

    except Exception as e:

        print(f"❌ CASE 9 Failed : {e}")


    try:

        print("\n===== CASE 10 : BULK SHIPMENT NOTES =====")

        page.wait_for_selector("button[role='checkbox']")

        select_bulk_shipments(page)

        bulk_add_notes(page)

    except Exception as e:

        print(f"❌ CASE 10 Failed : {e}")


    try:

        print("\n===== CASE 11 : BULK MANIFEST DOWNLOAD =====")

        page.wait_for_selector("button[role='checkbox']")

        select_bulk_shipments(page)

        bulk_manifest_download(page)

    except Exception as e:

        print(f"❌ CASE 11 Failed : {e}")

    print("\n🎉 SANITY SUITE COMPLETED")