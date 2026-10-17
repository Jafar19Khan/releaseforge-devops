#!/usr/bin/env python3
"""Small Selenium smoke test for the ReleaseForge demo website.

Usage: python3 selenium_test.py http://127.0.0.1:8082/devopsIQ/
The browser and compatible driver must be installed on the test runner.
"""
import sys
from urllib.error import URLError
from urllib.request import urlopen

EXPECTED_TITLE = "ReleaseForge | DevOps Deployment Demo"
EXPECTED_MARKER = "ReleaseForge"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <website-url>", file=sys.stderr)
        return 2
    url = sys.argv[1].rstrip("/") + "/"
    try:
        with urlopen(url, timeout=10) as response:
            body = response.read().decode("utf-8", errors="replace")
            if response.status != 200:
                print(f"FAIL: HTTP {response.status}")
                return 1
    except (URLError, TimeoutError, OSError) as exc:
        print(f"FAIL: website is not reachable: {exc}")
        return 1
    if EXPECTED_MARKER not in body or EXPECTED_TITLE not in body:
        print("FAIL: expected ReleaseForge page markers were not found")
        return 1
    print(f"PASS: {url} returned HTTP 200 and expected page markers")
    # Selenium is intentionally optional for the basic assignment smoke test.
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)  # Selenium Manager resolves driver
        try:
            driver.get(url)
            if driver.title != EXPECTED_TITLE:
                print(f"FAIL: title mismatch: {driver.title!r}")
                return 1
            print("PASS: browser title verified with Selenium")
        finally:
            driver.quit()
    except ImportError:
        print("INFO: Selenium is not installed; HTTP smoke test completed. Install requirements-test.txt for browser testing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
