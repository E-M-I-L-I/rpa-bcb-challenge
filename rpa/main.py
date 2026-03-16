import json
import csv
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
ASSETS_DIR = BASE_DIR / "assets"

OUTPUT_DIR.mkdir(exist_ok=True)


def run_rpa():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # -------------------------
        # TEXT BOX
        # -------------------------

        page.goto("https://demoqa.com/text-box")

        page.fill("#userName", "John Doe")
        page.fill("#userEmail", "john@email.com")
        page.fill("#currentAddress", "Rua Teste")
        page.fill("#permanentAddress", "Rua Teste 2")

        page.click("#submit")

        result = page.inner_text("#output")

        with open(OUTPUT_DIR / "text_box_result.json", "w") as f:
            json.dump({"resultado": result}, f, indent=4)

        # -------------------------
        # WEB TABLES
        # -------------------------

        page.goto("https://demoqa.com/webtables")

        rows = page.query_selector_all(".rt-tr-group")

        data = []

        for row in rows:

            text = row.inner_text()
            cells = text.split("\n")

            if len(cells) >= 6:
                data.append(cells[:6])

        with open(OUTPUT_DIR / "webtables_extract.csv", "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow(
                ["First Name", "Last Name", "Age", "Email", "Salary", "Department"]
            )

            writer.writerows(data)

        # -------------------------
        # UPLOAD
        # -------------------------

        page.goto("https://demoqa.com/upload-download")

        file_path = ASSETS_DIR / "documento_teste.pdf"

        page.set_input_files("#uploadFile", str(file_path))

        with open(OUTPUT_DIR / "upload_result.json", "w") as f:
            json.dump({"upload": "success"}, f, indent=4)

        browser.close()


if __name__ == "__main__":
    run_rpa()