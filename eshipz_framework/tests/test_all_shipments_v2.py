# from utils.shipment_functions_v2 import create_shipment, load_shipment_data, download_and_validate_label
from utils.config import BASE_URL
from utils.shipment_functions_v2 import load_shipment_data , download_and_validate_label,create_shipment


def test_all_shipments(logged_in_page):

    page = logged_in_page
    data = load_shipment_data()

    shipment_cases = [
        ("Document", "Personal"),
        ("Document", "Commercial"),
        ("Parcel", "Personal"),
        ("Parcel", "Commercial"),
    ]

    for shipment_type, courier_purpose in shipment_cases:

        print(f"\n===== Running Case: {shipment_type} | {courier_purpose} =====")

        try:

            # page.goto("https://uat.eshipz.com:444/v2/fulfillment/create-shipment")
            page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")
            page.wait_for_load_state("networkidle")

            create_shipment(page, data, shipment_type, courier_purpose)

            download_and_validate_label(page, data)

            print(f"✅ Shipment completed for {shipment_type} | {courier_purpose}")

        except Exception as e:

            print("❌ Error occurred while creating shipment")
            print(f"Case: {shipment_type} | {courier_purpose}")
            print(f"Error: {str(e)}")

            try:
                error_msg = page.locator("div[role='alert']").inner_text(timeout=3000)
                print(f"UI Error Message: {error_msg}")
            except:
                print("No UI error message captured")

        finally:

            print("➡ Moving to next shipment case...\n")

