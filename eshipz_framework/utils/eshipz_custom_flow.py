import re
from playwright.sync_api import expect
from utils.login import login


def eshipz_custom_flow(page, order_name):

    login(page)

    page.goto(
        "https://uat.eshipz.com:444/v2/fulfillment/orders/new"
    )

    for i in range(10):

        print(f"Searching order sync attempt {i + 1}")

        page.locator(
            "img[alt='Sync Sales Orders']"
        ).click()

        page.wait_for_timeout(4000)

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

        page.wait_for_timeout(4000)

        if page.get_by_text(order_name).count() > 0:
            print("Order synced successfully")
            break

    else:
        raise Exception("Order not synced")

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

    page.get_by_role(
        "textbox",
        name="First Name",
        exact=True
    ).fill("nasir")

    page.locator("#seller-company-name").fill("infosys")
    page.locator("#seller-address-line1").fill("jamia milla")
    page.locator("#seller-address-line2").fill("snt jhones rd")

    page.get_by_role(
        "combobox",
        name="Country India"
    ).click()

    page.get_by_role(
        "option",
        name="India",
        exact=True
    ).click()

    page.locator("#seller-pincode").fill("110020")
    page.locator("#seller-state").fill("dl")
    page.locator("#customer-pincode").fill("110020")
    page.locator("#customer-state").fill("dl")

    page.get_by_role(
        "button",
        name="Custom Ship"
    ).click()

    page.wait_for_timeout(5000)

    import random

    print("\n===== PREPAID MAPPING =====")

    # =====================================
    # PREPAID CARRIER
    # =====================================

    page.locator("#prepaid-carrier").click()
    page.wait_for_timeout(1500)

    options = page.locator('[role="option"]:visible')

    count = options.count()

    if count == 0:
        raise Exception("No Prepaid Carriers Found")

    idx = random.randint(0, count - 1)

    prepaid_carrier = (
        options.nth(idx)
        .inner_text()
        .strip()
    )

    options.nth(idx).click()

    print(f"Prepaid Carrier : {prepaid_carrier}")

    page.wait_for_timeout(2000)

    # =====================================
    # PREPAID VENDOR
    # =====================================

    page.locator("#prepaid-vendor").click()
    page.wait_for_timeout(1500)

    options = page.locator('[role="option"]:visible')

    count = options.count()

    if count == 0:
        raise Exception("No Prepaid Vendors Found")

    idx = random.randint(0, count - 1)

    prepaid_vendor = (
        options.nth(idx)
        .inner_text()
        .strip()
    )

    options.nth(idx).click()

    print(f"Prepaid Vendor : {prepaid_vendor}")

    page.wait_for_timeout(2000)

    # =====================================
    # PREPAID SERVICE
    # =====================================

    page.locator("#prepaid-service").click()
    page.wait_for_timeout(1500)

    options = page.locator('[role="option"]:visible')

    count = options.count()

    if count == 0:
        raise Exception("No Prepaid Services Found")

    idx = random.randint(0, count - 1)

    prepaid_service = (
        options.nth(idx)
        .inner_text()
        .strip()
    )

    options.nth(idx).click()

    print(f"Prepaid Service : {prepaid_service}")

    page.wait_for_timeout(3000)

    print("\n===== COD MAPPING =====")

    # =====================================
    # COD CARRIER
    # =====================================

    carrier_dropdown = page.get_by_role(
        "combobox"
    ).nth(0)

    carrier_dropdown.click()

    page.wait_for_timeout(1500)

    options = page.locator('[role="option"]:visible')

    count = options.count()

    if count == 0:
        raise Exception("No COD Carriers Found")

    idx = random.randint(0, count - 1)

    cod_carrier = (
        options.nth(idx)
        .inner_text()
        .strip()
    )

    options.nth(idx).click()

    print(f"COD Carrier : {cod_carrier}")

    page.wait_for_timeout(2000)

    # =====================================
    # COD VENDOR
    # =====================================

    vendor_dropdown = page.get_by_role(
        "combobox"
    ).nth(1)

    vendor_dropdown.click()

    page.wait_for_timeout(1500)

    options = page.locator('[role="option"]:visible')

    count = options.count()

    if count == 0:
        raise Exception("No COD Vendors Found")

    idx = random.randint(0, count - 1)

    cod_vendor = (
        options.nth(idx)
        .inner_text()
        .strip()
    )

    options.nth(idx).click()

    print(f"COD Vendor : {cod_vendor}")

    page.wait_for_timeout(2000)

    # =====================================
    # COD SERVICE
    # =====================================

    service_dropdown = page.get_by_role(
        "combobox"
    ).nth(2)

    service_dropdown.click()

    page.wait_for_timeout(1500)

    options = page.locator('[role="option"]:visible')

    count = options.count()

    if count == 0:
        raise Exception("No COD Services Found")

    idx = random.randint(0, count - 1)

    cod_service = (
        options.nth(idx)
        .inner_text()
        .strip()
    )

    options.nth(idx).click()

    print(f"COD Service : {cod_service}")

    page.wait_for_timeout(2000)

    print("\n===== FINAL MAPPING =====")
    print(f"Prepaid Carrier : {prepaid_carrier}")
    print(f"Prepaid Vendor  : {prepaid_vendor}")
    print(f"Prepaid Service : {prepaid_service}")

    print(f"COD Carrier     : {cod_carrier}")
    print(f"COD Vendor      : {cod_vendor}")
    print(f"COD Service     : {cod_service}")

    page.get_by_role(
        "button",
        name="Ship Order"
    ).click()

    print("Shipment created successfully")

    page.wait_for_timeout(9000)

    page.goto(
        "https://uat.eshipz.com:444/v2/fulfillment/shipment/all"
    )

    page.get_by_role(
        "button",
        name="Bulk Search"
    ).click()

    page.get_by_role(
        "textbox",
        name="Search"
    ).fill(order_name)

    page.get_by_role(
        "button",
        name="Search shipments"
    ).click()

    page.get_by_role(
        "row",
        name="Order ID Status Shipper"
    ).get_by_role("checkbox").click()

    page.wait_for_timeout(4000)

    page.get_by_role(
        "button",
        name="Bulk Actions"
    ).click()

    page.get_by_role(
        "menuitem",
        name="Update Tracking Status"
    ).click()

    expect(
        page.get_by_text("Updated Successfully")
    ).to_be_visible(timeout=15000)

    print("Shipment status updated successfully")



def eshipz_custompage_flow(page, order_name):

    login(page)

    page.goto(
        "https://uat.eshipz.com:444/v2/fulfillment/orders/new"
    )

    for i in range(10):

        print(f"Searching order sync attempt {i + 1}")

        page.locator(
            "img[alt='Sync Sales Orders']"
        ).click()

        page.wait_for_timeout(4000)

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

        page.wait_for_timeout(4000)

        if page.get_by_text(order_name).count() > 0:
            print("Order synced successfully")
            break

    else:
        raise Exception("Order not synced")

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

    page.get_by_role(
        "textbox",
        name="First Name",
        exact=True
    ).fill("nasir")

    page.locator("#seller-company-name").fill("infosys")
    page.locator("#seller-address-line1").fill("jamia milla")
    page.locator("#seller-address-line2").fill("snt jhones rd")

    page.get_by_role(
        "combobox",
        name="Country India"
    ).click()

    page.get_by_role(
        "option",
        name="India",
        exact=True
    ).click()

    page.locator("#seller-pincode").fill("110020")
    page.locator("#seller-state").fill("dl")
    page.locator("#customer-pincode").fill("110020")
    page.locator("#customer-state").fill("dl")

    page.get_by_role("button", name="Custom Ship").click()
    page.wait_for_timeout(5000)

    import random

    # =====================================
    # PREPAID MAPPING
    # =====================================

    print("\n===== PREPAID MAPPING =====")

    page.locator("#prepaid-carrier").click()

    carrier_options = page.get_by_role("option")

    carrier_count = carrier_options.count()

    carrier_index = random.randint(
        0,
        carrier_count - 1
    )

    carrier_text = (
        carrier_options
        .nth(carrier_index)
        .inner_text()
        .strip()
    )

    carrier_options.nth(
        carrier_index
    ).click()

    print(
        f"Prepaid Carrier: {carrier_text}"
    )

    page.wait_for_timeout(2000)

    # PREPAID VENDOR

    page.locator("#prepaid-vendor").click()

    vendor_options = page.get_by_role("option")

    vendor_count = vendor_options.count()

    vendor_index = random.randint(
        0,
        vendor_count - 1
    )

    vendor_text = (
        vendor_options
        .nth(vendor_index)
        .inner_text()
        .strip()
    )

    vendor_options.nth(
        vendor_index
    ).click()

    print(
        f"Prepaid Vendor: {vendor_text}"
    )

    page.wait_for_timeout(2000)

    # PREPAID SERVICE

    page.locator("#prepaid-service").click()

    service_options = page.get_by_role("option")

    service_count = service_options.count()

    service_index = random.randint(
        0,
        service_count - 1
    )

    service_text = (
        service_options
        .nth(service_index)
        .inner_text()
        .strip()
    )

    service_options.nth(
        service_index
    ).click()

    print(
        f"Prepaid Service: {service_text}"
    )

    page.wait_for_timeout(2000)

    # =====================================
    # COD MAPPING
    # =====================================

    print("\n===== COD MAPPING =====")

    page.get_by_role(
        "combobox",
        name="Carrier",
        exact=True
    ).click()

    carrier_options = page.get_by_role("option")

    carrier_count = carrier_options.count()

    carrier_index = random.randint(
        0,
        carrier_count - 1
    )

    carrier_text = (
        carrier_options
        .nth(carrier_index)
        .inner_text()
        .strip()
    )

    carrier_options.nth(
        carrier_index
    ).click()

    print(
        f"COD Carrier: {carrier_text}"
    )

    page.wait_for_timeout(2000)

    # COD VENDOR

    page.get_by_role(
        "combobox",
        name="Vendor",
        exact=True
    ).click()

    vendor_options = page.get_by_role("option")

    vendor_count = vendor_options.count()

    vendor_index = random.randint(
        0,
        vendor_count - 1
    )

    vendor_text = (
        vendor_options
        .nth(vendor_index)
        .inner_text()
        .strip()
    )

    vendor_options.nth(
        vendor_index
    ).click()

    print(
        f"COD Vendor: {vendor_text}"
    )

    page.wait_for_timeout(2000)

    # COD SERVICE

    page.get_by_role(
        "combobox",
        name="Service",
        exact=True
    ).click()

    service_options = page.get_by_role("option")

    service_count = service_options.count()

    service_index = random.randint(
        0,
        service_count - 1
    )

    service_text = (
        service_options
        .nth(service_index)
        .inner_text()
        .strip()
    )

    service_options.nth(
        service_index
    ).click()

    print(
        f"COD Service: {service_text}"
    )

    page.wait_for_timeout(2000)

    print("\n===== MAPPING COMPLETED =====")

    page.get_by_role("button", name="Ship Order").click()
    print("Shipment created successfully")

    page.get_by_role("button", name="Update Status").click()
    expect(page.get_by_text("Updated Successfully")).to_be_visible(timeout=15000)
    print("Shipment status updated successfully")




def eshipz_createpage_flow(page, order_name):

    login(page)

    page.goto(
        "https://uat.eshipz.com:444/v2/fulfillment/orders/new"
    )

    for i in range(10):

        print(f"Searching order sync attempt {i + 1}")

        page.locator(
            "img[alt='Sync Sales Orders']"
        ).click()

        page.wait_for_timeout(4000)

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

        page.wait_for_timeout(4000)

        if page.get_by_text(order_name).count() > 0:
            print("Order synced successfully")
            break

    else:
        raise Exception("Order not synced")

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

    page.get_by_role(
        "textbox",
        name="First Name",
        exact=True
    ).fill("nasir")

    page.locator("#seller-company-name").fill("infosys")
    page.locator("#seller-address-line1").fill("jamia milla")
    page.locator("#seller-address-line2").fill("snt jhones rd")

    page.get_by_role(
        "combobox",
        name="Country India"
    ).click()

    page.get_by_role(
        "option",
        name="India",
        exact=True
    ).click()

    page.locator("#seller-pincode").fill("110020")
    page.locator("#seller-state").fill("dl")
    page.locator("#customer-pincode").fill("110020")
    page.locator("#customer-state").fill("dl")

    page.get_by_role("button", name="Fetch Now").click()
    page.wait_for_timeout(5000)

    page.locator("div").filter(has_text=re.compile(r"^BLUEDARTforautomation$")).first.click()
    page.locator("div").filter(has_text=re.compile(r"^eTailCODAir$")).first.click()

    page.get_by_role("button", name="Ship Order").click()
    print("Shipment created successfully")

    page.get_by_role("button", name="Update Status").click()
    expect(page.get_by_text("Updated Successfully")).to_be_visible(timeout=15000)
    print("Shipment status updated successfully")



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
