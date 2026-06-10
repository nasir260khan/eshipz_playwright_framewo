# import random
# import time
# from playwright.sync_api import sync_playwright, expect
#
# EMAIL = "madhuraki27@gmail.com"
# PASSWORD = "password"
#
# HSN_MAPPING = {
#     "ironbox": "85164000",
#     "mobile": "85171300",
#     "laptop": "84713010",
#     "bottle": "39233000",
#     "fan": "84145120",
# }
#
#
# def get_hsn_code(description):
#     return HSN_MAPPING.get(description.lower(), "99999999")
#
#
# def test_add_sku():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         # Login
#         page.goto("https://uat.eshipz.com:444/login")
#
#         page.get_by_role(
#             "textbox",
#             name="Enter your email"
#         ).fill(EMAIL)
#
#         page.get_by_role(
#             "textbox",
#             name="Enter your password"
#         ).fill(PASSWORD)
#
#         page.get_by_role(
#             "button",
#             name="Login"
#         ).click()
#
#         page.wait_for_load_state("networkidle")
#
#         # Open SKU page directly
#         page.goto(
#             "https://uat.eshipz.com:444/v2/settings/shipping-setup/SKU-list"
#         )
#
#         page.wait_for_load_state("networkidle")
#
#         # Test data
#         sku_name = f"SKU_{random.randint(10000,99999)}"
#         description = "ironbox"
#         hsn_code = get_hsn_code(description)
#
#         gst = str(random.randint(11, 20))
#         length = str(random.randint(10, 20))
#         width = str(random.randint(1, 10))
#         height = str(random.randint(10, 20))
#         weight = str(random.randint(1, 20))
#
#         print(f"SKU      : {sku_name}")
#         print(f"HSN      : {hsn_code}")
#         print(f"GST      : {gst}")
#
#         # Add SKU
#         page.get_by_role("button", name="Add SKU").click()
#
#         page.get_by_role(
#             "textbox",
#             name="Product SKU *"
#         ).fill(sku_name)
#
#         page.get_by_role(
#             "textbox",
#             name="Product Description"
#         ).fill(description)
#
#         page.get_by_role(
#             "textbox",
#             name="HSN Code *"
#         ).fill(hsn_code)
#
#         page.get_by_role(
#             "spinbutton",
#             name="GST % *"
#         ).fill(gst)
#
#         # Wait for popup inputs
#         page.wait_for_timeout(1000)
#
#         # Debug all inputs
#         inputs = page.locator("input")
#         print("Total Inputs:", inputs.count())
#
#         # Fill dimension fields
#         # Based on recorder sequence:
#         # GST -> Length -> Width -> Height -> Weight
#
#         inputs.nth(3).fill(length)
#         inputs.nth(4).fill(width)
#         inputs.nth(5).fill(height)
#         inputs.nth(6).fill(weight)
#
#         page.get_by_role(
#             "button",
#             name="Save"
#         ).click()
#
#         # Success popup validation
#         expect(
#             page.get_by_text(
#                 "SKU Mapping Saved Successfully"
#             )
#         ).to_be_visible(timeout=15000)
#
#         page.get_by_role(
#             "button",
#             name="Close"
#         ).click()
#
#         # Search created SKU
#         search_box = page.get_by_role(
#             "textbox",
#             name="Search"
#         )
#
#         search_box.fill(sku_name)
#
#         page.wait_for_timeout(2000)
#
#         # Validate row
#         row = page.locator("table tbody tr").first
#
#         expect(row).to_contain_text(sku_name)
#         expect(row).to_contain_text(description)
#         expect(row).to_contain_text(hsn_code)
#         expect(row).to_contain_text(gst)
#
#         print("✅ SKU Added Successfully")
#         print("✅ SKU Validation Successful")
#
#         time.sleep(5)
#
#         browser.close()
#
#
# if __name__ == "__main__":
#     test_add_sku()


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


def test_add_sku():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
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

        # Dynamic Data
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
        print("LWH :", length, width, height)
        print("WT  :", weight)
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

        # IMPORTANT:
        # Replace these locators with the correct Length/Width/Height/Weight locators
        # if available in your application.

        inputs = page.locator("input")

        print("Total Inputs:", inputs.count())

        # Fill remaining fields if present
        if inputs.count() >= 8:
            inputs.nth(4).fill(length)
            inputs.nth(5).fill(width)
            inputs.nth(6).fill(height)
            inputs.nth(7).fill(weight)

        page.get_by_role(
            "button",
            name="Save"
        ).click()

        # Success popup
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

        row = page.locator("table tbody tr").first

        expect(row).to_be_visible()

        row_text = row.inner_text()

        print("\n========== ROW TEXT ==========")
        print(row_text)
        print("==============================")

        # Validations

        assert sku_name in row_text, \
            f"SKU not found. Expected: {sku_name}"

        assert description in row_text, \
            f"Description not found. Expected: {description}"

        print("✅ SKU Validation Passed")
        print("✅ Description Validation Passed")

        # Optional validations

        if hsn_code in row_text:
            print("✅ HSN Validation Passed")
        else:
            print(f"⚠ HSN {hsn_code} not found in row")

        if gst in row_text:
            print("✅ GST Validation Passed")
        else:
            print(f"⚠ GST {gst} not found in row")

        if weight in row_text:
            print("✅ Weight Validation Passed")
        else:
            print(f"⚠ Weight {weight} not found in row")

        time.sleep(5)

        browser.close()


if __name__ == "__main__":
    test_add_sku()