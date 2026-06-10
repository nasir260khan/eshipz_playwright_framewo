from utils.config import BASE_URL
from utils.NPR_functions import (
    get_created_shipment_details,
    search_shipment_by_customer_ref,
    open_npr_action,
    confirm_npr_action,
    search_awb_in_npr_action_requested,
    fill_npr_reschedule_date,
    fill_npr_edit_and_reschedule,
    update_carrier_tracking_status,
    CANCELFUNC, update_tracking_exception,
)
from utils.shipment_functions_v2 import load_shipment_data, create_shipment

from eshipz_framework.utils.NPR_functions import search_shipment_by_customer_refexce


def test_NPR(logged_in_page):
    page = logged_in_page
    data = load_shipment_data()

    shipment_cases = [
        ("Parcel", "Commercial"),
    ]

    npr_flows = [
        ("RESCHEDULE", fill_npr_reschedule_date),
        ("EDIT_AND_RESCHEDULE", fill_npr_edit_and_reschedule),
        ("CANCEL", CANCELFUNC),
    ]

    for shipment_type, courier_purpose in shipment_cases:
        for flow_name, npr_func in npr_flows:

            print(f"\n===== Running Case: {shipment_type} | {courier_purpose} | {flow_name} =====")

            try:
                page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")
                page.wait_for_load_state("networkidle")

                create_shipment(page, data, shipment_type, courier_purpose)

                custref, awb_text = get_created_shipment_details(page)

                search_shipment_by_customer_ref(page, BASE_URL, custref)
                update_tracking_exception(page)
                search_shipment_by_customer_refexce(page, BASE_URL, custref)

                open_npr_action(page)

                # ✅ CANCEL FLOW → skip everything else
                if flow_name == "CANCEL":
                    CANCELFUNC(page)
                    print("✅ Cancel flow executed. Skipping remaining steps.")
                else:
                    # ✅ Only RESCHEDULE and EDIT call this
                    npr_func(page)

                # ✅ Only for RESCHEDULE & EDIT


                status = confirm_npr_action(page, awb_text, action_type=flow_name)

                if status == "ACTION_REQUIRED":
                    print("🛑 Shipment is in Action Required. Moving to next case.")


                search_awb_in_npr_action_requested(page, BASE_URL, awb_text)

                update_carrier_tracking_status(page, awb_text)

                print(f"✅ Completed: {shipment_type} | {courier_purpose} | {flow_name}")

            except Exception as e:
                print("❌ Error occurred")
                print(f"Case: {shipment_type} | {courier_purpose} | {flow_name}")
                print(f"Error: {str(e)}")

                try:
                    error_msg = page.locator("div[role='alert']").inner_text(timeout=3000)
                    print(f"UI Error Message: {error_msg}")
                except:
                    print("No UI error message captured")

            finally:
                print("➡ Moving to next case...\n")