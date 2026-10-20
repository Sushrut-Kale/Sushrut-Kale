#!/usr/bin/env python3
import asyncio
import os
from playwright.async_api import async_playwright

async def capture():
    os.makedirs("docs/proof", exist_ok=True)
    svg_path = os.path.abspath("assets/naruto-contrib-dark.svg")
    url = f"file:///{svg_path.replace(os.sep, '/')}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 900, "height": 300})
        await page.goto(url)

        # t = 0s
        await page.screenshot(path="docs/proof/strike-t0s.png")
        print("Captured docs/proof/strike-t0s.png")

        # t = 4s
        await asyncio.sleep(4)
        await page.screenshot(path="docs/proof/strike-t4s.png")
        print("Captured docs/proof/strike-t4s.png")

        # t = 8s
        await asyncio.sleep(4)
        await page.screenshot(path="docs/proof/strike-t8s.png")
        print("Captured docs/proof/strike-t8s.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
