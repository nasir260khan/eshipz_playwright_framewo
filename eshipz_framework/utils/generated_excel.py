import os
import random
import string
import openpyxl


def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_excel_file():
    PROJECT_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    excel_path = os.path.join(
        PROJECT_ROOT,
        "downloadedfiles",
        "ordersexcel",
        "eshipz_import_orders_sample.xlsx"
    )

    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel template not found: {excel_path}")

    wb = openpyxl.load_workbook(excel_path)
    sh = wb["bulk_upload"]


    country_code_map = {"India": "IN"}
    country_state_map = {"India": "DL"}
    countries = list(country_code_map.keys())

    bulk_rows = 2
    generated_orders = []

    for j in range(2, 2 + bulk_rows):
        order_reference = generate_random_string(5)
        generated_orders.append(order_reference)
        country_choice = random.choice(countries)
        country_code = country_code_map[country_choice]
        country_state = country_state_map[country_choice]

        values = [
            "shopify", order_reference, "fan2", "sku007", "book", "",
            "30", "KG", "300", "20", "1", "30", "2", "3", "4",
            "CM", "INR", "", "", "", "True", "False", "200", "500",
            "INR", "", "", "233", "", "78987656545", "", "",
            "riyuzaki", "riyu", "infosys", "kjs street",
            "addr1", "addr2",
            "Delhi", country_state, "",
            country_choice, country_code, "110002",
            "7878787878", "riyu@gmail.com",
            "jhon", "jhones", "eshipz",
            "shipper street1", "shipper street2",
            "Bangalore", "Delhi", country_state, country_state,
            country_choice, country_code, "110002",
            "9898989898", "jhon@gmail.com"
        ]

        for col, val in enumerate(values, start=1):
            sh.cell(row=j, column=col).value = val

    output_file = os.path.join(
        PROJECT_ROOT,
        f"bulk_{generate_random_string(6)}.xlsx"
    )

    wb.save(output_file)

    return output_file, generated_orders
