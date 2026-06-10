
import pytest
import time

from utils.functions import load_orders, create_order, open_order_menu, get_popup_message, \
    download_pick_list
# from utils.functions import (
#     create_order,
#     get_popup_message,
#     load_orders,
#     open_order_menu,
#     download_pick_list
# )

from eshipz_framework.utils.login import login


@pytest.fixture(scope="session")
def orders_data():
    return load_orders("data/orders.json")


def test_order_sanity(page, orders_data):

    login(page)

    page.locator("img[alt='box']").first.click()

    page.wait_for_selector("span:has-text('Order')")
    page.locator("span:has-text('Order')").click()

    ref = "ORD" + str(int(time.time()))
    orders_data["reference_no"] = ref

    print("\n=== SANITY START ===")

    # ---------------- CREATE ----------------
    msg = create_order(page, orders_data)
    print("Create =>", msg)

    page.wait_for_selector("button:has(svg.lucide-ellipsis-vertical)")

    # ---------------- EDIT ----------------
    open_order_menu(page)
    page.get_by_role("button", name="Edit").click()

    page.wait_for_selector("#customer-company-name")

    edited_company = "Sanity Company Edited"
    page.locator("#customer-company-name").fill(edited_company)

    # VALIDATE FIELD VALUE (no navigation changes)
    current_value = page.locator("#customer-company-name").input_value()
    if current_value == edited_company:
        print("✅ Edit Field Updated:", current_value)
    else:
        print("❌ Edit Field Failed:", current_value)

    page.locator("//button[.//span[text()='Update Order']]").click()

    edit_msg = get_popup_message(page)
    print("Edit =>", edit_msg)

    page.wait_for_selector("button:has(svg.lucide-ellipsis-vertical)")

    # ---------------- SPLIT ----------------
    open_order_menu(page)
    page.get_by_role("button", name="Split Order").click()

    page.locator("#order-action-confirmation-apply").click()

    page.wait_for_timeout(3000)

    # ---------------- BULK SEARCH ----------------
    # ---------------- BULK SEARCH ----------------
    page.locator("//span[text()='Bulk Search']").click(force=True)

    bulk_input = page.locator("textarea").first
    bulk_input.fill(ref)

    page.locator("button:has(span:text-is('Search orders'))").click()

    # wait for search results
    page.wait_for_selector("table tbody tr", timeout=90000)

    # open first order from results
    page.locator("table tbody tr").first.click()

    # validate split message
    page.wait_for_selector("text=This order is Split", timeout=60000)
    split_text = page.locator("text=This order is Split").text_content()

    print("Split =>", split_text)

    # close order drawer
    page.locator("//img[@alt='close']").click()

    # clear filters
    page.locator("//span[normalize-space()='Clear All']").click()


    # ---------------- PICK LIST ----------------
    page.wait_for_selector("button:has(svg.lucide-ellipsis-vertical)")
    open_order_menu(page)

    with page.context.expect_page() as new_page_info:
        page.get_by_role("button", name="Pick List").click()

    pick_page = new_page_info.value
    pick_page.wait_for_load_state()

    with pick_page.expect_download() as download_info:
        pick_page.get_by_role("button", name="DOWNLOAD").click()

    download_pick_list(download_info.value, orders_data)

    pick_page.close()
    page.bring_to_front()

    # ---------------- CLONE ----------------
    open_order_menu(page)
    page.get_by_role("button", name="Clone").click()

    page.locator("#order-action-confirmation-apply").click()

    clone_msg = get_popup_message(page)
    print("Clone =>", clone_msg)

    # ---------------- CANCEL ----------------
    open_order_menu(page)
    page.get_by_role("button", name="Cancel").nth(1).click()

    page.locator("#order-action-confirmation-apply").click()

    cancel_msg = get_popup_message(page)
    print("Cancel =>", cancel_msg)

    # ---------------- TABS ----------------
    page.get_by_role("button", name="Unprocessed").click()
    print("user moved to unprocessed tab")

    page.get_by_role("button", name="Cancelled").click()
    print("user moved to cancelled tab")

    page.get_by_role("button", name="Shipped").click()
    print("user moved to shipped tab")

    page.get_by_role("button", name="All Orders").click()
    print("user moved to all orders tab")

    print("\n=== SANITY END ===")


