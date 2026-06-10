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
    CANCELFUNC, fill_npr_bulkedit_and_reschedule, fill_npr_reschedule_bulkdate, confirm_bulknpr_action,
    download_bulk_npr_excel, update_bulk_npr_excel, search_waybills_in_action_requested, upload_bulk_npr_excel,
    get_waybills_from_excel, update_tracking_exception,
)
from utils.shipment_functions_v2 import load_shipment_data, create_shipment


def test_bulkNPR(logged_in_page):
    page = logged_in_page
    data = load_shipment_data()

    shipment_cases = [
        ("Parcel", "Commercial"),
    ]

    npr_flows = [
        ("RESCHEDULE", fill_npr_reschedule_bulkdate),
        ("EDIT_AND_RESCHEDULE", fill_npr_bulkedit_and_reschedule),
    ]

    for shipment_type, courier_purpose in shipment_cases:

        for flow_name, npr_func in npr_flows:

            print(f"\n===== Running Case: {shipment_type} | {courier_purpose} | {flow_name} =====")

            page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")
            page.wait_for_load_state("networkidle")

            create_shipment(page, data, shipment_type, courier_purpose)

            custref, awb_text = get_created_shipment_details(page)
            search_shipment_by_customer_ref(page, BASE_URL, custref)
            update_tracking_exception(page)

            for attempt in range(1, 3):
                print(f"➡ NPR Attempt {attempt} for {flow_name}")

                search_shipment_by_customer_ref(page, BASE_URL, custref)
                open_npr_action(page)

                npr_func(page)

                status = confirm_bulknpr_action(page, awb_text)
                print(f"Attempt {attempt} Status: {status}")

                page.wait_for_timeout(2000)

            print(f"✅ NPR completed for {flow_name}")

        # ✅ Download only after all NPR actions are completed
        print("➡ All NPR actions completed. Now downloading Bulk NPR Excel")

        excel_path = download_bulk_npr_excel(page)

        # ✅ Get all waybill numbers before editing Excel
        waybill_text = get_waybills_from_excel(excel_path)
        print("✅ Waybill Text:", waybill_text)

        # ✅ Update downloaded Excel
        updated_excel = update_bulk_npr_excel(
            excel_path=excel_path,
            action_type="EDIT_AND_RESCHEDULE"
        )

        print("✅ Updated Excel Path:", updated_excel)

        # ✅ Upload updated Excel
        upload_bulk_npr_excel(page, updated_excel)

        # ✅ Search waybills in Action Requested tab
        search_waybills_in_action_requested(page, waybill_text)

        print("✅ Bulk NPR upload and Action Requested search completed")