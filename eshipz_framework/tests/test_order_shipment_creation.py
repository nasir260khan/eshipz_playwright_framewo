import pytest
import time

from  utils.functions import load_orders, create_order, create_shipment, download_and_validate_label

from  utils.login import login


# from utils.functions import create_order, create_shipment, download_and_validate_label, load_orders





@pytest.fixture(scope="session")
def orders_data():
    return load_orders("data/orders.json")


def test_order_shipment(page, orders_data):

    login(page)

    # open sidebar
    page.locator("img[alt='box']").first.click()

    # go to orders
    page.wait_for_selector("span:has-text('Order')")
    page.locator("span:has-text('Order')").click()

    ref = "ORD" + str(int(time.time()))
    orders_data["reference_no"] = ref

    # create order
    create_order(page, orders_data)

    # wait for order checkbox
    page.wait_for_selector("button[role='checkbox']")

    # create shipment
    create_shipment(page)

    # validate label
    download_and_validate_label(page, orders_data)