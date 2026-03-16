import os
import json
import pandas as pd
from playwright.sync_api import sync_playwright

# --- CONFIGURAÇÃO DE PASTAS ---
os.makedirs("outputs", exist_ok=True)

def run_challenge():
    with sync_playwright() as p:
        print("[LOG] - Iniciando navegador...")
        browser = p.chromium.launch(headless=False, slow_mo=250, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # --- CENÁRIO 1: TEXT BOX ---
        print("[LOG] - Executando Cenário 1: Text Box")
        page.goto("https://demoqa.com/text-box")
        page.fill("#userName", "Emilio RPA Developer")
        page.fill("#userEmail", "emilio@exemplo.com")
        page.fill("#currentAddress", "Rua das Automações, 123")
        page.fill("#permanentAddress", "Avenida do Python, 456")
        page.click("#submit")
        result_text = page.locator("#output").inner_text()
        with open("outputs/text_box_result.json", "w", encoding="utf-8") as f:
            json.dump({"resultado_exibido": result_text}, f, indent=4, ensure_ascii=False)
        print("[OK] - Cenário 1 salvo.")

        # --- CENÁRIO 2: CHECK BOX ---
        page.goto("https://demoqa.com/checkbox")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)

        # Remover banners
        page.evaluate("""
        document.querySelectorAll('#fixedban, iframe, footer').forEach(el => el.remove());
        """)
        page.wait_for_timeout(500)

        # Esperar o container principal da árvore
        tree_container = page.locator(".check-box-tree-wrapper")
        tree_container.wait_for(state="visible", timeout=60000)

        # Scroll até o nó Home
        home_label = page.locator("label", has_text="Home")
        home_label.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        # Clique forçado (ignora se algo está sobreposto)
        home_label.click(force=True)
        page.wait_for_timeout(500)

        # Validar resultado
        result_text = page.locator("#result").inner_text()
        print("[OK] Checkbox 'Home' marcado:", result_text)
        # --- CENÁRIO 3: WEB TABLES ---
        print("[LOG] - Executando Cenário 3: Web Tables")
        page.goto("https://demoqa.com/webtables")
        page.evaluate("document.querySelectorAll('#fixedban, iframe, footer').forEach(el => el.remove());")
        rows = page.locator(".rt-tr-group")
        data = []
        for i in range(rows.count()):
            cells = rows.nth(i).locator(".rt-td").all_inner_texts()
            if cells and cells[0].strip():
                data.append({
                    "First Name": cells[0],
                    "Last Name": cells[1],
                    "Age": cells[2],
                    "Email": cells[3],
                    "Salary": cells[4],
                    "Department": cells[5]
                })
        df = pd.DataFrame(data)
        df.to_csv("outputs/webtables_extract.csv", index=False, encoding="utf-8")
        df["Salary"] = pd.to_numeric(df["Salary"])
        summary = {
            "total_registros": len(df),
            "media_salary": round(df["Salary"].mean(), 2),
            "registros_por_department": df["Department"].value_counts().to_dict()
        }
        with open("outputs/webtables_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)
        print("[OK] Cenário 3 salvo.")

        # --- CENÁRIO 4: UPLOAD ---
        print("[LOG] - Executando Cenário 4: Upload de arquivo")
        page.goto("https://demoqa.com/upload-download")
        page.set_input_files("#uploadFile", "assets/documento_teste.pdf")
        page.wait_for_timeout(1000)  # dar tempo para aparecer o nome
        uploaded_name = page.locator("#uploadedFilePath").inner_text()
        upload_result = {"arquivo_enviado": uploaded_name}
        with open("outputs/upload_result.json", "w", encoding="utf-8") as f:
            json.dump(upload_result, f, indent=4, ensure_ascii=False)
        print("[OK] Cenário 4 salvo.")

        # --- FINALIZAÇÃO ---
        print("[LOG] - Automação concluída. Fechando navegador...")
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    run_challenge()