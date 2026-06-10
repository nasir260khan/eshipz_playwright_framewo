import json
import random
import string
from pathlib import Path
from openpyxl import Workbook

EXCEL_NAME = "bulk_order_template.xlsx"

def order_reference():
    return "".join(random.choices(string.ascii_lowercase, k=5))

def generate_mapper_name():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def load_json():
    json_path = Path(__file__).parent.parent / "data" / "bulk_custom_order.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ✅ NOW accepts optional headers argument
def create_excel(headers=None):
    data = load_json()

    source_headers = data["source_headers"]
    expected_values = data["expected_values"].copy()  # ✅ avoid mutating original dict
    expected_values_ui = data.get("expected_values_ui", {}).copy()

    # ✅ if test passes headers, use them; else use JSON headers
    if headers is not None:
        source_headers = headers

    # 🔥 handle dynamic Order ID
    if expected_values.get("OrderiD") == "REF_DYNAMIC":
        expected_values["OrderiD"] = order_reference()

    # ✅ update UI expected value dynamically using generated ref
    if "order-reference" in expected_values_ui:
        expected_values_ui["order-reference"] = expected_values["OrderiD"]

    base_dir = Path(__file__).parent.parent / "data"
    base_dir.mkdir(exist_ok=True)

    excel_path = base_dir / EXCEL_NAME

    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"

    # ✅ Header row
    ws.append(source_headers)

    # ✅ Data row comes from JSON (NO hardcode)
    row = [expected_values[header] for header in source_headers]
    ws.append(row)

    wb.save(excel_path)

    # ✅ return ui expected also (so test can validate edit page)
    return excel_path, expected_values["OrderiD"], expected_values_ui