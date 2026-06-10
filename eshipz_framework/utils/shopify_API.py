import json
import requests
import time

SHOP = "neww-11.myshopify.com"
TOKEN = "YOUR_NEW_ACCESS_TOKEN"
API = "2026-04"


def shopify_api(query, variables):

    res = requests.post(
        f"https://{SHOP}/admin/api/{API}/graphql.json",
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": "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"
        },
        data=json.dumps({
            "query": query,
            "variables": variables
        })
    )

    return res.json()


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

    return shopify_api(query, {"id": order_id})["data"]["order"]


def verify_fulfillment(order_id):
    for _ in range(10):
        order = get_order(order_id)

        if order["displayFulfillmentStatus"] == "FULFILLED":
            print("\n===== SHOPIFY ORDER DETAILS =====")
            print("Order Name:", order["name"])
            print("Fulfillment Status:", order["displayFulfillmentStatus"])
            print("Shopify order fulfilled successfully")

            for f in order["fulfillments"]:
                print("Fulfillment Status:", f["status"])
                for t in f["trackingInfo"]:
                    print("Tracking Number:", t["number"])
                    print("Carrier/Company:", t["company"])
                    print("Tracking URL:", t["url"])
            return

        time.sleep(10)

    raise Exception("Shopify order not fulfilled")