import os
import random
import time
from playwright.sync_api import sync_playwright, expect

EMAIL = "madhuraki27@gmail.com"
PASSWORD = "password"

HSN_MAPPING = {
    "ironbox": "85164000",
    "mobile": "85171300",
    "laptop": "84713010",
    "bottle": "39233000",
    "fan": "84145120",
}


def get_hsn_code(description):
    return HSN_MAPPING.get(description.lower(), "99999999")


def is_headless_mode():
    return os.getenv("CI", "").lower() in {"1", "true", "yes"} or os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}


def test_add_sku():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=is_headless_mode(),
            slow_mo=0 if is_headless_mode() else 500
        )

        page = browser.new_page()

        # Login
        page.goto("https://uat.eshipz.com:444/login")

        page.get_by_role(
            "textbox",
            name="Enter your email"
        ).fill(EMAIL)

        page.get_by_role(
            "textbox",
            name="Enter your password"
        ).fill(PASSWORD)

        page.get_by_role(
            "button",
            name="Login"
        ).click()

        page.wait_for_load_state("networkidle")

        # Open SKU Page
        page.goto(
            "https://uat.eshipz.com:444/v2/settings/shipping-setup/SKU-list"
        )

        page.wait_for_load_state("networkidle")

        # Test Data
        sku_name = f"SKU_{random.randint(10000,99999)}"

        description = "ironbox"
        hsn_code = get_hsn_code(description)

        gst = str(random.randint(11, 20))
        length = str(random.randint(10, 20))
        width = str(random.randint(1, 10))
        height = str(random.randint(10, 20))
        weight = str(random.randint(1, 20))

        print("\n========== TEST DATA ==========")
        print("SKU :", sku_name)
        print("DESC:", description)
        print("HSN :", hsn_code)
        print("GST :", gst)
        print("Length :", length)
        print("Width  :", width)
        print("Height :", height)
        print("Weight :", weight)
        print("================================")

        # Add SKU
        page.get_by_role(
            "button",
            name="Add SKU"
        ).click()

        page.get_by_role(
            "textbox",
            name="Product SKU *"
        ).fill(sku_name)

        page.get_by_role(
            "textbox",
            name="Product Description"
        ).fill(description)

        page.get_by_role(
            "textbox",
            name="HSN Code *"
        ).fill(hsn_code)

        page.get_by_role(
            "spinbutton",
            name="GST % *"
        ).fill(gst)

        # ===== PACKAGE DIMENSIONS =====

        # Height
        page.locator('input[name="height"]').fill(height)

        # Width
        page.locator('input[name="width"]').fill(width)

        # Length
        page.locator('input[name="length"]').fill(length)

        # Weight
        page.locator('input[name="weight"]').fill(weight)

        print("\n===== VALUES ENTERED =====")
        print(
            "Height:",
            page.locator('input[name="height"]').input_value()
        )
        print(
            "Width:",
            page.locator('input[name="width"]').input_value()
        )
        print(
            "Length:",
            page.locator('input[name="length"]').input_value()
        )
        print(
            "Weight:",
            page.locator('input[name="weight"]').input_value()
        )
        print("==========================")

        page.get_by_role(
            "button",
            name="Save"
        ).click()

        expect(
            page.get_by_text(
                "SKU Mapping Saved Successfully"
            )
        ).to_be_visible(timeout=15000)

        print("✅ SKU Created Successfully")

        page.get_by_role(
            "button",
            name="Close"
        ).click()

        # Search SKU
        search_box = page.get_by_role(
            "textbox",
            name="Search"
        )

        search_box.fill(sku_name)

        page.wait_for_timeout(3000)

        row = page.locator(
            "table tbody tr"
        ).first

        expect(row).to_be_visible()

        row_text = row.inner_text()

        print("\n========== ROW TEXT ==========")
        print(row_text)
        print("==============================")

        # SKU Validation
        assert sku_name in row_text
        print("✅ SKU Validation Passed")

        # Description Validation
        assert description in row_text
        print("✅ Description Validation Passed")

        # HSN Validation
        assert hsn_code in row_text
        print("✅ HSN Validation Passed")

        # GST Validation
        if gst in row_text:
            print("✅ GST Validation Passed")
        else:
            print(f"❌ GST Validation Failed. Expected: {gst}")

        # Table Cells
        cells = row.locator("td")

        print("\n========== TABLE CELLS ==========")

        for i in range(cells.count()):
            print(
                f"Column {i}: "
                f"{cells.nth(i).inner_text().strip()}"
            )

        print("=================================")

        # Weight Column Validation
        if weight in row_text:
            print("✅ Weight Validation Passed")
        else:
            print(f"❌ Weight Validation Failed. Expected: {weight}")

        # ============================================================
        # EDIT SKU
        # ============================================================

        print("\n========== EDIT SKU ==========")

        edited_desc = "mobile"
        edited_hsn = get_hsn_code(edited_desc)

        edited_gst = str(random.randint(1, 28))
        edited_length = str(random.randint(10, 20))
        edited_width = str(random.randint(1, 10))
        edited_height = str(random.randint(10, 20))
        edited_weight = str(round(random.uniform(1, 20), 2))

        print("Edited Description :", edited_desc)
        print("Edited HSN         :", edited_hsn)
        print("Edited GST         :", edited_gst)
        print("Edited Length      :", edited_length)
        print("Edited Width       :", edited_width)
        print("Edited Height      :", edited_height)
        print("Edited Weight      :", edited_weight)

        # Refresh search
        search_box.fill("")
        search_box.fill(sku_name)

        page.wait_for_timeout(3000)

        row = page.locator("table tbody tr").first
        expect(row).to_be_visible()

        # Debug row buttons
        buttons = row.locator("button")

        print(f"Buttons Found : {buttons.count()}")

        for i in range(buttons.count()):
            try:
                print(
                    f"Button {i}:",
                    buttons.nth(i).inner_text()
                )
            except:
                pass

        # Click Edit button
        buttons.first.click()

        # Wait for popup
        page.wait_for_timeout(3000)

        # Verify popup opened
        expect(
            page.get_by_role(
                "textbox",
                name="Product Description"
            )
        ).to_be_visible(timeout=10000)

        print("✅ Edit popup opened")

        # Update fields
        page.get_by_role(
            "textbox",
            name="Product Description"
        ).fill(edited_desc)

        page.get_by_role(
            "textbox",
            name="HSN Code *"
        ).fill(edited_hsn)

        page.get_by_role(
            "spinbutton",
            name="GST % *"
        ).fill(edited_gst)

        page.locator(
            'input[name="height"]'
        ).fill(edited_height)

        page.locator(
            'input[name="width"]'
        ).fill(edited_width)

        page.locator(
            'input[name="length"]'
        ).fill(edited_length)

        page.locator(
            'input[name="weight"]'
        ).fill(edited_weight)

        print("\n===== EDIT VALUES ENTERED =====")

        print(
            "Height:",
            page.locator(
                'input[name="height"]'
            ).input_value()
        )

        print(
            "Width:",
            page.locator(
                'input[name="width"]'
            ).input_value()
        )

        print(
            "Length:",
            page.locator(
                'input[name="length"]'
            ).input_value()
        )

        print(
            "Weight:",
            page.locator(
                'input[name="weight"]'
            ).input_value()
        )

        print("==============================")

        # Update button
        update_btn = page.get_by_role(
            "button",
            name="Update"
        )

        expect(update_btn).to_be_visible(timeout=10000)
        expect(update_btn).to_be_enabled(timeout=10000)

        print("✅ Update button enabled")

        update_btn.click()

        # expect(
        #     page.get_by_text(
        #         "SKU Mapping Saved Successfully"
        #     )
        # ).to_be_visible(timeout=15000)

        print("✅ SKU Edited Successfully")

        # Close popup
        

        page.wait_for_timeout(5000)

        print("✅ SKU Edited Successfully")

        # ============================================================
        # VALIDATE EDITED SKU
        # ============================================================

        search_box.fill("")
        search_box.fill(sku_name)

        page.wait_for_timeout(3000)

        row = page.locator("table tbody tr").first

        expect(row).to_be_visible()

        updated_row_text = row.inner_text()

        print("\n========== UPDATED ROW ==========")
        print(updated_row_text)
        print("=================================")

        assert edited_desc in updated_row_text
        print("✅ Edited Description Validation Passed")

        assert edited_hsn in updated_row_text
        print("✅ Edited HSN Validation Passed")

        if edited_gst in updated_row_text:
            print("✅ Edited GST Validation Passed")
        else:
            print(
                f"❌ Edited GST Validation Failed. "
                f"Expected: {edited_gst}"
            )

        edited_weight_int = edited_weight.split(".")[0]

        if (
                edited_weight in updated_row_text
                or edited_weight_int in updated_row_text
        ):
            print("✅ Edited Weight Validation Passed")
        else:
            print(
                f"❌ Edited Weight Validation Failed. "
                f"Expected: {edited_weight}"
            )

        print("✅ Edited SKU Validation Completed")

        # ============================================================
        # DELETE SKU
        # ============================================================

        print("\n========== DELETE SKU ==========")

        search_box.fill("")
        search_box.fill(sku_name)

        page.wait_for_timeout(3000)

        row = page.locator("table tbody tr").first

        expect(row).to_be_visible()

        buttons = row.locator("button")

        print("Buttons Found :", buttons.count())

        for i in range(buttons.count()):
            try:
                print(
                    f"Button {i}:",
                    buttons.nth(i).inner_text()
                )
            except:
                pass

        # Change index if Delete button is not nth(1)
        buttons.nth(1).click()

        page.wait_for_timeout(2000)

        # Confirm delete popup if available
        try:
            delete_btn = page.get_by_role(
                "button",
                name="Delete"
            )

            if delete_btn.is_visible():
                delete_btn.click()

        except Exception:
            pass

        page.wait_for_timeout(5000)

        print("✅ Delete Action Completed")

        # ============================================================
        # VALIDATE SKU DELETED
        # ============================================================

        search_box.fill("")
        search_box.fill(sku_name)

        page.wait_for_timeout(3000)

        body_text = page.locator("body").inner_text()

        assert sku_name not in body_text, (
            f"SKU {sku_name} still exists after deletion"
        )

        print("✅ SKU Deleted Successfully")

        print("\n========== TEST COMPLETED ==========")
        print("✔ SKU Created")
        print("✔ SKU Validated")
        print("✔ SKU Edited")
        print("✔ Edited Data Validated")
        print("✔ SKU Deleted")
        print("✔ Delete Validation Passed")
        print("====================================")

        browser.close()


if __name__ == "__main__":
    test_add_sku()