import random

# tests/test_bulk_import.py

import pytest
from pathlib import Path


from utils.generated_excel import generate_excel_file
from utils.labelvalidationfunction import extract_excel_text, extract_pdf_text





# @pytest.mark.bulk
# def test_bulk_import_and_create_shipment(logged_in_page):
#     # ---------------- LOGIN ---------------- #
#     page = logged_in_page
#
#     page.wait_for_load_state("networkidle")
#
#     # ---------------- NAVIGATION ---------------- #
#     page.get_by_role("heading", name="Create New Order").click()
#     page.get_by_role("button", name="Bulk").click()
#
#     # ---------------- EXCEL UPLOAD ---------------- #
#     excel_file, order_refs = generate_excel_file()
#     excel_path = Path(excel_file)
#
#     page.set_input_files("input[type='file']", excel_file)
#     page.locator("//button[normalize-space()='Import your orders']").click()
#     page.wait_for_timeout(5000)
#
#     # ---------------- SELECT ORDERS ---------------- #
#     for order_ref in order_refs:
#         row = page.locator(
#             f"//tr[.//text()[normalize-space()='{order_ref}']]"
#         )
#         checkbox = row.locator("xpath=.//button[@role='checkbox']")
#         checkbox.wait_for(state="visible", timeout=15000)
#
#         if checkbox.get_attribute("aria-checked") != "true":
#             checkbox.click()
#
#
#
#     # ---------------- CREATE SHIPMENT ---------------- #
#     page.get_by_role("button", name="Bulk Actions").click()
#     page.get_by_role("menuitem", name="Create Shipments").click()
#
#     page.get_by_role("button", name="Custom Ship").click()
#
#     # page.locator("#prepaid-carrier").click()
#     # page.get_by_role("option", name="Blue Dart").click()
#
#     carriers = ["India Post", "Blue Dart"]
#
#     # Click dropdown using ID
#     page.locator("#prepaid-carrier").click()
#
#     # Wait for options to load
#     page.wait_for_selector("li[role='option']")
#
#     # Select random carrier
#     page.get_by_role("option", name=random.choice(carriers)).click()
#
#     page.locator("#prepaid-vendor").click()
#     page.wait_for_selector("li[role='option']")
#
#     options = page.locator(
#         "li[role='option']:not([aria-disabled='true'])"
#     ).filter(has_not_text="Select")
#
#     random_index = random.randint(0, options.count() - 1)
#     selected_vendor = options.nth(random_index).inner_text()
#
#     options.nth(random_index).click()
#
#     print(f"Selected Vendor: {selected_vendor}")
#     # page.get_by_role("option", name="tblue").click()
#
#     page.locator("#prepaid-service").click()
#     page.locator("#prepaid-carrier").click()
#     page.get_by_role("option", name="Blue Dart").click()
#     page.locator("#prepaid-vendor").click()
#     page.get_by_role("option", name="revamp testing").click()
#     page.locator("#prepaid-service").click()
#     page.get_by_role("option", name="Apex").click()
#     page.get_by_role("combobox", name="Carrier", exact=True).click()
#     page.get_by_role("option", name="Blue Dart").click()
#     page.get_by_role("combobox", name="Vendor", exact=True).click()
#     page.get_by_role("option", name="revamp testing").click()
#     page.get_by_role("combobox", name="Service", exact=True).click()
#     page.get_by_role("option", name="eTail COD Air").click()
#     page.get_by_role("button", name="Ship Order").click()
#
#     # ---------------- DOWNLOAD LABEL ---------------- #
#     download_dir = Path("downloads")
#     download_dir.mkdir(exist_ok=True)
#
#     with page.expect_download(timeout=60000) as download_info:
#         page.get_by_role("button", name="Download Label").click()
#
#     download = download_info.value
#     label_path = download_dir / download.suggested_filename
#     download.save_as(label_path)
#
#     # ---------------- BASIC VALIDATION ---------------- #
#     assert label_path.exists(), "❌ Label not downloaded"
#     assert label_path.stat().st_size > 50 * 1024, "❌ Label file too small"
#
#     # ---------------- CONTENT VALIDATION ---------------- #
#     excel_values = extract_excel_text(excel_path)
#     pdf_text = extract_pdf_text(label_path)
#
#     matched, missing = [], []
#
#     for value in excel_values:
#         if value in pdf_text:
#             matched.append(value)
#         else:
#             missing.append(value)
#
#     # ---------------- REPORT (NO ASSERT) ---------------- #
#     print("\n========= LABEL CONTENT VALIDATION REPORT =========")
#
#     if matched:
#         print("\n✅ FOUND IN PDF:")
#         for v in matched:
#             print(f"   ✔ {v}")
#
#     if missing:
#         print("\n⚠️ MISSING IN PDF:")
#         for v in missing:
#             print(f"   ✖ {v}")
#
#     if not missing:
#         print("\n🎉 ALL EXCEL VALUES PRESENT")
#
#     print("==================================================")





# import random
# import re
# from pathlib import Path
#
# import pytest
# from playwright.sync_api import expect
#
#
# # =========================================================
# # RANDOM OPTION SELECTOR
# # =========================================================
#
# def select_random_option(
#         page,
#         dropdown_locator,
#         exclude_options=None
# ):
#
#     if exclude_options is None:
#         exclude_options = []
#
#     # CLICK DROPDOWN
#     page.locator(dropdown_locator).click()
#
#     page.wait_for_timeout(2000)
#
#     # WAIT OPTIONS
#     page.wait_for_selector("li[role='option']")
#
#     # GET OPTIONS
#     options = page.locator(
#         "li[role='option']:not([aria-disabled='true'])"
#     )
#
#     all_options = options.all_text_contents()
#
#     valid_options = []
#
#     for option in all_options:
#
#         option = option.strip()
#
#         if (
#                 option
#                 and option.lower() != "select"
#                 and option not in exclude_options
#         ):
#             valid_options.append(option)
#
#     if not valid_options:
#         raise Exception(
#             f"No valid options available "
#             f"for {dropdown_locator}"
#         )
#
#     # RANDOM SELECTION
#     selected_option = random.choice(valid_options)
#
#     page.get_by_role(
#         "option",
#         name=selected_option,
#         exact=True
#     ).click()
#
#     print(
#         f"✅ Selected {selected_option} "
#         f"from {dropdown_locator}"
#     )
#
#     return selected_option
#
#
# # =========================================================
# # SELECT RANDOM SHIPPING COMBINATION
# # =========================================================
#
# def select_random_shipping(page):
#
#     selected = {}
#
#     print(
#         "\n===== SELECTING RANDOM SHIPPING ====="
#     )
#
#     # =====================================================
#     # PREPAID
#     # =====================================================
#
#     print("\n--- PREPAID ---")
#
#     prepaid_carrier = select_random_option(
#         page,
#         "#prepaid-carrier"
#     )
#
#     selected["prepaid_carrier"] = prepaid_carrier
#
#     page.wait_for_timeout(1500)
#
#     prepaid_vendor = select_random_option(
#         page,
#         "#prepaid-vendor"
#     )
#
#     selected["prepaid_vendor"] = prepaid_vendor
#
#     page.wait_for_timeout(1500)
#
#     prepaid_service = select_random_option(
#         page,
#         "#prepaid-service"
#     )
#
#     selected["prepaid_service"] = prepaid_service
#
#     # =====================================================
#     # COD
#     # =====================================================
#
#     print("\n--- COD ---")
#
#     page.wait_for_timeout(1500)
#
#     cod_carrier = select_random_option(
#         page,
#         "#cod-carrier"
#     )
#
#     selected["cod_carrier"] = cod_carrier
#
#     page.wait_for_timeout(1500)
#
#     cod_vendor = select_random_option(
#         page,
#         "#cod-vendor"
#     )
#
#     selected["cod_vendor"] = cod_vendor
#
#     page.wait_for_timeout(1500)
#
#     cod_service = select_random_option(
#         page,
#         "#cod-service"
#     )
#
#     selected["cod_service"] = cod_service
#
#     return selected
#
#
# # =========================================================
# # FALLBACK INDIA POST SELECTION
# # =========================================================
#
# def fallback_india_post(page):
#
#     print(
#         "\n===== FALLBACK TO INDIA POST ====="
#     )
#
#     # =====================================================
#     # PREPAID
#     # =====================================================
#
#     print("\n--- PREPAID INDIA POST ---")
#
#     # CARRIER
#     page.locator("#prepaid-carrier").click()
#
#     page.get_by_role(
#         "option",
#         name=re.compile("India Post", re.I)
#     ).click()
#
#     page.wait_for_timeout(1500)
#
#     # VENDOR
#     try:
#
#         page.locator("#prepaid-vendor").click()
#
#         page.wait_for_selector("li[role='option']")
#
#         options = page.locator(
#             "li[role='option']:not([aria-disabled='true'])"
#         )
#
#         all_options = options.all_text_contents()
#
#         valid = [
#             x.strip()
#             for x in all_options
#             if x.strip().lower() != "select"
#         ]
#
#         if valid:
#
#             page.get_by_role(
#                 "option",
#                 name=valid[0],
#                 exact=True
#             ).click()
#
#             print(
#                 f"✅ Prepaid Vendor: {valid[0]}"
#             )
#
#     except Exception as e:
#
#         print(
#             f"Vendor selection failed: {str(e)}"
#         )
#
#     page.wait_for_timeout(1500)
#
#     # SERVICE
#     try:
#
#         page.locator("#prepaid-service").click()
#
#         page.wait_for_selector("li[role='option']")
#
#         options = page.locator(
#             "li[role='option']:not([aria-disabled='true'])"
#         )
#
#         all_options = options.all_text_contents()
#
#         valid = [
#             x.strip()
#             for x in all_options
#             if x.strip().lower() != "select"
#         ]
#
#         if valid:
#
#             page.get_by_role(
#                 "option",
#                 name=valid[0],
#                 exact=True
#             ).click()
#
#             print(
#                 f"✅ Prepaid Service: {valid[0]}"
#             )
#
#     except Exception as e:
#
#         print(
#             f"Service selection failed: {str(e)}"
#         )
#
#     # =====================================================
#     # COD
#     # =====================================================
#
#     print("\n--- COD INDIA POST ---")
#
#     page.wait_for_timeout(1500)
#
#     # CARRIER
#     page.locator("#cod-carrier").click()
#
#     page.get_by_role(
#         "option",
#         name=re.compile("India Post", re.I)
#     ).click()
#
#     page.wait_for_timeout(1500)
#
#     # VENDOR
#     try:
#
#         page.locator("#cod-vendor").click()
#
#         page.wait_for_selector("li[role='option']")
#
#         options = page.locator(
#             "li[role='option']:not([aria-disabled='true'])"
#         )
#
#         all_options = options.all_text_contents()
#
#         valid = [
#             x.strip()
#             for x in all_options
#             if x.strip().lower() != "select"
#         ]
#
#         if valid:
#
#             page.get_by_role(
#                 "option",
#                 name=valid[0],
#                 exact=True
#             ).click()
#
#             print(
#                 f"✅ COD Vendor: {valid[0]}"
#             )
#
#     except Exception as e:
#
#         print(
#             f"COD Vendor failed: {str(e)}"
#         )
#
#     page.wait_for_timeout(1500)
#
#     # SERVICE
#     try:
#
#         page.locator("#cod-service").click()
#
#         page.wait_for_selector("li[role='option']")
#
#         options = page.locator(
#             "li[role='option']:not([aria-disabled='true'])"
#         )
#
#         all_options = options.all_text_contents()
#
#         valid = [
#             x.strip()
#             for x in all_options
#             if x.strip().lower() != "select"
#         ]
#
#         if valid:
#
#             page.get_by_role(
#                 "option",
#                 name=valid[0],
#                 exact=True
#             ).click()
#
#             print(
#                 f"✅ COD Service: {valid[0]}"
#             )
#
#     except Exception as e:
#
#         print(
#             f"COD Service failed: {str(e)}"
#         )
#
#
# # =========================================================
# # SHIP ORDER WITH RETRY
# # =========================================================
#
# def ship_order_with_retry(page):
#
#     # =====================================================
#     # RANDOM SELECTION
#     # =====================================================
#
#     selected_data = select_random_shipping(page)
#
#     print(
#         "\n===== RANDOM SHIPPING SELECTED ====="
#     )
#
#     print(selected_data)
#
#     page.wait_for_timeout(3000)
#
#     # =====================================================
#     # CLICK SHIP ORDER
#     # =====================================================
#
#     page.get_by_role(
#         "button",
#         name="Ship Order"
#     ).click()
#
#     page.wait_for_timeout(8000)
#
#     # =====================================================
#     # CHECK FAILURE
#     # =====================================================
#
#     body_text = (
#         page.locator("body")
#         .text_content()
#         .lower()
#     )
#
#     failure_keywords = [
#         "failed",
#         "error",
#         "unable",
#         "not serviceable",
#         "shipment failed"
#     ]
#
#     failed = any(
#         keyword in body_text
#         for keyword in failure_keywords
#     )
#
#     # =====================================================
#     # RETRY WITH INDIA POST
#     # =====================================================
#
#     if failed:
#
#         print(
#             "\n❌ FIRST SHIPMENT FAILED"
#         )
#
#         retry_button = page.get_by_role(
#             "button",
#             name=re.compile(
#                 "Retry Failed",
#                 re.I
#             )
#         )
#
#         if retry_button.count() > 0:
#
#             retry_button.click()
#
#             page.wait_for_timeout(3000)
#
#         else:
#
#             page.get_by_role(
#                 "button",
#                 name="Custom Ship"
#             ).click()
#
#             page.wait_for_timeout(3000)
#
#         fallback_india_post(page)
#
#         page.wait_for_timeout(3000)
#
#         page.get_by_role(
#             "button",
#             name="Ship Order"
#         ).click()
#
#         page.wait_for_timeout(8000)
#
#         print(
#             "\n✅ RETRY COMPLETED "
#             "WITH INDIA POST"
#         )
#
#     else:
#
#         print(
#             "\n✅ SHIPMENT CREATED SUCCESSFULLY"
#         )
#
#
# # =========================================================
# # TEST CASE
# # =========================================================
#
# @pytest.mark.bulk
# def test_bulk_import_and_create_shipment(logged_in_page):
#
#     # ---------------- LOGIN ---------------- #
#
#     page = logged_in_page
#
#     page.wait_for_load_state("networkidle")
#
#     # ---------------- NAVIGATION ---------------- #
#
#     page.get_by_role(
#         "heading",
#         name="Create New Order"
#     ).click()
#
#     page.get_by_role(
#         "button",
#         name="Bulk"
#     ).click()
#
#     # ---------------- EXCEL UPLOAD ---------------- #
#
#     excel_file, order_refs = generate_excel_file()
#
#     excel_path = Path(excel_file)
#
#     page.set_input_files(
#         "input[type='file']",
#         excel_file
#     )
#
#     page.locator(
#         "//button[normalize-space()='Import your orders']"
#     ).click()
#
#     page.wait_for_timeout(5000)
#
#     # ---------------- SELECT ORDERS ---------------- #
#
#     for order_ref in order_refs:
#
#         row = page.locator(
#             f"//tr[.//text()[normalize-space()='{order_ref}']]"
#         )
#
#         checkbox = row.locator(
#             "xpath=.//button[@role='checkbox']"
#         )
#
#         checkbox.wait_for(
#             state="visible",
#             timeout=15000
#         )
#
#         if checkbox.get_attribute(
#                 "aria-checked"
#         ) != "true":
#
#             checkbox.click()
#
#     # ---------------- CREATE SHIPMENT ---------------- #
#
#     page.get_by_role(
#         "button",
#         name="Bulk Actions"
#     ).click()
#
#     page.get_by_role(
#         "menuitem",
#         name="Create Shipments"
#     ).click()
#
#     page.wait_for_timeout(3000)
#
#     # ---------------- CUSTOM SHIP ---------------- #
#
#     page.get_by_role(
#         "button",
#         name="Custom Ship"
#     ).click()
#
#     page.wait_for_timeout(3000)
#
#     # ---------------- SHIP WITH RETRY ---------------- #
#
#     ship_order_with_retry(page)
#
#     # ---------------- DOWNLOAD LABEL ---------------- #
#
#     download_dir = Path("downloads")
#
#     download_dir.mkdir(exist_ok=True)
#
#     with page.expect_download(
#             timeout=60000
#     ) as download_info:
#
#         page.get_by_role(
#             "button",
#             name="Download Label"
#         ).click()
#
#     download = download_info.value
#
#     label_path = (
#             download_dir
#             / download.suggested_filename
#     )
#
#     download.save_as(label_path)
#
#     # ---------------- BASIC VALIDATION ---------------- #
#
#     assert (
#         label_path.exists()
#     ), "❌ Label not downloaded"
#
#     assert (
#             label_path.stat().st_size
#             > 50 * 1024
#     ), "❌ Label file too small"
#
#     # ---------------- CONTENT VALIDATION ---------------- #
#
#     excel_values = extract_excel_text(
#         excel_path
#     )
#
#     pdf_text = extract_pdf_text(
#         label_path
#     )
#
#     matched = []
#     missing = []
#
#     for value in excel_values:
#
#         if value in pdf_text:
#
#             matched.append(value)
#
#         else:
#
#             missing.append(value)
#
#     # ---------------- REPORT ---------------- #
#
#     print(
#         "\n========= LABEL CONTENT "
#         "VALIDATION REPORT ========="
#     )
#
#     if matched:
#
#         print("\n✅ FOUND IN PDF:")
#
#         for v in matched:
#
#             print(f"   ✔ {v}")
#
#     if missing:
#
#         print("\n⚠️ MISSING IN PDF:")
#
#         for v in missing:
#
#             print(f"   ✖ {v}")
#
#     if not missing:
#
#         print(
#             "\n🎉 ALL EXCEL VALUES PRESENT"
#         )
#
#     print(
#         "=========================================="
#     )


import random
import time
from pathlib import Path

import pytest


# ============================================================
# RANDOM DROPDOWN SELECTOR
# ============================================================

def select_random_option(
        page,
        dropdown_selector,
        exclude_text=None
):

    page.locator(dropdown_selector).click()

    page.wait_for_selector(
        "li[role='option']",
        timeout=15000
    )

    options = page.locator(
        "li[role='option']"
    ).filter(
        has_not_text="Select"
    )

    all_options = []

    for i in range(options.count()):

        text = options.nth(i).inner_text().strip()

        if text and text != exclude_text:
            all_options.append(text)

    if not all_options:
        raise Exception(
            f"No options available for {dropdown_selector}"
        )

    selected = random.choice(all_options)

    page.get_by_role(
        "option",
        name=selected,
        exact=True
    ).click()

    print(f"✅ Selected: {selected}")

    return selected


# ============================================================
# SELECT PREPAID
# ============================================================

def select_prepaid(
        page,
        exclude_carrier=None
):

    print("\n========== PREPAID SELECTION ==========")

    prepaid_carrier = select_random_option(
        page,
        "#prepaid-carrier",
        exclude_text=exclude_carrier
    )

    prepaid_vendor = select_random_option(
        page,
        "#prepaid-vendor"
    )

    prepaid_service = select_random_option(
        page,
        "#prepaid-service"
    )

    return {
        "carrier": prepaid_carrier,
        "vendor": prepaid_vendor,
        "service": prepaid_service
    }


# ============================================================
# SELECT COD
# ============================================================

def select_cod(
        page,
        exclude_carrier=None
):

    print("\n========== COD SELECTION ==========")

    cod_carrier = select_random_option(
        page,
        "#cod-carrier",
        exclude_text=exclude_carrier
    )

    cod_vendor = select_random_option(
        page,
        "#cod-vendor"
    )

    cod_service = select_random_option(
        page,
        "#cod-service"
    )

    return {
        "carrier": cod_carrier,
        "vendor": cod_vendor,
        "service": cod_service
    }


# ============================================================
# CLOSE FAILED POPUP / OVERLAY
# ============================================================

def close_overlay_if_present(page):

    try:

        overlay = page.locator(
            "div.fixed.inset-0"
        )

        if overlay.count() > 0:

            print("⚠ Overlay detected")

            close_btn = page.locator(
                "button:has(svg)"
            ).last

            if close_btn.is_visible():
                close_btn.click()
                page.wait_for_timeout(2000)

    except Exception as e:
        print(f"Overlay close skipped: {e}")


# ============================================================
# SHIPMENT FAILURE CHECK
# ============================================================

def shipment_failed(page):

    page.wait_for_timeout(8000)

    body_text = page.locator(
        "body"
    ).text_content().lower()

    failure_keywords = [
        "failed",
        "error",
        "retry failed",
        "shipment failed",
        "unable",
    ]

    return any(
        keyword in body_text
        for keyword in failure_keywords
    )


# ============================================================
# SHIP ORDER WITH RETRY
# ============================================================

def ship_order_with_retry(page):

    # ---------------- FIRST ATTEMPT ---------------- #

    prepaid_data = select_prepaid(page)

    cod_data = select_cod(page)

    print("\n🚚 FIRST SHIPMENT ATTEMPT")

    page.get_by_role(
        "button",
        name="Ship Order"
    ).click()

    page.wait_for_timeout(10000)

    # ---------------- SUCCESS ---------------- #

    if not shipment_failed(page):

        print("✅ Shipment created successfully")
        return

    print("❌ FIRST SHIPMENT FAILED")

    # ====================================================
    # CLOSE FAILED MODAL / OVERLAY
    # ====================================================

    close_overlay_if_present(page)

    # ====================================================
    # CLICK CUSTOM SHIP AGAIN
    # ====================================================

    try:

        custom_ship_btn = page.get_by_role(
            "button",
            name="Custom Ship"
        )

        custom_ship_btn.wait_for(
            state="visible",
            timeout=20000
        )

        custom_ship_btn.click()

    except Exception:

        # fallback JS click

        page.locator(
            "button:has-text('Custom Ship')"
        ).evaluate(
            "el => el.click()"
        )

    page.wait_for_timeout(4000)

    # ====================================================
    # SECOND ATTEMPT
    # FORCE INDIA POST IF FIRST FAILED
    # ====================================================

    print("\n🔁 RETRYING WITH DIFFERENT CARRIER")

    # PREPAID

    page.locator("#prepaid-carrier").click()

    page.get_by_role(
        "option",
        name="India Post"
    ).click()

    prepaid_vendor = select_random_option(
        page,
        "#prepaid-vendor"
    )

    prepaid_service = select_random_option(
        page,
        "#prepaid-service"
    )

    # COD

    page.locator("#cod-carrier").click()

    page.get_by_role(
        "option",
        name="India Post"
    ).click()

    cod_vendor = select_random_option(
        page,
        "#cod-vendor"
    )

    cod_service = select_random_option(
        page,
        "#cod-service"
    )

    # ====================================================
    # SHIP AGAIN
    # ====================================================

    print("\n🚚 SECOND SHIPMENT ATTEMPT")

    page.get_by_role(
        "button",
        name="Ship Order"
    ).click()

    page.wait_for_timeout(15000)

    if shipment_failed(page):

        raise Exception(
            "❌ Shipment failed again after retry"
        )

    print("✅ Shipment success after retry")


# ============================================================
# MAIN TEST
# ============================================================

@pytest.mark.bulk
def test_bulk_import_and_create_shipment(logged_in_page):

    # ---------------- LOGIN ---------------- #

    page = logged_in_page



    # ---------------- NAVIGATION ---------------- #

    page.get_by_role(
        "heading",
        name="Create New Order"
    ).click()

    page.get_by_role(
        "button",
        name="Bulk"
    ).click()

    # ---------------- EXCEL UPLOAD ---------------- #

    excel_file, order_refs = generate_excel_file()

    excel_path = Path(excel_file)

    page.set_input_files(
        "input[type='file']",
        excel_file
    )

    page.locator(
        "//button[normalize-space()='Import your orders']"
    ).click()



    # ---------------- SELECT ORDERS ---------------- #

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

    # ---------------- CREATE SHIPMENT ---------------- #

    page.get_by_role(
        "button",
        name="Bulk Actions"
    ).click()

    page.get_by_role(
        "menuitem",
        name="Create Shipments"
    ).click()

    page.wait_for_timeout(5000)

    # ---------------- CUSTOM SHIP ---------------- #

    page.get_by_role(
        "button",
        name="Custom Ship"
    ).click()

    page.wait_for_timeout(3000)

    # ---------------- SHIP WITH RETRY ---------------- #

    ship_order_with_retry(page)

    # ==================================================
    # DOWNLOAD LABEL
    # ==================================================

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

    # ==================================================
    # VALIDATION
    # ==================================================

    assert label_path.exists()

    print("\n✅ LABEL DOWNLOADED SUCCESSFULLY")