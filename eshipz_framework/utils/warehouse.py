import random, time
from playwright.sync_api import expect
from utils.config import BASE_URL


created_warehouses = []
edited_warehouses = []
deleted_warehouses = []


def phone():
    return "9" + "".join(str(random.randint(0, 9)) for _ in range(9))


def warehouse_data(w_type):
    unique = int(time.time() * 1000)
    return {
        "type": w_type,
        "alias": f"CREATE_{w_type}_{unique}",
        "company": f"{w_type} Company",
        "contact": f"{w_type} Contact",
        "email": f"{w_type.lower()}{unique}@gmail.com",
        "phone": phone(),
        "address1": f"{w_type} Address {unique}",
        "address2": f"{w_type} Address Line 2",
        "address3": f"{w_type} Address Line 3",
        "state": "Delhi",
        "city": "Delhi",
        "pincode": "110020",
    }


def open_warehouse_list(page):
    page.goto(f"{BASE_URL}/v2/settings/shipping-setup/warehouse-list", wait_until="domcontentloaded")
    expect(page.get_by_role("button", name="Add new Warehouse")).to_be_visible(timeout=30000)


def search_warehouse(page, alias):

    print(f"\nSearching warehouse: {alias}")

    search_box = page.get_by_role(
        "textbox",
        name="Search by name, address..."
    )

    # clear search
    search_box.click()
    search_box.press("Control+A")
    search_box.press("Backspace")

    page.wait_for_timeout(1000)

    # search warehouse
    search_box.fill(alias)

    # IMPORTANT WAIT
    page.wait_for_timeout(8000)

    # try multiple locator strategies
    warehouse_locator = page.get_by_text(alias, exact=False)

    count = warehouse_locator.count()

    print(f"Matched warehouse count: {count}")

    if count > 0:
        expect(warehouse_locator.first).to_be_visible(timeout=20000)
        print(f"✅ Warehouse found: {alias}")
        return True

    # fallback strategy
    page.wait_for_timeout(5000)

    warehouse_locator = page.locator(f"text={alias}")

    count = warehouse_locator.count()

    print(f"Fallback matched count: {count}")

    if count > 0:
        expect(warehouse_locator.first).to_be_visible(timeout=20000)
        print(f"✅ Warehouse found using fallback: {alias}")
        return True

    # debug print
    try:
        print("\n===== PAGE CONTENT DEBUG =====")
        print(page.locator("body").inner_text()[:5000])
    except:
        pass

    raise AssertionError(f"Warehouse not found after search: {alias}")

def select_type(page, w_type):
    page.get_by_role("combobox").first.click()
    page.get_by_role("option", name=w_type, exact=True).click()


def fill_form(page, data):
    fields = {
        "Alias Name *": data["alias"],
        "Company Name *": data["company"],
        "Contact Name *": data["contact"],
        "Email Address *": data["email"],
        "Phone Number *": data["phone"],
        "Address Line 1 *": data["address1"],
        "Address Line 2": data["address2"],
        "Address Line 3": data["address3"],
        "City *": data["city"],
        "Pincode *": data["pincode"],
    }

    for name, value in fields.items():
        page.get_by_role("textbox", name=name).fill(value)

    page.get_by_role("combobox", name="Country * India").click()
    page.get_by_role("option", name="India", exact=True).click()

    page.get_by_role("combobox", name="State *").click()
    page.get_by_role("combobox", name="State *").fill(data["state"])
    page.get_by_role("option", name=data["state"], exact=True).click()


def validate_form(page, data):
    checks = {
        "Alias Name *": data["alias"],
        "Company Name *": data["company"],
        "Contact Name *": data["contact"],
        "Email Address *": data["email"],
        "Phone Number *": data["phone"],
        "Address Line 1 *": data["address1"],
        "City *": data["city"],
        "Pincode *": data["pincode"],
    }

    for name, value in checks.items():
        expect(page.get_by_role("textbox", name=name)).to_have_value(value, timeout=10000)


def create_warehouse(page, w_type):
    data = warehouse_data(w_type)

    open_warehouse_list(page)
    page.get_by_role("button", name="Add new Warehouse").click()

    select_type(page, w_type)
    fill_form(page, data)

    page.get_by_role("checkbox", name="Set As Primary For This").check()
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_role("heading", name="Warehouse Created Successfully")).to_be_visible(timeout=15000)
    page.get_by_role("button", name="Close").click()

    created_warehouses.append(data)
    return data


def edit_warehouse(page, data):

    open_warehouse_list(page)

    # IMPORTANT
    page.reload()

    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(5000)

    search_warehouse(page, data["alias"])

    page.get_by_role("button", name="Edit Warehouse").first.click()
    validate_form(page, data)

    edited = data.copy()
    edited["company"] = f"EDIT {data['type']} Company"
    edited["contact"] = f"EDIT {data['type']} Contact"
    edited["city"] = "Gurgaon"
    edited["pincode"] = "122001"

    page.get_by_role("textbox", name="Company Name *").fill(edited["company"])
    page.get_by_role("textbox", name="Contact Name *").fill(edited["contact"])
    page.get_by_role("textbox", name="City *").fill(edited["city"])
    page.get_by_role("textbox", name="Pincode *").fill(edited["pincode"])

    page.get_by_role("button", name="Update").click()
    expect(page.get_by_role("heading", name="Warehouse Updated Successfully")).to_be_visible(timeout=15000)
    page.get_by_role("button", name="Close").click()

    edited_warehouses.append(edited)
    return edited

def validate_warehouse_visible_in_create_shipment(page, shipper_data, receiver_data, rto_data):

    print("\n===== VALIDATING WAREHOUSE VISIBILITY IN CREATE SHIPMENT =====")

    page.goto(f"{BASE_URL}/v2/fulfillment/create-shipment")

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(5000)

    # ==========================================================
    # PICKUP WAREHOUSE VALIDATION
    # ==========================================================

    print(f"\nChecking Pickup warehouse: {shipper_data['alias']}")

    page.locator("#sender").click()

    page.wait_for_timeout(3000)

    pickup_visible = page.get_by_text(
        shipper_data["alias"],
        exact=False
    )

    expect(pickup_visible.first).to_be_visible(timeout=15000)

    print(f"✅ Pickup warehouse displayed: {shipper_data['alias']}")

    page.keyboard.press("Escape")

    page.wait_for_timeout(2000)

    # ==========================================================
    # RECEIVER WAREHOUSE VALIDATION
    # ==========================================================

    print(f"\nChecking Receiver warehouse: {receiver_data['alias']}")

    receiver_dropdown = page.locator('div[role="combobox"]').nth(1)

    receiver_dropdown.click()

    page.wait_for_timeout(3000)

    receiver_visible = page.get_by_text(
        receiver_data["alias"],
        exact=False
    )

    expect(receiver_visible.first).to_be_visible(timeout=15000)

    print(f"✅ Receiver warehouse displayed: {receiver_data['alias']}")

    page.keyboard.press("Escape")

    page.wait_for_timeout(2000)

    # ==========================================================
    # RTO WAREHOUSE VALIDATION
    # ==========================================================

    print(f"\nChecking RTO warehouse: {rto_data['alias']}")

    rto_dropdown = page.locator('div[role="combobox"]').nth(2)

    rto_dropdown.click()

    page.wait_for_timeout(3000)

    rto_visible = page.get_by_text(
        rto_data["alias"],
        exact=False
    )

    expect(rto_visible.first).to_be_visible(timeout=15000)

    print(f"✅ RTO warehouse displayed: {rto_data['alias']}")

    page.keyboard.press("Escape")

    print("\n✅ ALL CREATED WAREHOUSES ARE DISPLAYED")


def delete_warehouse(page, data):
    alias = data["alias"]
    warehouse_type = data["type"]

    print(f"\n===== Deleting {warehouse_type} Warehouse: {alias} =====")

    # 1. Open edit page and uncheck primary
    open_warehouse_list(page)
    search_warehouse(page, alias)

    page.get_by_role("button", name="Edit Warehouse").first.click()
    page.wait_for_timeout(2000)

    checkbox = page.get_by_role("checkbox", name="Set As Primary For This")
    if checkbox.is_checked():
        checkbox.uncheck()
        page.get_by_role("button", name="Update").click()

        expect(page.get_by_role("heading", name="Warehouse Updated Successfully")).to_be_visible(timeout=15000)
        page.get_by_role("button", name="Close").click()
        page.wait_for_timeout(2000)

    # 2. VERY IMPORTANT: come back to list page before delete
    open_warehouse_list(page)
    search_warehouse(page, alias)

    # 3. Delete from list page
    delete_btn = page.get_by_role("button", name="Delete Warehouse").first

    if delete_btn.count() == 0:
        print(f"❌ Delete button not found for warehouse: {alias}")
        return False

    delete_btn.click()
    page.wait_for_timeout(1000)

    page.get_by_role("button", name="Confirm").click()
    page.wait_for_timeout(3000)

    deleted_warehouses.append(data)
    print(f"🗑️ Deleted warehouse: {alias}")

    return True


def validate_deleted(page, alias):

    open_warehouse_list(page)

    search_box = page.get_by_role("textbox", name="Search by name, address...")
    search_box.click()
    search_box.fill("")
    search_box.fill(alias)

    page.wait_for_timeout(3000)

    count = page.get_by_text(alias, exact=False).count()

    if count == 0:
        print(f"✅ Deleted successfully. Warehouse not found: {alias}")
        return True

    else:
        print(f"❌ Delete failed. Warehouse still found: {alias}")
        return False