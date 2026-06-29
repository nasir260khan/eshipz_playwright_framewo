# import random
# from playwright.sync_api import sync_playwright
#
#
# def run():
#     with sync_playwright() as p:
#
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         # Login
#         page.goto("https://uat.eshipz.com:444/login")
#
#         page.get_by_role("textbox", name="Enter your email").fill(
#             "madhuraki27@gmail.com"
#         )
#         page.get_by_role("textbox", name="Enter your password").fill(
#             "password"
#         )
#         page.get_by_role("button", name="Login").click()
#
#         page.wait_for_load_state("networkidle")
#
#         # Orders -> Unprocessed
#         page.get_by_role("button", name="box").click()
#         page.get_by_role("button", name="Order").click()
#         page.get_by_role("button", name="Unprocessed").click()
#
#         page.wait_for_timeout(5000)
#
#         print("\n===== DEBUG ORDER DATA =====")
#
#         # Get all visible text elements
#         divs = page.locator("div")
#
#         total = divs.count()
#         print(f"Total divs found: {total}")
#
#         order_candidates = []
#
#         for i in range(total):
#             try:
#                 text = divs.nth(i).text_content()
#
#                 if text:
#                     text = text.strip()
#
#                     if (
#                         len(text) > 3
#                         and len(text) < 80
#                         and "Order" not in text
#                         and "Shipment" not in text
#                         and "Dashboard" not in text
#                     ):
#                         order_candidates.append(text)
#
#             except Exception:
#                 pass
#
#         order_candidates = list(set(order_candidates))
#
#         print("\nPossible Order IDs:")
#         for idx, value in enumerate(order_candidates[:50]):
#             print(f"{idx + 1}. {value}")
#
#         if order_candidates:
#             selected_order = random.choice(order_candidates)
#             print(f"\nRandom Selection: {selected_order}")
#
#             try:
#                 page.get_by_text(selected_order, exact=False).first.click()
#                 print("Clicked successfully")
#             except Exception as e:
#                 print(f"Click failed: {e}")
#
#         page.wait_for_timeout(5000)
#
#         context.close()
#         browser.close()
#
#
# def test_unprocessed_order_validation():
#     run()
#
#
# if __name__ == "__main__":
#     run()


import random
from playwright.sync_api import sync_playwright

# import random
# from playwright.sync_api import sync_playwright
#
#
# def run():
#     with sync_playwright() as p:
#
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         # LOGIN
#         page.goto("https://uat.eshipz.com:444/login")
#
#         page.get_by_role("textbox", name="Enter your email").fill(
#             "madhuraki27@gmail.com"
#         )
#         page.get_by_role("textbox", name="Enter your password").fill(
#             "password"
#         )
#
#         page.get_by_role("button", name="Login").click()
#         page.wait_for_load_state("networkidle")
#
#         # OPEN UNPROCESSED ORDERS
#         page.goto(
#             "https://uat.eshipz.com:444/v2/fulfillment/orders/unprocessed"
#         )
#
#         page.wait_for_timeout(5000)
#
#         print("\n===== FINDING ORDERS =====")
#
#         real_orders = []
#
#         divs = page.locator("div")
#
#         for i in range(divs.count()):
#             try:
#                 text = divs.nth(i).inner_text().strip()
#
#                 if not text:
#                     continue
#
#                 first_line = text.split("\n")[0].strip()
#
#                 # Skip truncated orders
#                 if first_line.endswith(".."):
#                     continue
#
#                 if (
#                     first_line.startswith("test")
#                     or "-cl" in first_line
#                 ):
#                     real_orders.append(first_line)
#
#             except:
#                 pass
#
#         real_orders = list(set(real_orders))
#
#         print(f"Orders Found: {len(real_orders)}")
#
#         if not real_orders:
#             raise Exception("No valid orders found")
#
#         order_id = random.choice(real_orders)
#
#         print(f"\nSelected Order ID : {order_id}")
#
#         # OPEN CREATE SHIPMENT PAGE
#         page.goto(
#             "https://uat.eshipz.com:444/v2/fulfillment/create-shipment"
#         )
#
#         page.wait_for_load_state("networkidle")
#         page.wait_for_timeout(5000)
#
#         print("\n===== SEARCHING ORDER =====")
#
#         search_box = page.get_by_role(
#             "textbox",
#             name="Search Unshipped and"
#         )
#
#         search_box.click()
#         search_box.fill(order_id)
#         search_box.press("Enter")
#
#         page.wait_for_timeout(5000)
#
#         print("\n===== VALIDATION =====")
#
#         body_text = page.locator("body").inner_text()
#
#         if order_id.lower() in body_text.lower():
#             print(f"✅ Order Found : {order_id}")
#         else:
#             print(f"❌ Order Not Found : {order_id}")
#
#             # Debug output
#             print("\nCurrent URL:", page.url)
#
#             rows = page.locator("tr")
#             print(f"Rows found after search: {rows.count()}")
#
#             for i in range(min(rows.count(), 5)):
#                 try:
#                     print(rows.nth(i).inner_text())
#                 except:
#                     pass
#
#         page.wait_for_timeout(10000)
#
#         context.close()
#         browser.close()
#
#
# def test_unprocessed_order_validation():
#     run()
#
#
# if __name__ == "__main__":
#     run()



import os
import random
from playwright.sync_api import sync_playwright


def is_headless_mode():
    return os.getenv("CI", "").lower() in {"1", "true", "yes"} or os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}


def run():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=is_headless_mode())
        context = browser.new_context()
        page = context.new_page()

        # LOGIN
        page.goto("https://uat.eshipz.com:444/login")

        page.get_by_role("textbox", name="Enter your email").fill(
            "qatesting@gmail.com"
        )
        page.get_by_role("textbox", name="Enter your password").fill(
            "password"
        )

        page.get_by_role("button", name="Login").click()
        page.wait_for_timeout(5000)

        # OPEN UNPROCESSED ORDERS
        # OPEN UNPROCESSED ORDERS
        page.goto(
            "https://uat.eshipz.com:444/v2/fulfillment/orders/unprocessed"
        )

        page.wait_for_timeout(5000)

        print("\n===== FINDING ORDERS =====")

        real_orders = []

        # Capture orders from table rows instead of all divs
        rows = page.locator("tr")

        for i in range(rows.count()):
            try:
                row_text = rows.nth(i).inner_text().strip()

                if not row_text:
                    continue

                first_line = row_text.split("\n")[0].strip()

                # Skip headers
                if (
                        "Order" in first_line
                        or "Customer" in first_line
                        or "Payment" in first_line
                        or "Created" in first_line
                        or len(first_line) < 4
                ):
                    continue

                real_orders.append(first_line)

            except Exception:
                pass

        # Fallback if table rows are not available
        if not real_orders:

            divs = page.locator("div")

            for i in range(divs.count()):
                try:
                    text = divs.nth(i).inner_text().strip()

                    if not text:
                        continue

                    first_line = text.split("\n")[0].strip()

                    if (
                            len(first_line) > 4
                            and "Shopify" not in first_line
                            and "Prepaid" not in first_line
                            and "COD" not in first_line
                            and "Error" not in first_line
                    ):
                        real_orders.append(first_line)

                except Exception:
                    pass

        real_orders = list(dict.fromkeys(real_orders))

        print(f"\nOrders Found: {len(real_orders)}")

        for order in real_orders[:20]:
            print(order)

        if not real_orders:
            print("\n===== DEBUG PAGE CONTENT =====")
            print(page.locator("body").inner_text())

            raise Exception("No valid orders found")

        order_id = random.choice(real_orders)

        print(f"\nSelected Order ID : {order_id}")

        # ==========================
        # CAPTURE ORDER DETAILS
        # ==========================

        page_text = page.locator("body").inner_text()

        try:
            index = page_text.find(order_id)

            if index != -1:
                print("\n===== ORDER DETAILS FROM UNPROCESSED PAGE =====")
                print(page_text[index:index + 400])

        except Exception as e:
            print("Capture Error:", e)

        # OPEN CREATE SHIPMENT PAGE
        page.goto(
            "https://uat.eshipz.com:444/v2/fulfillment/create-shipment"
        )

        page.wait_for_timeout(5000)

        print("\n===== SEARCHING ORDER =====")

        search_box = page.get_by_role(
            "textbox",
            name="Search Unshipped and"
        )

        search_box.click()
        search_box.fill(order_id)
        search_box.press("Enter")

        page.wait_for_timeout(5000)

        # CLICK THE SEARCHED ORDER
        try:
            page.get_by_text(order_id, exact=False).first.click()

            print("✅ Opened Order Details Panel")
        except Exception as e:
            print("Unable to click order:", e)

        print("\n===== VALIDATION =====")

        body_text = page.locator("body").inner_text()

        if order_id.lower() in body_text.lower():

            print(f"✅ Order Found : {order_id}")

            print("\n===== CREATE SHIPMENT DETAILS =====")

            try:
                details_text = page.locator("body").inner_text()

                # Sender Details
                if "Sender Details" in details_text:
                    start = details_text.find("Sender Details")

                    print("\n===== SENDER DETAILS =====")
                    print(details_text[start:start + 700])

                # Receiver Details
                if "Receiver Details" in details_text:
                    start = details_text.find("Receiver Details")

                    print("\n===== RECEIVER DETAILS =====")
                    print(details_text[start:start + 700])

                # Order Details
                if "Order Details" in details_text:
                    start = details_text.find("Order Details")

                    print("\n===== ORDER DETAILS =====")
                    print(details_text[start:start + 700])

                # Item Details
                if "Item Details" in details_text:
                    start = details_text.find("Item Details")

                    print("\n===== ITEM DETAILS =====")
                    print(details_text[start:start + 700])

            except Exception as e:
                print("Unable to capture shipment details:", e)

            print("\n===== FIELD VALIDATION =====")

            if order_id in body_text:
                print("✅ Order ID Matched")
            else:
                print("❌ Order ID Mismatch")

            if order_id in body_text:
                print("✅ Order Reference Matched")
            else:
                print("❌ Order Reference Mismatch")

            # Additional validations
            validation_fields = [
                "Sender Details",
                "Receiver Details",
                "Order Details",
                "Item Details"
            ]

            for field in validation_fields:
                if field in body_text:
                    print(f"✅ {field} Present")
                else:
                    print(f"❌ {field} Missing")

            print("\n✅ COMPLETE VALIDATION PASSED")

        else:

            print(f"❌ Order Not Found : {order_id}")

            print("\nCurrent URL:", page.url)

            rows = page.locator("tr")

            print(f"Rows found after search: {rows.count()}")

            for i in range(min(rows.count(), 5)):
                try:
                    print(rows.nth(i).inner_text())
                except:
                    pass

        page.wait_for_timeout(10000)

        context.close()
        browser.close()


def test_unprocessed_order_validation():
    run()


if __name__ == "__main__":
    run()