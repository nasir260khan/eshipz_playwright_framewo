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
    CANCELFUNC,
    update_tracking_exception,
    fill_npr_bulkedit_and_reschedule,
    fill_npr_reschedule_bulkdate,
    confirm_bulknpr_action,
    download_bulk_npr_excel,
    update_bulk_npr_excel,
    search_waybills_in_action_requested,
    upload_bulk_npr_excel,
    get_waybills_from_excel,
)
from utils.shipment_functions_v2 import load_shipment_data, create_shipment

from utils.NPR_functions import search_shipment_by_customer_refexce


def create_and_make_npr_exception(page, data, shipment_type, courier_purpose):
    page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")
    page.wait_for_load_state("networkidle")

    create_shipment(page, data, shipment_type, courier_purpose)

    custref, awb_text = get_created_shipment_details(page)

    search_shipment_by_customer_ref(page, BASE_URL, custref)
    update_tracking_exception(page)

    return custref, awb_text


def test_single_and_bulk_npr(logged_in_page):
    page = logged_in_page
    data = load_shipment_data()

    shipment_cases = [
        ("Parcel", "Commercial"),
    ]

    single_npr_flows = [
        ("RESCHEDULE", fill_npr_reschedule_date),
        ("EDIT_AND_RESCHEDULE", fill_npr_edit_and_reschedule),
        ("CANCEL", CANCELFUNC),
    ]

    bulk_npr_flows = [
        ("RESCHEDULE", fill_npr_reschedule_bulkdate),
        ("EDIT_AND_RESCHEDULE", fill_npr_bulkedit_and_reschedule),
    ]

    # ============================================================
    # CASE 1: SINGLE NPR FLOW
    # ============================================================
    print("\n================ CASE 1: SINGLE NPR STARTED ================\n")

    for shipment_type, courier_purpose in shipment_cases:
        for flow_name, npr_func in single_npr_flows:

            print(f"\n===== Single NPR Case: {shipment_type} | {courier_purpose} | {flow_name} =====")

            try:
                custref, awb_text = create_and_make_npr_exception(
                    page, data, shipment_type, courier_purpose
                )

                search_shipment_by_customer_refexce(page, BASE_URL, custref,awb_text)
                open_npr_action(page)

                if flow_name == "CANCEL":
                    CANCELFUNC(page)
                    print("✅ Cancel flow executed.")
                else:
                    npr_func(page)

                status = confirm_npr_action(page, awb_text, action_type=flow_name)

                if status == "ACTION_REQUIRED":
                    print("🛑 Shipment is in Action Required.")

                search_awb_in_npr_action_requested(page, BASE_URL, awb_text)

                update_carrier_tracking_status(page, awb_text)

                print(f"✅ Single NPR Completed: {shipment_type} | {courier_purpose} | {flow_name}")

            except Exception as e:
                print("❌ Error occurred in Single NPR")
                print(f"Case: {shipment_type} | {courier_purpose} | {flow_name}")
                print(f"Error: {str(e)}")

            finally:
                print("➡ Moving to next Single NPR case...\n")

    # ============================================================
    # CASE 2: BULK NPR FLOW
    # ============================================================
    print("\n================ CASE 2: BULK NPR STARTED ================\n")

    for shipment_type, courier_purpose in shipment_cases:
        try:
            for flow_name, npr_func in bulk_npr_flows:

                print(f"\n===== Bulk NPR Case: {shipment_type} | {courier_purpose} | {flow_name} =====")

                custref, awb_text = create_and_make_npr_exception(
                    page, data, shipment_type, courier_purpose
                )

                for attempt in range(1, 3):
                    print(f"➡ Bulk NPR Attempt {attempt} for {flow_name}")

                    search_shipment_by_customer_ref(page, BASE_URL, custref)
                    open_npr_action(page)

                    npr_func(page)

                    status = confirm_bulknpr_action(page, awb_text)
                    print(f"Attempt {attempt} Status: {status}")

                    page.wait_for_timeout(2000)

                print(f"✅ Bulk NPR action completed for {flow_name}")

            print("➡ All Bulk NPR actions completed. Downloading Bulk NPR Excel")

            excel_path = download_bulk_npr_excel(page)

            waybill_text = get_waybills_from_excel(excel_path)
            print("✅ Waybill Text:", waybill_text)

            updated_excel = update_bulk_npr_excel(
                excel_path=excel_path,
                action_type="EDIT_AND_RESCHEDULE"
            )

            print("✅ Updated Excel Path:", updated_excel)

            upload_bulk_npr_excel(page, updated_excel)

            search_waybills_in_action_requested(page, waybill_text)

            print("✅ Bulk NPR upload and Action Requested search completed")

        except Exception as e:
            print("❌ Error occurred in Bulk NPR")
            print(f"Case: {shipment_type} | {courier_purpose}")
            print(f"Error: {str(e)}")

        finally:
            print("➡ Bulk NPR case completed\n")