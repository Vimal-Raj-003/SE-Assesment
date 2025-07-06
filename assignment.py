from playwright.sync_api import sync_playwright
import time
import pandas as pd

def extract_metadata_from_card(card):
    try:
        name = card.locator("div[aria-label]").first
        name_text = name.inner_text().strip() if name else "N/A"

        rating = card.locator("span[aria-hidden='true']").first
        rating_text = rating.inner_text().strip() if rating else "N/A"

        category = card.locator("span").nth(1)
        category_text = category.inner_text().strip() if category else "N/A"

        address = card.locator("div[jsinstance='0'] div:nth-child(2) span").first
        address_text = address.inner_text().strip() if address else "N/A"

        return {
            "Business Name": name_text,
            "Rating": rating_text,
            "Category": category_text,
            "Address": address_text
        }
    except Exception as e:
        print("[!] Error parsing card:", e)
        return {}

def scroll_results(page, max_scrolls=10, delay=2.5):
    print("[✓] Scrolling results to load cards...")
    scrollable = page.locator("div[role='region']")

    prev_card_count = 0
    for i in range(max_scrolls):
        scrollable.evaluate("el => el.scrollBy(0, 1000)")
        time.sleep(delay)

        cards = page.locator("div[role='article']")
        card_count = cards.count()
        print(f"[Scroll {i+1}] Cards loaded: {card_count}")

        if card_count == prev_card_count:
            print("[✓] No new cards loaded. Stopping scroll.")
            break

        prev_card_count = card_count

def write_to_csv(data_list, file_name='google_maps_data.csv'):
    df = pd.DataFrame(data_list)
    df.to_csv(file_name, index=False, encoding='utf-8')
    print(f"[✔] Data saved to {file_name}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)

        search_query = "coffee shops in Chennai"
        page.fill("input#searchboxinput", search_query)
        page.click("button#searchbox-searchbutton")
        page.wait_for_timeout(5000)

        scroll_results(page)

        all_data = []
        cards = page.locator("div[role='article']")
        total_cards = cards.count()
        print(f"[✓] Found {total_cards} cards after scroll.")

        for i in range(total_cards):
            card = cards.nth(i)
            metadata = extract_metadata_from_card(card)
            if metadata:
                print(f"[{i+1}] {metadata['Business Name']}")
                all_data.append(metadata)

        if all_data:
            write_to_csv(all_data)
        else:
            print("[!] No data extracted.")

        browser.close()

if __name__ == "__main__":
    main()
