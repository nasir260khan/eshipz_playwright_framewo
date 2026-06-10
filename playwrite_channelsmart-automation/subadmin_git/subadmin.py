import pytest
import json
import pandas as pd
from datetime import datetime
from functions import search_user_by_email_from_csv, login_to_channelsmart
from playwright.sync_api import sync_playwright
import os
import shutil
from pathlib import Path


# ✅ Helper to select an exact option from Angular Material <mat-select>
def select_mat_option_exact(page, select_selector: str, option_text: str):
    # Open the dropdown
    page.click(select_selector)
    # The options render in an overlay panel
    panel = page.locator("div.mat-select-panel")
    panel.wait_for(state="visible")

    # Prefer role=option with exact match
    opt = panel.get_by_role("option", name=option_text, exact=True)
    if opt.count() > 0:
        opt.first.click()
        return

    # Fallback: exact text inside mat-option
    panel.locator("mat-option").get_by_text(option_text, exact=True).click()


@pytest.mark.parametrize("headless_mode", [True])  # Set to True for GitHub Actions
def test_full_channelsmart_flow(headless_mode):
    video_dir = "videos"
    if os.path.exists(video_dir):
        shutil.rmtree(video_dir)
    os.makedirs(video_dir, exist_ok=True)

    with open("playwrite_channelsmart-automation/subadmin_git/data_report1.json") as file:
        # with open("data_report1.json", "r") as f:
        reports = json.load(file)
    with open("playwrite_channelsmart-automation/subadmin_git/data_user1.json") as file:
        # with open("data_user1.json", "r") as f:
        user = json.load(file)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_mode)
        context = browser.new_context(
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        # page = browser.new_page()

        # Login
        login_to_channelsmart(page, "subadminuat@gmail.com", "password")
        page.wait_for_timeout(2000)

        # ---------------- Reports ----------------
        page.get_by_role("link", name="Reports").click()
        page.wait_for_selector("//input[@formcontrolname='fromday']")
        page.fill("//input[@formcontrolname='fromday']", reports["start_date"])
        page.fill("//input[@formcontrolname='today']", reports["end_date"])
        page.fill("//input[@formcontrolname='email_id']", reports["email_id"])
        page.get_by_role("button", name='Generate Report').click()
        page.wait_for_timeout(5000)

        success_message6 = page.locator("mat-dialog-content >> text=Generated Report Shared To Your Email.")
        page.wait_for_timeout(1000)

        # Wait up to 5 seconds for the dialog to appear
        if success_message6.is_visible(timeout=7000):
            print("✅ Report generated successfully by sub_admin")
        else:
            print("❌ Report generation dialog not found.")
        page.click("#generated-report-confirm")
        page.wait_for_timeout(4000)

        # ---------------- User Creation ----------------
        page.wait_for_timeout(4000)
        page.get_by_role("link", name="Users").click()

        page.click("//button[contains(., 'Add User ')]")

        for key in [
            "esa_id", "password", "first_name", "last_name", "contact_number",
            "email_id", "address_1", "address_2", "address_3", "city",
            "state", "country", "country_code", "postal_code", "aadhaar_number",
            "license_key", "area_code", "login_id", "pu_code", "pu_name",
            "emp_name", "emp_code"
        ]:
            page.fill(f"//input[@formcontrolname='{key}']", user[key])

        # ✅ Exact option selection to avoid strict mode violations (e.g., Apex vs Apex_TDD)
        select_mat_option_exact(page, 'mat-select[formcontrolname="services"]', user["services"])

        page.locator("h2.mat-dialog-title", has_text="Add ESA User").click(force=True)
        page.get_by_role("button", name="Add").click()
        page.wait_for_timeout(4000)

        success_message = page.locator("mat-dialog-content >> text=Added User Successfully.")

        # Wait up to 5 seconds for the dialog to appear
        if success_message.is_visible(timeout=5000):
            print("✅ ESA-agent created successfully by sub_admin")
        else:
            print("❌ user creation dialog not found.")

        page.wait_for_selector("#added-user-confirm").click()
        page.wait_for_timeout(4000)

        # ---------------- Bulk Upload ----------------
        page.click("//button[contains(., 'Bulk Upload User')]")
        page.wait_for_timeout(5000)
        file_input = page.locator("#file")
        file_input.wait_for(state="visible", timeout=60000)
        file_input.wait_for(state="attached", timeout=60000)

        # Upload the file
        file_input.set_input_files("playwrite_channelsmart-automation/subadmin_git/esa_template.csv")
        print("✅ File upload triggered.")

        page.locator("button.btn.btn-primary", has_text="Upload").click()
        page.wait_for_timeout(3000)
        success_message = page.locator("mat-dialog-content >> text=Uploaded Successfully.")

        # Wait up to 5 seconds for the dialog to appear
        if success_message.is_visible(timeout=5000):
            print("✅ bulk esa-agent created successfully by sub_admin")
        else:
            print("❌ bulk-user creation dialog not found.")

        page.wait_for_selector("#bulk-upload-user-confirm").click()
        page.wait_for_timeout(3000)

        # ---------------- User Edit ----------------
        search_user_by_email_from_csv(page, "playwrite_channelsmart-automation/subadmin_git/esa_template.csv")
        page.wait_for_timeout(3000)
        page.click(
            "xpath=/html/body/app-root/app-admin/div/div/app-esa-user/div[2]/div/app-card/div/div[2]/div/table/tbody/tr/td[6]/mat-icon")
        page.fill("//input[@formcontrolname='last_name']", "replaced")
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="Update").click()
        page.wait_for_timeout(3000)

        # ---------------- Deactivate User ----------------
        search_user_by_email_from_csv(page, "playwrite_channelsmart-automation/subadmin_git/esa_template.csv")
        page.wait_for_timeout(3000)
        toggle_label = page.locator("mat-slide-toggle label").first
        toggle_label.wait_for(state="visible")

        # Click to toggle
        toggle_label.click()
        print("✅ Toggle clicked via label.")

        success_message2 = page.locator("mat-dialog-content >>text=Deactivated Successfully")
        page.wait_for_timeout(3000)

        if success_message2.is_visible(timeout=5000):
            print("✅ ESA-agent de-activated successfully by sub_admin")
        else:
            print("❌ user de-activation dialog not found.")
        page.wait_for_selector("#toggle-confirm").click()
        page.wait_for_timeout(1000)

        # ---------------- Activate User ----------------
        page.locator("button:has(mat-icon:text('search'))").click()
        page.wait_for_timeout(1000)
        toggle_input = page.locator("mat-slide-toggle input[type='checkbox']").first

        # Wait for it to be attached
        toggle_input.wait_for(state="attached")

        # Check if the toggle is OFF (disabled)
        if toggle_input.get_attribute("aria-checked") == "false":
            toggle_label = page.locator("mat-slide-toggle label").first
            toggle_label.wait_for(state="visible")
            toggle_label.click()
            print("✅ Toggle was OFF, now enabled.")
        else:
            print("ℹ️ Toggle is already ON. No action needed.")

        success_message3 = page.locator("mat-dialog-content >>text=Activated Successfully")
        page.wait_for_timeout(3000)

        if success_message3.is_visible(timeout=5000):
            print("✅ ESA-agent activated successfully by sub_admin")
        else:
            print("❌ user activation dialog not found.")
        page.wait_for_selector("#toggle-confirm").click()
        page.wait_for_timeout(3000)

        context.close()
        browser.close()
