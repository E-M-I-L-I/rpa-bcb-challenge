from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) # Headed para você ver acontecendo
    page = browser.new_page()
    page.goto("https://demoqa.com/text-box")
    print(f"Título da página: {page.title()}")
    browser.close()