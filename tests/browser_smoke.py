#!/usr/bin/env python3
# Optional Selenium browser smoke test; HTTP validation is in smoke_test.py.
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

EXPECTED_TITLE = "ReleaseForge — Ship with confidence"

def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <website-url>", file=sys.stderr)
        return 2
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(sys.argv[1])
        if driver.title != EXPECTED_TITLE:
            print(f"FAIL: expected {EXPECTED_TITLE!r}, got {driver.title!r}")
            return 1
        if "Ship better." not in driver.page_source:
            print("FAIL: expected hero content is missing")
            return 1
        print("PASS: browser title and expected page content verified")
        return 0
    finally:
        driver.quit()

if __name__ == "__main__":
    raise SystemExit(main())
