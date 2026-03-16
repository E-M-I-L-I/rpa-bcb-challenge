from playwright.sync_api import sync_playwright
import pandas as pd
import json
import os

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def text_box(page):

    page.goto("https://demoqa.com/text-box")

    page.fill("#userName", "John Doe")
    page.fill("#userEmail", "john@email.com")
    page.fill("#currentAddress", "Rua Teste 123")
    page.fill("#permanentAddress", "Rua Permanente 456")

    page.click("#submit")

    result = page.locator("#output").inner_text()

    data = {"resultado": result}

    with open(f"{OUTPUT_DIR}/text_box_result.json", "w") as f:
        json.dump(data, f, indent=4)


def check_box(page):

    page.goto("https://demoqa.com/checkbox")

    page.click(".rct-option-expand-all")

    page.locator("label:has-text('Commands')").click()
    page.locator("label:has-text('General')").click()


def web_tables(page):

    page.goto("https://demoqa.com/webtables")

    rows = page.locator(".rt-tbody .rt-tr-group")

    data = []

    for i in range(rows.count()):
        row = rows.nth(i).inner_text().split("\n")

        if len(row) >= 6:
            data.append(row[:6])

    df = pd.DataFrame(data, columns=[
        "First Name","Last Name","Age","Email","Salary","Department"
    ])

    df.to_csv(f"{OUTPUT_DIR}/webtables_extract.csv", index=False)

    df["Salary"] = pd.to_numeric(df["Salary"])

    summary = {
        "total_registros": len(df),
        "media_salary": df["Salary"].mean(),
        "registros_por_department": df["Department"].value_counts().to_dict()
    }

    with open(f"{OUTPUT_DIR}/webtables_summary.json", "w") as f:
        json.dump(summary, f, indent=4)


def upload(page):

    page.goto("https://demoqa.com/upload-download")

    file_path = os.path.abspath("assets/documento_teste.pdf")

    page.set_input_files("#uploadFile", file_path)

    result = page.locator("#uploadedFilePath").inner_text()

    data = {
        "arquivo_enviado": result
    }

    with open(f"{OUTPUT_DIR}/upload_result.json", "w") as f:
        json.dump(data, f, indent=4)


def run():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width":1920,"height":1080})

        page = context.new_page()

        text_box(page)
        check_box(page)
        web_tables(page)
        upload(page)

        browser.close()


if __name__ == "__main__":
    run()