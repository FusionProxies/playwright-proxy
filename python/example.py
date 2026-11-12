"""Playwright (Python) with Fusion Proxy residential proxies.

Each browser context gets its own sticky session, so every page in that
context keeps one residential IP, and a new context gets a new IP.

pip install -r requirements.txt && playwright install chromium
export FUSION_USER=... FUSION_PASS=... [FUSION_COUNTRY=us]
"""
import os
import random

from playwright.sync_api import sync_playwright

USER = os.environ["FUSION_USER"]
PASS = os.environ["FUSION_PASS"]
COUNTRY = os.environ.get("FUSION_COUNTRY", "us")


def sticky_proxy(minutes: int = 10) -> dict:
    session = random.randint(1000000, 9999999)
    return {
        "server": "http://resi.fusionproxy.net:12286",
        "username": f"{USER}-country-{COUNTRY}-sessid-{session}-sessTime-{minutes * 60}s",
        "password": PASS,
    }


with sync_playwright() as p:
    # contexts set their own proxy below; the launch value is only a placeholder
    # that some Chromium builds need before per-context proxies work
    browser = p.chromium.launch(proxy={"server": "http://per-context"})

    for n in range(1, 3):
        context = browser.new_context(proxy=sticky_proxy())
        page = context.new_page()
        page.goto("https://ipinfo.io/json", timeout=60_000)
        print(f"context {n}:", page.locator("body").inner_text().replace("\n", " ")[:120])
        context.close()

    browser.close()
