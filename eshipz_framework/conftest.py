# import pytest
#
# from utils.config import BASE_URL
# from utils.login import login
#
# login_done = False
#
#
# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         "record_video_dir": "videos/",
#         "record_video_size": {"width": 1280, "height": 720},
#     }
#
#
# @pytest.fixture
# def logged_in_page(page, context):
#
#     global login_done
#
#     # Optional trace for debugging
#     context.tracing.start(screenshots=True, snapshots=True, sources=True)
#
#     if not login_done:
#         login(page)
#         login_done = True
#     else:
#         page.goto(f"{BASE_URL}/")
#
#     yield page
#
#     # Stop trace
#     context.tracing.stop(path="videos/trace.zip")





import os
import sys
import pytest
from playwright.sync_api import sync_playwright

# Ensure package-local imports like `import utils.*` work when running pytest
# Add workspace root and package dir so both `eshipz_framework.*` and `utils.*` resolve
workspace_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, workspace_root)
sys.path.insert(0, os.path.dirname(__file__))

from .utils.config import BASE_URL
from .utils.login import login

login_done = False


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720}
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def logged_in_page(page):
    global login_done

    if not login_done:
        login(page)
        login_done = True
    else:
        page.goto(f"{BASE_URL}/")

    yield page