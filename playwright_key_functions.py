# cricket_news_bing_xpath.py
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser (visible mode)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Step 1: Open Bing
        await page.goto("https://www.bing.com")

        # Step 2: Use your provided XPath to type the query
        search_box = await page.wait_for_selector('xpath=//*[@id="sb_form_q"]')
        await search_box.fill("India cricket match latest news")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)  # Wait for results to load

        # Step 3: Extract top 5 news result titles and URLs
        print("\n📰 Top Cricket News from Bing:")
        results = await page.query_selector_all("li.b_algo h2 a")

        for i, result in enumerate(results[:5]):
            title = await result.inner_text()
            link = await result.get_attribute("href")
            print(f"{i+1}. {title} → {link}")

        # Step 4: Close the browser
        await browser.close()

# Run the async function
asyncio.run(run())
