from utils.config import BASE_URL


def go_to_reverse_create_page(page):
    page.goto(f"{BASE_URL}/v2/return/create-shipment/reverse")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector("#customer-reference", timeout=60000)


def go_to_reverse_list_page(page):
    page.goto(f"{BASE_URL}/v2/return/all")
    page.wait_for_load_state("networkidle")
    page.wait_for_selector("svg.lucide-ellipsis-vertical", timeout=60000)