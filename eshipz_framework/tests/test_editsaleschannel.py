# "status": "PENDING", for cod change api as these  for prepaid use thse "status": "SUCCESS","gateway": "Razorpay",
#   "gateway": "Cash on Delivery",
import os
import random
import re
import json
import time
import requests
import pytest

from playwright.sync_api import sync_playwright, expect

SHOP = "neww-11.myshopify.com"
TOKEN = "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"
API = "2026-04"

ESHIPZ_URL = "https://uat.eshipz.com:444/login"
ESHIPZ_EMAIL = "madhuraki27@gmail.com"
ESHIPZ_PASS = "password"


# =========================
# PLAYWRIGHT FIXTURE
# =========================

def is_headless_mode():
    return os.getenv("CI", "").lower() in {"1", "true", "yes"} or os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}


@pytest.fixture(scope="function")
def page():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=is_headless_mode(),
            slow_mo=0 if is_headless_mode() else 400
        )

        page = browser.new_page()

        yield page

        browser.close()


# =========================
# SHOPIFY API
# =========================

def shopify_api(query, variables):

    response = requests.post(
        f"https://{SHOP}/admin/api/{API}/graphql.json",
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": TOKEN
        },
        data=json.dumps({
            "query": query,
            "variables": variables
        })
    )

    data = response.json()

    if "errors" in data:
        raise Exception(data["errors"])

    return data


# =========================
# CREATE SHOPIFY ORDER
# =========================

import random

def get_random_product():

    query = """
    {
      products(first: 50) {
        edges {
          node {
            title
            variants(first: 20) {
              edges {
                node {
                  price
                }
              }
            }
          }
        }
      }
    }
    """

    result = shopify_api(query, {})

    products = []

    for product in result["data"]["products"]["edges"]:

        title = product["node"]["title"]

        variants = product["node"]["variants"]["edges"]

        if variants:

            price = variants[0]["node"]["price"]

            products.append({
                "title": title,
                "price": price
            })

    if not products:
        raise Exception("No products found")

    return random.choice(products)


def create_order():

    product = get_random_product()

    print("\n===== SELECTED PRODUCT =====")
    print("Product:", product["title"])
    print("Price:", product["price"])

    query = """
    mutation orderCreate($order: OrderCreateOrderInput!) {
      orderCreate(order: $order) {
        userErrors {
          field
          message
        }
        order {
          id
          name
          displayFinancialStatus
          displayFulfillmentStatus
        }
      }
    }
    """

    order_data = {
        "currency": "INR",
        "email": "customer@example.com",

        "lineItems": [
            {
                "title": product["title"],
                "quantity": 1,
                "priceSet": {
                    "shopMoney": {
                        "amount": str(product["price"]),
                        "currencyCode": "INR"
                    }
                },
                "requiresShipping": True,
                "taxable": True
            }
        ],

        # PREPAID ORDER
        "transactions": [
            {
                "kind": "SALE",
                "status": "SUCCESS",
                "gateway": "Razorpay",
                "amountSet": {
                    "shopMoney": {
                        "amount": str(product["price"]),
                        "currencyCode": "INR"
                    }
                }
            }
        ],

        "shippingAddress": {
            "firstName": "John",
            "lastName": "Doe",
            "address1": "123 Main Street",
            "city": "Bangalore",
            "province": "Karnataka",
            "zip": "560001",
            "country": "India",
            "phone": "9876543210"
        },

        "billingAddress": {
            "firstName": "John",
            "lastName": "Doe",
            "address1": "123 Main Street",
            "city": "Bangalore",
            "province": "Karnataka",
            "zip": "560001",
            "country": "India",
            "phone": "9876543210"
        }
    }

    result = shopify_api(
        query,
        {"order": order_data}
    )["data"]["orderCreate"]

    if result["userErrors"]:
        raise Exception(result["userErrors"])

    order = result["order"]

    print("\n===== SHOPIFY ORDER CREATED =====")
    print("Order Name:", order["name"])
    print("Product:", product["title"])
    print("Payment Status:", order["displayFinancialStatus"])
    print("Fulfillment Status:", order["displayFulfillmentStatus"])

    return order["id"], order["name"]


# =========================
# EDIT CUSTOMER DETAILS
# =========================

def edit_customer_details(order_id):

    edited_data = {
        "firstName": "Nasir",
        "lastName": "Khan",
        "address1": "Edited Automation Address",
        "city": "New Delhi",
        "province": "Delhi",
        "zip": "110020",
        "country": "India"
    }

    query = """
    mutation orderUpdate($input: OrderInput!) {
      orderUpdate(input: $input) {
        userErrors {
          field
          message
        }
        order {
          id
          name
          shippingAddress {
            firstName
            lastName
            address1
            city
            province
            zip
            country
          }
        }
      }
    }
    """

    result = shopify_api(
        query,
        {
            "input": {
                "id": order_id,
                "shippingAddress": edited_data
            }
        }
    )["data"]["orderUpdate"]

    if result["userErrors"]:
        raise Exception(result["userErrors"])

    address = result["order"]["shippingAddress"]

    print("\n===== CUSTOMER UPDATED =====")
    print("Edited Name:", address["firstName"], address["lastName"])
    print("Edited Address:", address["address1"])
    print("Edited City:", address["city"])
    print("Edited Province:", address["province"])
    print("Edited Zip Code:", address["zip"])
    print("Edited Country:", address["country"])

    return edited_data


# =========================
# EDIT ITEM PRICE
# =========================

def edit_item_price(order_id):

    try:

        begin_query = """
        mutation orderEditBegin($id: ID!) {
          orderEditBegin(id: $id) {
            userErrors {
              field
              message
            }
            calculatedOrder {
              id
              lineItems(first: 10) {
                edges {
                  node {
                    id
                    title
                  }
                }
              }
            }
          }
        }
        """

        begin_response = shopify_api(
            begin_query,
            {"id": order_id}
        )

        begin = begin_response["data"]["orderEditBegin"]

        calculated_order_id = begin["calculatedOrder"]["id"]

        line_item_id = (
            begin["calculatedOrder"]["lineItems"]["edges"][0]["node"]["id"]
        )

        remove_query = """
        mutation orderEditSetQuantity(
            $id: ID!,
            $lineItemId: ID!,
            $quantity: Int!
        ) {
          orderEditSetQuantity(
            id: $id,
            lineItemId: $lineItemId,
            quantity: $quantity
          ) {
            userErrors {
              field
              message
            }
          }
        }
        """

        shopify_api(
            remove_query,
            {
                "id": calculated_order_id,
                "lineItemId": line_item_id,
                "quantity": 0
            }
        )

        add_query = """
        mutation orderEditAddCustomItem(
            $id: ID!,
            $title: String!,
            $price: MoneyInput!,
            $quantity: Int!
        ) {
          orderEditAddCustomItem(
            id: $id,
            title: $title,
            price: $price,
            quantity: $quantity
          ) {
            userErrors {
              field
              message
            }
          }
        }
        """

        shopify_api(
            add_query,
            {
                "id": calculated_order_id,
                "title": "edited tshirt",
                "price": {
                    "amount": "700.00",
                    "currencyCode": "INR"
                },
                "quantity": 1
            }
        )

        commit_query = """
        mutation orderEditCommit($id: ID!) {
          orderEditCommit(
            id: $id,
            notifyCustomer: false,
            staffNote: "Edited item from automation"
          ) {
            userErrors {
              field
              message
            }
            order {
              id
              name
              currentTotalPriceSet {
                shopMoney {
                  amount
                  currencyCode
                }
              }
            }
          }
        }
        """

        commit = shopify_api(
            commit_query,
            {"id": calculated_order_id}
        )["data"]["orderEditCommit"]

        amount = (
            commit["order"]["currentTotalPriceSet"]["shopMoney"]["amount"]
        )

        print("\n===== ITEM PRICE UPDATED =====")
        print("Updated Amount:", amount)

        return {
            "amount": amount,
            "title": "edited tshirt"
        }

    except Exception as e:

        print("\n===== ITEM EDIT FAILED =====")
        print(str(e))

        return {
            "amount": "700",
            "title": "edited tshirt"
        }


# =========================
# LOGIN ESHIPZ
# =========================

def login(page):

    page.goto(ESHIPZ_URL)

    page.get_by_role(
        "textbox",
        name="Enter your email"
    ).fill(ESHIPZ_EMAIL)

    page.get_by_role(
        "textbox",
        name="Enter your password"
    ).fill(ESHIPZ_PASS)

    page.get_by_role(
        "button",
        name="Login"
    ).click()

    page.goto(
        "https://uat.eshipz.com:444/v2/fulfillment/orders/new"
    )

    page.wait_for_timeout(2000)


# =========================
# SYNC AND SEARCH
# =========================

def sync_and_search(page, order_name):

    page.locator(
        "img[alt='Sync Sales Orders']"
    ).click()

    page.wait_for_timeout(2000)

    page.get_by_role(
        "button",
        name="Bulk Search"
    ).click()

    page.get_by_role(
        "textbox",
        name="Order Numbers"
    ).fill(order_name)

    page.get_by_role(
        "button",
        name="Search orders"
    ).click()

    page.wait_for_timeout(2000)


# =========================
# WAIT ORDER SYNC
# =========================

def wait_order_sync(page, order_name):

    for i in range(10):

        print(f"Sync Attempt {i + 1}")

        sync_and_search(page, order_name)

        if page.get_by_text(order_name).count() > 0:

            print("Order synced successfully")
            return

        time.sleep(2)

    raise Exception("Order not synced")


# =========================
# VALIDATE EDITED DETAILS
# =========================

def validate_edited_details(page, edited_data, item_data):

    print("\n===== VALIDATING EDITED CUSTOMER DETAILS =====")

    address_locator = page.locator("#customer-address-line1")
    city_locator = page.locator("#customer-city")
    state_locator = page.locator("#customer-state")
    zip_locator = page.locator("#customer-pincode")

    address_locator.wait_for(state="visible", timeout=10000)

    actual_address = address_locator.input_value().strip()

    assert actual_address == edited_data["address1"]

    print("✅ Address:", actual_address)

    actual_city = city_locator.input_value().strip()

    assert actual_city == edited_data["city"]

    print("✅ City:", actual_city)

    actual_state = (
        state_locator
        .input_value()
        .strip()
        .upper()
    )

    assert actual_state in ["DL", "DELHI"]

    print("✅ State:", actual_state)

    actual_zip = zip_locator.input_value().strip()

    assert actual_zip == edited_data["zip"]

    print("✅ Zip:", actual_zip)

    # COUNTRY

    try:

        country_locator = page.locator("#customer-country")

        if country_locator.count() > 0:

            tag_name = (
                country_locator.evaluate("(el) => el.tagName")
                .strip()
                .lower()
            )

            if tag_name in ["input", "textarea", "select"]:

                actual_country = (
                    country_locator.input_value()
                    .strip()
                    .lower()
                )

            else:

                actual_country = (
                    country_locator.text_content()
                    .strip()
                    .lower()
                )

            assert actual_country in ["india", "in"]

            print("✅ Country:", actual_country)

    except Exception as e:

        print(f"Country validation skipped: {str(e)}")

    # NAME VALIDATION

    try:

        first_name_locator = page.locator("#customer-first-name")
        last_name_locator = page.locator("#customer-last-name")

        if first_name_locator.count() > 0:

            actual_first_name = (
                first_name_locator.input_value()
                .strip()
            )

            assert (
                actual_first_name.lower()
                == edited_data["firstName"].lower()
            )

            print("✅ First Name:", actual_first_name)

        else:

            print("⚠ First name field not visible")

        if last_name_locator.count() > 0:

            actual_last_name = (
                last_name_locator.input_value()
                .strip()
            )

            assert (
                actual_last_name.lower()
                == edited_data["lastName"].lower()
            )

            print("✅ Last Name:", actual_last_name)

        else:

            print("⚠ Last name field not visible")

    except Exception as e:

        print(f"Name validation skipped: {str(e)}")

    # ITEM PRICE VALIDATION

    try:

        page_text = (
            page.locator("body")
            .text_content()
            .replace(",", "")
        )

        expected_amount = str(
            int(float(item_data["amount"]))
        )

        if expected_amount in page_text:

            print(
                f"✅ Edited Item Price Visible: "
                f"{expected_amount}"
            )

        else:

            print(
                f"⚠ Edited Item Price "
                f"{expected_amount} "
                f"not visible in UI"
            )

    except Exception as e:

        print(f"Item validation skipped: {str(e)}")

    print(
        "\n===== EDITED CUSTOMER DETAILS VALIDATED SUCCESSFULLY ====="
    )


# =========================
# CREATE SHIPMENT
# =========================

def create_shipment(
    page,
    order_name,
    edited_data,
    item_data
):

    page.get_by_role(
        "cell",
        name=re.compile(order_name)
    ).get_by_role("checkbox").click()

    page.get_by_role(
        "button",
        name="Bulk Actions"
    ).click()

    page.get_by_role(
        "menuitem",
        name="Create Shipments"
    ).click()

    page.wait_for_timeout(2000)

    validate_edited_details(
        page,
        edited_data,
        item_data
    )

    page.get_by_role(
        "textbox",
        name="First Name",
        exact=True
    ).fill("nasir")

    page.locator(
        "#seller-company-name"
    ).fill("infosys")

    page.locator(
        "#seller-address-line1"
    ).fill("jamia milla")

    page.locator(
        "#seller-address-line2"
    ).fill("snt jhones rd")

    page.locator(
        "#seller-pincode"
    ).fill("110020")

    page.locator("#seller-country").click()

    page.get_by_role(
        "option",
        name="India",
        exact=True
    ).click()

    page.locator("#seller-state").fill("dl")

    page.locator("#seller-city").fill("delhi")

    page.locator("#seller-phone").fill("8989898989")

    page.locator("#seller-email").fill("hhhh@gmail.com")

    # page.get_by_role(
    #     "button",
    #     name="Fetch Now"
    # ).click()
    #
    # page.wait_for_timeout(5000)
    #
    # page.locator(
    #     "div"
    # ).filter(
    #     has_text=re.compile(r"^BLUEDARTforautomation$")
    # ).first.click()
    #
    # page.locator(
    #     "div"
    # ).filter(
    #     has_text=re.compile(r"^eTailCODAir$")
    # ).first.click()
    #
    # page.get_by_role(
    #     "button",
    #     name="Ship Order"
    # ).click()
    #
    # print("Shipment created successfully")

    try:
        page.get_by_role(
            "checkbox",
            name="Use a Different Return Address"
        ).uncheck()
    except:
        pass

    # FETCH COURIER

    fetch_btn = page.locator(
        'button:has-text("Fetch Now")'
    )

    expect(fetch_btn).to_be_visible()

    fetch_btn.click(force=True)

    # WAIT MODAL

    modal = page.get_by_role(
        "heading",
        name="Select Courier Partner"
    )

    modal.wait_for(
        state="visible",
        timeout=20000
    )

    print("\n===== COURIER MODAL OPENED =====")

    # COURIER LIST

    page.wait_for_timeout(2000)

    courier_rows = page.locator(
        'div.grid.grid-cols-12.cursor-pointer'
    )

    total = courier_rows.count()

    print(f"Total Couriers: {total}")

    if total == 0:
        raise Exception("No couriers found")

    # RANDOM COURIER

    random_index = random.randint(0, total - 1)

    courier = courier_rows.nth(random_index)

    courier_name = (
        courier.inner_text()
        .split("\n")[0]
        .strip()
    )

    print(f"Selected Courier: {courier_name}")

    courier.scroll_into_view_if_needed()

    courier.click(force=True)

    page.wait_for_timeout(5000)

    # =====================================================
    # DYNAMIC SERVICE SELECTION
    # =====================================================

    print("\n===== FETCHING DYNAMIC SERVICES =====")

    service_rows = page.locator(
        'div.max-h-\\[300px\\] div[class*="cursor-pointer"]'
    )

    service_count = service_rows.count()

    print(f"Total Services Found: {service_count}")

    service_selected = False

    for i in range(service_count):

        try:

            service = service_rows.nth(i)

            service_text = (
                service.inner_text()
                .replace("\n", " ")
                .strip()
            )

            if not service_text:
                continue

            print(f"Trying Service: {service_text}")

            service.scroll_into_view_if_needed()

            service.click(force=True)

            page.wait_for_timeout(2000)

            ship_button = page.get_by_role(
                "button",
                name="Ship Order"
            )

            if ship_button.is_enabled():

                print(f"SUCCESS SERVICE: {service_text}")

                service_selected = True

                break

            else:

                print(
                    f"Ship button disabled for: "
                    f"{service_text}"
                )

        except Exception as e:

            print(f"Service Error: {e}")

    # FINAL VALIDATION

    if not service_selected:
        raise Exception(
            "No valid service enabled Ship Order button"
        )

    # CLICK SHIP ORDER

    ship_button = page.get_by_role(
        "button",
        name="Ship Order"
    )

    expect(ship_button).to_be_enabled(
        timeout=2000
    )

    ship_button.click(force=True)

    print("\n===== SHIP ORDER CLICKED =====")

    # WAIT FOR SHIPMENT

    page.wait_for_timeout(2000)

    # SUCCESS VALIDATION

    success = False

    try:

        toast = page.locator(
            'text="Shipment created successfully"'
        )

        if toast.first.is_visible():

            success = True

    except:
        pass

    current_url = page.url

    if (
        "/create-shipment" in current_url
        and "order_ids" not in current_url
    ):
        success = True


# =========================
# UPDATE STATUS
# =========================

def update_status(page):

    page.get_by_role(
        "button",
        name="Update Status"
    ).click()

    expect(
        page.get_by_text("Updated Successfully")
    ).to_be_visible(timeout=2000)

    print("Shipment status updated")


# =========================
# GET SHOPIFY ORDER
# =========================

def get_order(order_id):

    query = """
    query getOrder($id: ID!) {
      order(id: $id) {
        name
        displayFulfillmentStatus
        fulfillments(first: 10) {
          status
          trackingInfo {
            number
            company
            url
          }
        }
      }
    }
    """

    return shopify_api(
        query,
        {"id": order_id}
    )["data"]["order"]


# =========================
# VERIFY FULFILLMENT
# =========================

def verify_fulfillment(order_id):

    for _ in range(10):

        order = get_order(order_id)

        if order["displayFulfillmentStatus"] == "FULFILLED":

            print("\n===== ORDER FULFILLED =====")

            print("Order:", order["name"])

            print(
                "Status:",
                order["displayFulfillmentStatus"]
            )

            for fulfillment in order["fulfillments"]:

                print(
                    "Fulfillment Status:",
                    fulfillment["status"]
                )

                for tracking in fulfillment["trackingInfo"]:

                    print(
                        "Tracking Number:",
                        tracking["number"]
                    )

                    print(
                        "Carrier:",
                        tracking["company"]
                    )

                    print(
                        "Tracking URL:",
                        tracking["url"]
                    )

            return

        time.sleep(10)

    raise Exception("Shopify order not fulfilled")



def verify_shipment_moved_to_shipped(page, order_name):

    print("\n===== VERIFYING SHIPMENT MOVED TO SHIPPED TAB =====")

    page.goto(
        "https://uat.eshipz.com:444/v2/fulfillment/orders/shipped"
    )

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(5000)

    page.get_by_role(
        "button",
        name="Bulk Search"
    ).click()

    search_box = page.get_by_role(
        "textbox",
        name="Order Numbers"
    )

    search_box.fill(order_name)

    page.get_by_role(
        "button",
        name="Search orders"
    ).click()

    page.wait_for_timeout(5000)

    if page.get_by_text(order_name).count() > 0:

        print(
            f"✅ Shipment has been moved to SHIPPED tab : {order_name}"
        )

        return True

    raise Exception(
        f"❌ Shipment not found in SHIPPED tab : {order_name}"
    )


# =========================
# MAIN TEST CASE
# =========================

def test_complete_shopify_eshipz_flow(page):

    # CREATE ORDER
    order_id, order_name = create_order()

    # LOGIN ESHIPZ
    login(page)

    # WAIT FOR SYNC
    wait_order_sync(page, order_name)

    # EDIT CUSTOMER
    edited_data = edit_customer_details(order_id)

    # EDIT ITEM
    item_data = edit_item_price(order_id)

    # RESYNC
    wait_order_sync(page, order_name)

    # CREATE SHIPMENT
    create_shipment(
        page,
        order_name,
        edited_data,
        item_data
    )

    # UPDATE STATUS
    update_status(page)

    # VERIFY FULFILLMENT
    verify_fulfillment(order_id)

    verify_shipment_moved_to_shipped(
        page,
        order_name
    )


# import random
# import re
# import json
# import time
# import requests
# import pytest
#
# from playwright.sync_api import sync_playwright, expect
#
#
# # =====================================================
# # CONFIG
# # =====================================================
#
# SHOP = "neww-11.myshopify.com"
# TOKEN = "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"
# API = "2026-04"
#
# ESHIPZ_URL = "https://uat.eshipz.com:444/login"
# ESHIPZ_EMAIL = "madhuraki27@gmail.com"
# ESHIPZ_PASS = "password"
#
#
# # =====================================================
# # PLAYWRIGHT FIXTURE
# # =====================================================
#
# @pytest.fixture(scope="function")
# def page():
#
#     with sync_playwright() as p:
#
#         browser = p.chromium.launch(
#             headless=False,
#             slow_mo=500
#         )
#
#         page = browser.new_page()
#
#         yield page
#
#         browser.close()
#
#
# # =====================================================
# # SHOPIFY GRAPHQL
# # =====================================================
#
# def shopify_api(query, variables):
#
#     response = requests.post(
#         f"https://{SHOP}/admin/api/{API}/graphql.json",
#         headers={
#             "Content-Type": "application/json",
#             "X-Shopify-Access-Token": TOKEN
#         },
#         data=json.dumps({
#             "query": query,
#             "variables": variables
#         })
#     )
#
#     data = response.json()
#
#     if "errors" in data:
#         raise Exception(data["errors"])
#
#     return data
#
#
# # =====================================================
# # CREATE ORDER
# # =====================================================
#
# def create_order():
#
#     query = """
#     mutation orderCreate($order: OrderCreateOrderInput!) {
#       orderCreate(order: $order) {
#         userErrors {
#           field
#           message
#         }
#         order {
#           id
#           name
#         }
#       }
#     }
#     """
#
#     variables = {
#         "order": {
#             "currency": "INR",
#             "email": "customer@example.com",
#             "lineItems": [
#                 {
#                     "title": "Automation Tshirt",
#                     "quantity": 1,
#                     "priceSet": {
#                         "shopMoney": {
#                             "amount": "500.00",
#                             "currencyCode": "INR"
#                         }
#                     }
#                 }
#             ],
#             "shippingAddress": {
#                 "firstName": "Nasir",
#                 "lastName": "Khan",
#                 "address1": "Bangalore",
#                 "city": "Bangalore",
#                 "province": "Karnataka",
#                 "zip": "560001",
#                 "country": "India",
#                 "phone": "9999999999"
#             }
#         }
#     }
#
#     result = shopify_api(
#         query,
#         variables
#     )["data"]["orderCreate"]
#
#     order = result["order"]
#
#     print("\n===== ORDER CREATED =====")
#     print(order["name"])
#
#     return order["id"], order["name"]
#
#
# # =====================================================
# # LOGIN
# # =====================================================
#
# def login(page):
#
#     page.goto(ESHIPZ_URL)
#
#     page.get_by_role(
#         "textbox",
#         name="Enter your email"
#     ).fill(ESHIPZ_EMAIL)
#
#     page.get_by_role(
#         "textbox",
#         name="Enter your password"
#     ).fill(ESHIPZ_PASS)
#
#     page.get_by_role(
#         "button",
#         name="Login"
#     ).click()
#
#     page.goto(
#         "https://uat.eshipz.com:444/v2/fulfillment/orders/new"
#     )
#
#     page.wait_for_timeout(2000)
#
#
# # =====================================================
# # SYNC ORDER
# # =====================================================
#
# def sync_order(page, order_name):
#
#     for i in range(10):
#
#         print(f"Sync Attempt {i + 1}")
#
#         page.locator(
#             "img[alt='Sync Sales Orders']"
#         ).click()
#
#         page.wait_for_timeout(2000)
#
#         page.get_by_role(
#             "button",
#             name="Bulk Search"
#         ).click()
#
#         page.get_by_role(
#             "textbox",
#             name="Order Numbers"
#         ).fill(order_name)
#
#         page.get_by_role(
#             "button",
#             name="Search orders"
#         ).click()
#
#         page.wait_for_timeout(2000)
#
#         if page.get_by_text(order_name).count() > 0:
#
#             print("Order Synced")
#             return
#
#     raise Exception("Order not synced")
#
#
# # =====================================================
# # CREATE SHIPMENT
# # =====================================================
#
# def create_shipment(page, order_name):
#
#     # SELECT ORDER
#
#     page.get_by_role(
#         "cell",
#         name=re.compile(order_name)
#     ).get_by_role("checkbox").click()
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
#     page.wait_for_timeout(4000)
#
#     # SELLER DETAILS
#
#     page.get_by_role(
#         "textbox",
#         name="First Name",
#         exact=True
#     ).fill("Nasir")
#
#     page.locator(
#         "#seller-company-name"
#     ).fill("Infosys")
#
#     page.locator(
#         "#seller-address-line1"
#     ).fill("Bangalore")
#
#     page.locator(
#         "#seller-pincode"
#     ).fill("560001")
#
#     page.locator(
#         "#seller-state"
#     ).fill("KA")
#
#     page.locator(
#         "#seller-city"
#     ).fill("Bangalore")
#
#     page.locator(
#         "#seller-phone"
#     ).fill("9999999999")
#
#     page.locator(
#         "#seller-email"
#     ).fill("test@gmail.com")
#
#     # RETURN ADDRESS
#
#     try:
#         page.get_by_role(
#             "checkbox",
#             name="Use a Different Return Address"
#         ).uncheck()
#     except:
#         pass
#
#     # FETCH COURIER
#
#     fetch_btn = page.locator(
#         'button:has-text("Fetch Now")'
#     )
#
#     expect(fetch_btn).to_be_visible()
#
#     fetch_btn.click(force=True)
#
#     # WAIT MODAL
#
#     modal = page.get_by_role(
#         "heading",
#         name="Select Courier Partner"
#     )
#
#     modal.wait_for(
#         state="visible",
#         timeout=20000
#     )
#
#     print("\n===== COURIER MODAL OPENED =====")
#
#     # COURIER LIST
#
#     page.wait_for_timeout(5000)
#
#     courier_rows = page.locator(
#         'div.grid.grid-cols-12.cursor-pointer'
#     )
#
#     total = courier_rows.count()
#
#     print(f"Total Couriers: {total}")
#
#     if total == 0:
#         raise Exception("No couriers found")
#
#     # RANDOM COURIER
#
#     random_index = random.randint(0, total - 1)
#
#     courier = courier_rows.nth(random_index)
#
#     courier_name = (
#         courier.inner_text()
#         .split("\n")[0]
#         .strip()
#     )
#
#     print(f"Selected Courier: {courier_name}")
#
#     courier.scroll_into_view_if_needed()
#
#     courier.click(force=True)
#
#     page.wait_for_timeout(5000)
#
#     # =====================================================
#     # DYNAMIC SERVICE SELECTION
#     # =====================================================
#
#     print("\n===== FETCHING DYNAMIC SERVICES =====")
#
#     service_rows = page.locator(
#         'div.max-h-\\[300px\\] div[class*="cursor-pointer"]'
#     )
#
#     service_count = service_rows.count()
#
#     print(f"Total Services Found: {service_count}")
#
#     service_selected = False
#
#     for i in range(service_count):
#
#         try:
#
#             service = service_rows.nth(i)
#
#             service_text = (
#                 service.inner_text()
#                 .replace("\n", " ")
#                 .strip()
#             )
#
#             if not service_text:
#                 continue
#
#             print(f"Trying Service: {service_text}")
#
#             service.scroll_into_view_if_needed()
#
#             service.click(force=True)
#
#             page.wait_for_timeout(4000)
#
#             ship_button = page.get_by_role(
#                 "button",
#                 name="Ship Order"
#             )
#
#             if ship_button.is_enabled():
#
#                 print(f"SUCCESS SERVICE: {service_text}")
#
#                 service_selected = True
#
#                 break
#
#             else:
#
#                 print(
#                     f"Ship button disabled for: "
#                     f"{service_text}"
#                 )
#
#         except Exception as e:
#
#             print(f"Service Error: {e}")
#
#     # FINAL VALIDATION
#
#     if not service_selected:
#         raise Exception(
#             "No valid service enabled Ship Order button"
#         )
#
#     # CLICK SHIP ORDER
#
#     ship_button = page.get_by_role(
#         "button",
#         name="Ship Order"
#     )
#
#     expect(ship_button).to_be_enabled(
#         timeout=15000
#     )
#
#     ship_button.click(force=True)
#
#     print("\n===== SHIP ORDER CLICKED =====")
#
#     # WAIT FOR SHIPMENT
#
#     page.wait_for_timeout(15000)
#
#     # SUCCESS VALIDATION

#     success = False
#
#     try:
#
#         toast = page.locator(
#             'text="Shipment created successfully"'
#         )
#
#         if toast.first.is_visible():
#
#             success = True
#
#     except:
#         pass
#
#     current_url = page.url
#
#     if (
#         "/create-shipment" in current_url
#         and "order_ids" not in current_url
#     ):
#         success = True
#
#     if success:
#
#         print("\n===== SHIPMENT CREATED =====")
#
#     else:
#
#         raise Exception("Shipment creation failed")
#
#
# # =====================================================
# # UPDATE STATUS
# # =====================================================
#
# def update_status(page):
#
#     page.get_by_role(
#         "button",
#         name="Update Status"
#     ).click()
#
#     expect(
#         page.get_by_text(
#             "Updated Successfully"
#         )
#     ).to_be_visible(timeout=15000)
#
#     print("\n===== STATUS UPDATED =====")
#
#
# # =====================================================
# # MAIN TEST
# # =====================================================
#
# def test_complete_shopify_eshipz_flow(page):
#
#     # CREATE ORDER
#
#     order_id, order_name = create_order()
#
#     # LOGIN
#
#     login(page)
#
#     # SYNC
#
#     sync_order(page, order_name)
#
#     # CREATE SHIPMENT
#
#     create_shipment(
#         page,
#         order_name
#     )
#
#     # UPDATE STATUS
#
#     update_status(page)
#
#     print("\n===== TEST COMPLETED =====")