from utils.login import login

from utils.warehouse import (
    create_warehouse,
    edit_warehouse,
    delete_warehouse,
    validate_deleted,
    created_warehouses,
    edited_warehouses,
    deleted_warehouses,
    validate_warehouse_visible_in_create_shipment,
)

from utils.excelwarehousefunction import upload_and_validate_warehouse_excel


def test_all_warehouse_cases(page):

    login(page)

    print("\n========== CASE 1: CREATE EDIT DELETE WAREHOUSE ==========")

    # ==========================================================
    # CREATE WAREHOUSES
    # ==========================================================

    pickup_data = create_warehouse(page, "Pickup")
    receiver_data = create_warehouse(page, "Receiver")
    rto_data = create_warehouse(page, "RTO")

    # ==========================================================
    # EDIT WAREHOUSES
    # ==========================================================

    edit_warehouse(page, pickup_data)
    edit_warehouse(page, receiver_data)
    edit_warehouse(page, rto_data)

    # ==========================================================
    # VALIDATE IN CREATE SHIPMENT PAGE
    # ==========================================================

    validate_warehouse_visible_in_create_shipment(
        page,
        pickup_data,
        receiver_data,
        rto_data
    )

    # ==========================================================
    # DELETE VALIDATION
    # ==========================================================

    delete_failed = []

    for data in created_warehouses:

        deleted = delete_warehouse(page, data)

        if not deleted:
            print(f"❌ Delete action failed: {data['alias']}")
            delete_failed.append(data["alias"])
            continue

        is_deleted = validate_deleted(page, data["alias"])

        if is_deleted:
            print(f"✅ Warehouse deleted successfully: {data['alias']}")
        else:
            print(f"❌ Warehouse not deleted: {data['alias']}")
            delete_failed.append(data["alias"])

    # ==========================================================
    # SUMMARY
    # ==========================================================

    print("\nCreated:")
    for item in created_warehouses:
        print("✅", item["alias"])

    print("\nEdited:")
    for item in edited_warehouses:
        print("✏️", item["alias"])

    print("\nDeleted:")
    for item in deleted_warehouses:
        print("🗑️", item["alias"])

    if delete_failed:

        print("\nDelete Failed:")

        for item in delete_failed:
            print("❌", item)

        assert False, f"Some warehouses were not deleted: {delete_failed}"

    # ==========================================================
    # EXCEL UPLOAD
    # ==========================================================

    print("\n========== CASE 2: EXCEL UPLOAD WAREHOUSE ==========")

    rows = upload_and_validate_warehouse_excel(page)

    print("\n========== WAREHOUSE EXCEL UPLOAD SUMMARY ==========")

    for row in rows:
        print(f"✅ Uploaded and validated: {row['Display Type']} - {row['Alias Name']}")