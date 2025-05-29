import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://finance.yahoo.com/most-active", wait_until="networkidle", timeout=60000)

        # Accept cookies if popup appears
        try:
            await page.locator('button:has-text("Accept all")').click(timeout=5000)
        except:
            pass

        # Wait for the table rows after JS rendered
        try:
            await page.wait_for_selector('tr.simpTblRow', timeout=15000)
        except:
            print("Timeout waiting for table rows")

        rows = await page.locator('tr.simpTblRow').all()
        print(f"Found {len(rows)} rows.")

        for row in rows:
            cells = await row.locator('td').all_text_contents()
            if len(cells) >= 3:
                symbol = cells[0]
                name = cells[1]
                price = cells[2]
                print(f"{symbol} | {name} | {price}")

        await browser.close()

asyncio.run(run())




