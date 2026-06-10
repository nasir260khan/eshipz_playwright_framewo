# from utils.NDR_FUNCTIONS import open_ndr_action, fill_NDR_reschedule_date, fill_NDR_edit_and_reschedule, RTOFUNC, \
#     confirm_ndr_action
# from utils.config import BASE_URL
# from utils.NDR_FUNCTIONS import (
#     get_created_shipment_details,
#     search_shipment_by_customer_ref,
#     open_ndr_action,
#     confirm_ndr_action,
#     search_awb_in_ndr_action_requested,
#     fill_NDR_reschedule_date,
#     fill_NDR_edit_and_reschedule,
#     update_carrier_tracking_status,
#     RTOFUNC, update_tracking_exception,
# )
# from utils.shipment_functions_v2 import load_shipment_data, create_shipment, create_shipment_ndr
#
# from eshipz_framework.utils.NDR_FUNCTIONS import search_shipment_by_customer_refexcep
#
#
# def test_NPR(logged_in_page):
#     page = logged_in_page
#     data = load_shipment_data()
#
#     shipment_cases = [
#         ("Parcel", "Commercial"),
#     ]
#
#     ndr_flows = [
#         ("RE-ATTEMPT", fill_NDR_reschedule_date),
#         ("EDIT_AND_RESCHEDULE", fill_NDR_edit_and_reschedule),
#         ("RTO", RTOFUNC),
#     ]
#
#     for shipment_type, courier_purpose in shipment_cases:
#         for flow_name, ndr_func in ndr_flows:
#
#             print(f"\n===== Running Case: {shipment_type} | {courier_purpose} | {flow_name} =====")
#
#             try:
#                 page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")
#                 page.wait_for_load_state("networkidle")
#
#                 create_shipment_ndr(page, data, shipment_type, courier_purpose)
#
#                 custref, awb_text = get_created_shipment_details(page)
#
#                 search_shipment_by_customer_ref(page, BASE_URL, custref)
#                 update_tracking_exception(page)
#                 search_shipment_by_customer_refexcep(page, BASE_URL, custref,awb_text)
#
#                 open_ndr_action(page)
#
#                 # ✅ CANCEL FLOW → skip everything else
#                 if flow_name == "RTO":
#                     RTOFUNC(page)
#                     print("✅ Cancel flow executed. Skipping remaining steps.")
#                 else:
#                     # ✅ Only RESCHEDULE and EDIT call this
#                     ndr_func(page)
#
#                 # ✅ Only for RESCHEDULE & EDIT
#
#
#                 status = confirm_ndr_action(page, awb_text, action_type=flow_name)
#
#                 if status == "ACTION_REQUIRED":
#                     print("🛑 Shipment is in Action Required. Moving to next case.")
#
#
#                 search_awb_in_ndr_action_requested(page, BASE_URL, awb_text)
#
#                 update_carrier_tracking_status(page, awb_text)
#
#
#
#                 print(f"✅ Completed: {shipment_type} | {courier_purpose} | {flow_name}")
#
#             except Exception as e:
#                 print("❌ Error occurred")
#                 print(f"Case: {shipment_type} | {courier_purpose} | {flow_name}")
#                 print(f"Error: {str(e)}")
#
#                 try:
#                     error_msg = page.locator("div[role='alert']").inner_text(timeout=3000)
#                     print(f"UI Error Message: {error_msg}")
#                 except:
#                     print("No UI error message captured")
#
#             finally:
#                 print("➡ Moving to next case...\n")




from utils.NDR_FUNCTIONS import (
    open_ndr_action,
    fill_NDR_reschedule_date,
    fill_NDR_edit_and_reschedule,
    RTOFUNC,
    confirm_ndr_action,
)

from utils.config import BASE_URL

from utils.NDR_FUNCTIONS import (
    get_created_shipment_details,
    search_shipment_by_customer_ref,
    open_ndr_action,
    confirm_ndr_action,
    search_awb_in_ndr_action_requested,
    fill_NDR_reschedule_date,
    fill_NDR_edit_and_reschedule,
    update_carrier_tracking_status,
    update_carrier_tracking_status_forRTO,   # ✅ ADDED
    RTOFUNC,
    update_tracking_exception,
)

from utils.shipment_functions_v2 import (
    load_shipment_data,
    create_shipment,
    create_shipment_ndr,
)

from eshipz_framework.utils.NDR_FUNCTIONS import (
    search_shipment_by_customer_refexcep
)


def test_NPR(logged_in_page):

    page = logged_in_page

    data = load_shipment_data()

    shipment_cases = [
        ("Parcel", "Commercial"),
    ]

    ndr_flows = [
        ("RE-ATTEMPT", fill_NDR_reschedule_date),
        ("EDIT_AND_RESCHEDULE", fill_NDR_edit_and_reschedule),
        ("RTO", RTOFUNC),
    ]

    for shipment_type, courier_purpose in shipment_cases:

        for flow_name, ndr_func in ndr_flows:

            print(
                f"\n===== Running Case: "
                f"{shipment_type} | "
                f"{courier_purpose} | "
                f"{flow_name} ====="
            )

            try:

                page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")

                page.wait_for_load_state("networkidle")

                create_shipment_ndr(
                    page,
                    data,
                    shipment_type,
                    courier_purpose
                )

                custref, awb_text = get_created_shipment_details(page)

                # ======================================================
                # SEARCH SHIPMENT
                # ======================================================

                search_shipment_by_customer_ref(
                    page,
                    BASE_URL,
                    custref
                )

                # ======================================================
                # UPDATE TRACKING EXCEPTION
                # ======================================================

                update_tracking_exception(page)

                # ======================================================
                # SEARCH IN EXCEPTION PAGE
                # ======================================================

                search_shipment_by_customer_refexcep(
                    page,
                    BASE_URL,
                    custref,
                    awb_text
                )

                # ======================================================
                # OPEN NDR ACTION
                # ======================================================

                open_ndr_action(page)

                # ======================================================
                # RTO FLOW
                # ======================================================

                if flow_name == "RTO":

                    RTOFUNC(page)

                    print(
                        "✅ RTO flow executed. "
                        "Skipping reschedule/edit steps."
                    )

                else:

                    # ==============================================
                    # RE-ATTEMPT / EDIT_AND_RESCHEDULE
                    # ==============================================

                    ndr_func(page)

                # ======================================================
                # CONFIRM NDR ACTION
                # ======================================================

                status = confirm_ndr_action(
                    page,
                    awb_text,
                    action_type=flow_name
                )

                if status == "ACTION_REQUIRED":

                    print(
                        "🛑 Shipment is in Action Required. "
                        "Moving to next case."
                    )

                # ======================================================
                # SEARCH IN ACTION REQUESTED
                # ======================================================

                search_awb_in_ndr_action_requested(
                    page,
                    BASE_URL,
                    awb_text
                )

                # ======================================================
                # TRACKING STATUS UPDATE
                # ======================================================

                # ✅ ONLY RTO CALLS THIS FUNCTION
                if flow_name == "RTO":

                    update_carrier_tracking_status_forRTO(
                        page,
                        awb_text
                    )

                else:

                    update_carrier_tracking_status(
                        page,
                        awb_text
                    )

                print(
                    f"✅ Completed: "
                    f"{shipment_type} | "
                    f"{courier_purpose} | "
                    f"{flow_name}"
                )

            except Exception as e:

                print("❌ Error occurred")

                print(
                    f"Case: "
                    f"{shipment_type} | "
                    f"{courier_purpose} | "
                    f"{flow_name}"
                )

                print(f"Error: {str(e)}")

                try:

                    error_msg = page.locator(
                        "div[role='alert']"
                    ).inner_text(timeout=3000)

                    print(f"UI Error Message: {error_msg}")

                except:

                    print("No UI error message captured")

            finally:

                print("➡ Moving to next case...\n")