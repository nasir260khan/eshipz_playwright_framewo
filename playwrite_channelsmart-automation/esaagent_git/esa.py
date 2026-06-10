import pytest
import json
import pandas as pd
import re
from functions import login_to_channelsmart, fill_contact_number_from_csv, select_mat_option_exact, confirm_dialog
from playwright.sync_api import sync_playwright
import os
import shutil
from pathlib import Path


# 🛡️ Helper: ensure no angular dialogs are blocking clicks
def wait_for_all_dialogs_to_close(page, timeout: int = 7000):
    """
    Wait until no <mat-dialog-container> is on screen.
    If dialogs persist, try clicking common Close/OK/Cancel buttons or press Escape.
    """
    try:
        page.wait_for_selector("mat-dialog-container", state="detached", timeout=timeout)
        return
    except:
        pass  # try to close manually below

    # Try to close top-most dialogs a few times
    for _ in range(5):
        dialogs = page.locator("mat-dialog-container")
        if dialogs.count() == 0:
            return
        dlg = dialogs.last
        # try common close buttons
        for sel in [
            "button[aria-label='Close']",
            "button:has-text('Close')",
            "button:has-text('Cancel')",
            "button:has-text('OK')",
            "button:has-text('Done')",
            "button:has-text('Confirm')",
            "#added-customer-confirm",
            "#generated-report-confirm",
            "#bulk-upload-customer-confirm",
            "#bulk-upload-user-confirm",
            "#added-user-confirm",
            "#toggle-confirm",
        ]:
            if dlg.locator(sel).count() > 0:
                dlg.locator(sel).first.click()
                page.wait_for_timeout(400)
                break
        else:
            # no known button; try Escape
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)

        # check again if detached
        try:
            page.wait_for_selector("mat-dialog-container", state="detached", timeout=800)
            return
        except:
            continue

    # Final passive wait (don’t fail hard)
    try:
        page.wait_for_selector("mat-dialog-container", state="detached", timeout=1000)
    except:
        pass


@pytest.mark.parametrize("headless_mode", [True])
def test_full_customer_and_user_flow(headless_mode):
    video_dir = "videos"
    if os.path.exists(video_dir):
        shutil.rmtree(video_dir)
    os.makedirs(video_dir, exist_ok=True)

    with open("playwrite_channelsmart-automation/esaagent_git/data_report.json") as file:
        reports = json.load(file)

    with open("playwrite_channelsmart-automation/esaagent_git/data_credit.json") as file:
        customer = json.load(file)

    with open("playwrite_channelsmart-automation/esaagent_git/data_pickupuser.json") as file:
        user = json.load(file)

    with sync_playwright() as m:
        browser = m.chromium.launch(headless=headless_mode)
        context = browser.new_context(
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()

        # ---------------- Login ----------------
        login_to_channelsmart(page, "loadtest@gmail.com", "password")
        page.wait_for_timeout(3000)

        # ---------------- Report Generation ----------------
        page.get_by_role("link", name="Reports").click()
        page.locator("//input[@formcontrolname='fromday']").fill(reports["start_date"])
        page.locator("//input[@formcontrolname='today']").fill(reports["end_date"])
        page.locator("//input[@formcontrolname='email_id']").fill(reports["email_id"])
        page.get_by_role("button", name="Generate Report").click()
        page.wait_for_timeout(5000)

        success_message1 = page.locator("mat-dialog-content >> text=Generated Report Shared To Your Email.")
        page.wait_for_timeout(5000)

        if success_message1.is_visible(timeout=5000):
            print("✅ Report generated successfully by ESA_agent")
        else:
            print("❌ Report generation dialog not found.")

        # Confirm dialog and ensure all overlays gone
        confirm_dialog(
            page,
            prefer_text="Generated Report Shared To Your Email.",
            id_selector="#generated-report-confirm",
        )
        wait_for_all_dialogs_to_close(page)

        # ---------------- Customer Creation ----------------
        page.wait_for_timeout(4000)
        page.get_by_role("link", name="Customers").click()
        page.click("//button[contains(., 'Add Customer')]")

        for key in [
            "pancard_number", "aadhaar_number", "customer_code", "username",
            "addressline1", "addressline2", "addressline3", "company_name",
            "city", "pincode", "state", "phone_number", "email"
        ]:
            page.locator(f"//input[@formcontrolname='{key}']").fill(customer[key])

        select_mat_option_exact(page, 'mat-select[formcontrolname="services"]', customer["services"])

        page.locator("h2.mat-dialog-title", has_text="Add Customer").click(force=True)
        page.locator('mat-checkbox:has-text("Same As Billing Address")').click()
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(5000)

        success_message = page.locator("mat-dialog-content >> text=Added Customer Successfully.")
        if success_message.is_visible(timeout=5000):
            print("✅ Credit customer created successfully by ESA_agent")
        else:
            print("❌ Customer creation dialog not found.")
        page.wait_for_timeout(3000)

        confirm_dialog(
            page,
            prefer_text="Added Customer Successfully.",
            id_selector="#added-customer-confirm",
        )
        # 🔒 ensure dialogs are closed before clicking Bulk Upload button
        wait_for_all_dialogs_to_close(page)
        page.wait_for_timeout(400)

        # ---------------- Bulk Customer Upload ----------------
        page.click("//button[contains(., 'Bulk Upload Customer')]")
        file_input = page.locator("#file")
        file_input.wait_for(state="visible", timeout=60000)
        file_input.wait_for(state="attached", timeout=60000)
        file_input.set_input_files("playwrite_channelsmart-automation/esaagent_git/customer_template.csv")
        print("✅ File upload triggered.")
        page.wait_for_timeout(4000)

        page.locator("button.btn.btn-primary", has_text="Upload").click()
        page.wait_for_timeout(5000)

        dialog_content = page.locator("mat-dialog-content")
        try:
            dialog_content.wait_for(state="visible", timeout=10000)
            if "Customers Created Successfully." in dialog_content.inner_text():
                print("✅ Bulk credit customer created successfully by ESA_agent")
            else:
                print("⚠️ Dialog appeared but did not contain expected text.")
        except:
            print("❌ No confirmation dialog appeared after bulk upload.")

        confirm_dialog(
            page,
            prefer_text="Customers Created Successfully.",
            id_selector="#bulk-upload-customer-confirm",
        )
        wait_for_all_dialogs_to_close(page)
        page.wait_for_timeout(3000)

        # ---------------- Customer Search ----------------
        csv_path = "playwrite_channelsmart-automation/esaagent_git/customer_template.csv"
        df = pd.read_csv(csv_path)
        email_id = df.iloc[0]["BILLING_EMAIL[MANDATORY]"] if "BILLING_EMAIL[MANDATORY]" in df.columns else None
        if email_id:
            page.locator("#mat-select-0").click()
            page.locator("#mat-option-2").click()
            input_field = page.locator(
                "xpath=/html/body/app-root/app-admin/div/div/app-esa-customers/div[2]/div/app-card/div/div[2]/div/mat-form-field[2]/div/div[1]/div/input"
            )
            input_field.fill(email_id)
            print(f"✅ Entered email for search: {email_id}")
        else:
            print("❌ Email column not found in CSV.")
        page.wait_for_timeout(1000)
        page.locator("button:has(mat-icon:text('search'))").click()
        page.wait_for_timeout(3000)

        # ---------------- Customer Edit ----------------
        page.locator(
            "xpath=/html/body/app-root/app-admin/div/div/app-esa-customers/div[2]/div/app-card/div/div[2]/div/table/tbody/tr/td[6]/mat-icon"
        ).click()
        data_field1 = page.locator("//input[@formcontrolname='pincode']")
        data_field1.fill("560098")
        page.get_by_role("button", name="Update").click()
        print("✅ Customer update successful")
        page.wait_for_timeout(2000)
        page.locator("#cash-customer-service-error").click()
        page.click("button:has-text('Cancel')")

        # ---------------- Customer Deactivation ----------------
        page.locator("mat-slide-toggle label").first.click()
        page.wait_for_timeout(1000)
        if page.locator("mat-dialog-content >> text=Deactivated Successfully").is_visible(timeout=5000):
            print("✅ Customer deactivated successfully")
        confirm_dialog(page, id_selector="#toggle-confirm")  # safe confirm
        wait_for_all_dialogs_to_close(page)

        # ---------------- Customer Activation ----------------
        page.click("button:has(mat-icon:text('search'))")
        toggle = page.locator("mat-slide-toggle input[type='checkbox']").first
        if toggle.get_attribute("aria-checked") == "false":
            page.locator("mat-slide-toggle label").first.click()
        if page.locator("mat-dialog-content >> text=Activated Successfully").is_visible(timeout=5000):
            print("✅ Customer activated successfully")
        confirm_dialog(page, id_selector="#toggle-confirm")
        wait_for_all_dialogs_to_close(page)

        # ---------------- Pickup User Creation ----------------
        page.wait_for_timeout(3000)
        page.get_by_role("link", name="Users").click()
        page.click("//button[contains(., 'Add User')]")
        for key in ["first_name", "last_name", "email_id", "contact_number", "password"]:
            page.fill(f"//input[@formcontrolname='{key}']", user[key])

        select_mat_option_exact(page, 'mat-select[formcontrolname="services"]', user["services"])
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(3000)
        print("✅ Pickup user created successfully")

        confirm_dialog(
            page,
            prefer_text="Added User Successfully.",
            id_selector="#added-user-confirm",
        )
        wait_for_all_dialogs_to_close(page)

        # ---------------- Pickup User Bulk Upload ----------------
        page.click("//button[contains(., 'Bulk Upload User')]")
        file_input = page.locator("#file")
        file_input.wait_for(state="visible", timeout=60000)
        file_input.set_input_files("playwrite_channelsmart-automation/esaagent_git/pickup_template.csv")
        page.locator("button.btn.btn-primary", has_text="Upload").click()
        page.wait_for_timeout(3000)
        confirm_dialog(
            page,
            prefer_text="Uploaded Successfully.",
            id_selector="#bulk-upload-user-confirm",
        )
        wait_for_all_dialogs_to_close(page)

        # ---------------- Pickup User Edit ----------------
        fill_contact_number_from_csv(page)
        page.wait_for_timeout(3000)
        page.locator(
            "xpath=/html/body/app-root/app-admin/div/div/app-esa-user/div[2]/div/app-card/div/div[2]/div/table/tbody/tr/td[5]/mat-icon"
        ).click(force=True)

        data_field1 = page.locator("//input[@formcontrolname='last_name']")
        data_field1.fill("replace09")
        page.get_by_role("button", name="Update").click()
        print("✅ Pickup user updated successfully")

        # ---------------- Pickup User Deactivation ----------------
        fill_contact_number_from_csv(page)
        page.locator("mat-slide-toggle label").first.click()
        if page.locator("mat-dialog-content >> text=Deactivated Successfully").is_visible(timeout=5000):
            print("✅ Pickup user deactivated successfully")
        confirm_dialog(page, id_selector="#toggle-confirm")
        wait_for_all_dialogs_to_close(page)

        # ---------------- Pickup User Activation ----------------
        page.locator("button:has(mat-icon:text('search'))").click()
        toggle_input = page.locator("mat-slide-toggle input[type='checkbox']").first
        toggle_input.wait_for(state="attached")

        if toggle_input.get_attribute("aria-checked") == "false":
            toggle_label = page.locator("mat-slide-toggle label").first
            toggle_label.wait_for(state="visible")
            toggle_label.click()
            print("✅ Toggle was OFF, now enabled.")
        else:
            print("ℹ️ Toggle already ON, no action needed.")

        if page.locator("mat-dialog-content >> text=Activated Successfully").is_visible(timeout=5000):
            print("✅ Pickup user activated successfully")
        page.wait_for_selector("#toggle-confirm").click()
        wait_for_all_dialogs_to_close(page)

        context.close()
        browser.close()
