from playwright.sync_api import Page, TimeoutError

MAX_RETRY = 20
MAX_SCROLLS = 25   # ✅ more scrolls because Source list is long

def get_target_span(page, target_label):
    return page.locator(
        f"//span[contains(@class,'font-semibold') and normalize-space()='{target_label}']"
    )

def get_source_container(page: Page):
    """
    ✅ Scrollable container that holds Source chips (right side).
    This finds the panel under 'Source Fields (56)' heading.
    """
    return page.locator(
        "xpath=//div[contains(normalize-space(),'Source Fields')]/ancestor::div[1]"
        "//div[(contains(@class,'overflow') or contains(@class,'scroll') or contains(@style,'overflow'))]"
    ).first

def get_target_container(page: Page):
    """
    ✅ Scrollable container that holds Target fields (left side).
    """
    return page.locator(
        "xpath=//div[contains(normalize-space(),'Target Fields')]/ancestor::div[1]"
        "//div[(contains(@class,'overflow') or contains(@class,'scroll') or contains(@style,'overflow'))]"
    ).first

def scroll_in_container(container, delta=350):
    # scroll the container itself (not the page)
    container.evaluate(f"el => el.scrollTop = el.scrollTop + {delta}")

def ensure_visible_in_source(page: Page, source, max_scrolls=MAX_SCROLLS):
    """
    ✅ Make sure SOURCE chip is visible by scrolling inside Source container.
    Tries down first, then up.
    """
    source_container = get_source_container(page)

    # fallback: try normal scroll into view
    try:
        if source.count() > 0 and source.is_visible():
            return True
        source.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        if source.count() > 0 and source.is_visible():
            return True
    except Exception:
        pass

    # if no container found, fallback to page wheel
    if source_container.count() == 0:
        for _ in range(max_scrolls):
            if source.count() > 0 and source.is_visible():
                return True
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(200)
        return source.count() > 0 and source.is_visible()

    # ✅ scroll DOWN inside container
    for _ in range(max_scrolls):
        if source.count() > 0 and source.is_visible():
            source.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            return True
        scroll_in_container(source_container, 350)
        page.wait_for_timeout(200)

    # ✅ scroll UP inside container (in case element is above)
    for _ in range(max_scrolls):
        if source.count() > 0 and source.is_visible():
            source.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            return True
        scroll_in_container(source_container, -350)
        page.wait_for_timeout(200)

    return source.count() > 0 and source.is_visible()

def ensure_visible_in_target(page: Page, target_span, max_scrolls=MAX_SCROLLS):
    """
    ✅ Make sure TARGET label is visible by scrolling inside Target container.
    Uses your arrow logic as fallback.
    """
    target_container = get_target_container(page)

    # quick path
    if target_span.count() > 0 and target_span.is_visible():
        target_span.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        return True

    # scroll inside target container if found
    if target_container.count() > 0:
        for _ in range(max_scrolls):
            if target_span.count() > 0 and target_span.is_visible():
                target_span.scroll_into_view_if_needed()
                page.wait_for_timeout(200)
                return True
            scroll_in_container(target_container, 350)
            page.wait_for_timeout(200)

        for _ in range(max_scrolls):
            if target_span.count() > 0 and target_span.is_visible():
                target_span.scroll_into_view_if_needed()
                page.wait_for_timeout(200)
                return True
            scroll_in_container(target_container, -350)
            page.wait_for_timeout(200)

    # fallback to your previous wheel + arrows logic
    scrolls = 0
    while scrolls < 10:
        if target_span.count() > 0 and target_span.is_visible():
            target_span.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            return True

        arrows = page.locator("svg.lucide-chevron-right")
        for i in range(arrows.count()):
            arrow = arrows.nth(i)
            if arrow.is_visible():
                arrow.scroll_into_view_if_needed()
                arrow.click()
                page.wait_for_timeout(200)
                if target_span.count() > 0 and target_span.is_visible():
                    return True

        page.mouse.wheel(0, 250)
        page.wait_for_timeout(300)
        scrolls += 1

    return target_span.count() > 0 and target_span.is_visible()

def drag_and_drop_with_retry(page, source, target, label, target_label):
    for attempt in range(1, MAX_RETRY + 1):
        try:
            print(f"🔁 Attempt {attempt} → {label} → {target_label}")

            # ✅ 1) Make TARGET visible (left side scroll)
            target_span = get_target_span(page, target_label)
            if not ensure_visible_in_target(page, target_span):
                raise Exception(f"Target not visible → {target_label}")

            # ✅ 2) Make SOURCE visible (right side scroll)
            if not ensure_visible_in_source(page, source):
                raise Exception(f"Source not visible → {label}")

            # ✅ 3) Wait both
            source.wait_for(state="visible", timeout=15000)
            target.wait_for(state="visible", timeout=15000)

            # ✅ 4) Bring to view
            source.scroll_into_view_if_needed()
            target.scroll_into_view_if_needed()
            page.wait_for_timeout(300)

            # ✅ 5) Do a REAL drag (slow + hold)
            s = source.bounding_box()
            t = target.bounding_box()
            if not s or not t:
                raise Exception("Bounding box not available")

            sx = s["x"] + s["width"] / 2
            sy = s["y"] + s["height"] / 2
            tx = t["x"] + t["width"] / 2
            ty = t["y"] + t["height"] / 2

            page.mouse.move(sx, sy, steps=25)
            page.wait_for_timeout(200)

            page.mouse.down()
            page.wait_for_timeout(600)  # ✅ hold to start drag

            # tiny move to trigger drag start
            page.mouse.move(sx + 10, sy + 10, steps=10)
            page.wait_for_timeout(200)

            page.mouse.move(tx, ty, steps=70)  # ✅ slow drag
            page.wait_for_timeout(400)

            page.mouse.up()
            page.wait_for_timeout(800)

            print(f"✅ Mapping completed → {label} → {target_label}")
            return True

        except TimeoutError:
            print("⚠️ Timeout, retrying...")
        except Exception as e:
            print(f"⚠️ {e}, retrying...")

        page.wait_for_timeout(1000)

    raise Exception(f"❌ Failed after {MAX_RETRY} attempts → {label} → {target_label}")