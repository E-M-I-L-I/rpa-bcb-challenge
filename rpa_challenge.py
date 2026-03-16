import os
import json
import pandas as pd
from playwright.sync_api import sync_playwright

# --- CONFIGURAÇÃO DE PASTAS ---
os.makedirs("outputs", exist_ok=True)

def run_challenge():
    with sync_playwright() as p:
        print("[LOG] - Iniciando navegador...")
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()

        # Bloquear requests de anúncios e scripts extras
        context.route(
            "**/*",
            lambda route: route.abort() 
            if any(x in route.request.url for x in ["doubleclick", "ads", "adservice", "googlesyndication"])
            else route.continue_()
        )

        page = context.new_page()

        # -------------------------
        # CENÁRIO 1: TEXT BOX
        # -------------------------
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

        # -------------------------
        # CENÁRIO 2: CHECK BOX
        # -------------------------
        print("[LOG] - Executando Cenário 2: Check Box")
        page.goto("https://demoqa.com/checkbox")
        page.wait_for_timeout(1000)

        # Remover banners e iframes que sobrepõem elementos
        page.evaluate("document.querySelectorAll('iframe, #fixedban').forEach(el => el.remove());")
        page.wait_for_timeout(500)

        # Expandir Home via botão "+"
        page.evaluate("""
            const homeToggle = document.querySelector("#tree-node-home button");
            if(homeToggle) { homeToggle.click(); }
        """)
        page.wait_for_timeout(500)

        # Selecionar checkbox Home
        page.evaluate("""
            const homeBox = document.querySelector("label[for='tree-node-home']");
            if(homeBox) { homeBox.click(); }
        """)
        page.wait_for_timeout(500)

        # Selecionar Commands e General
        page.evaluate("""
            const commandsBox = document.querySelector("label[for='tree-node-commands']");
            if(commandsBox) { commandsBox.click(); }
            const generalBox = document.querySelector("label[for='tree-node-general']");
            if(generalBox) { generalBox.click(); }
        """)
        page.wait_for_timeout(500)

        # Capturar resultado final via JS
        result = page.evaluate("() => document.querySelector('#result')?.innerText || ''")
        print("[OK] Seleção realizada:")
        print(result)
        # -------------------------
        # --- CENÁRIO 3: WEB TABLES ---

        print("[LOG] - Executando Cenário 3: Web Tables")

        page.goto("https://demoqa.com/webtables")

        # remover banners, iframes, rodapé
        page.evaluate("""
            document.querySelectorAll('#fixedban, iframe, footer').forEach(el => el.remove());
        """)
        page.wait_for_timeout(1500)  # aguardar renderização

        # Capturar todas as linhas do tbody
        data = page.evaluate("""
        () => {
            const rows = Array.from(document.querySelectorAll('.web-tables-wrapper table tbody tr'));
            return rows.map(row => {
                const cells = row.querySelectorAll('td');
                if(cells.length < 6) return null; // ignorar linhas vazias
                return {
                    'First Name': cells[0]?.innerText.trim() || '',
                    'Last Name': cells[1]?.innerText.trim() || '',
                    'Age': parseInt(cells[2]?.innerText.trim()) || 0,
                    'Email': cells[3]?.innerText.trim() || '',
                    'Salary': parseInt(cells[4]?.innerText.replace(/[^0-9]/g,'')) || 0,
                    'Department': cells[5]?.innerText.trim() || ''
                };
            }).filter(r => r !== null);
        }
        """)

        # criar DataFrame
        df = pd.DataFrame(data)

        # salvar CSV
        df.to_csv("outputs/webtables_extract.csv", index=False, encoding="utf-8")

        # resumo
        summary = {
            "total_registros": len(df),
            "media_salary": round(df["Salary"].mean(), 2) if not df.empty else 0,
            "registros_por_department": df["Department"].value_counts().to_dict() if not df.empty else {}
        }

        # salvar JSON
        with open("outputs/webtables_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

        print("[OK] Cenário 3 salvo.")
        # CENÁRIO 4: UPLOAD
        # -------------------------
        print("[LOG] - Executando Cenário 4: Upload de arquivo")
        page.goto("https://demoqa.com/upload-download")
        page.set_input_files("#uploadFile", "assets/documento_teste.pdf")
        page.wait_for_timeout(1500)  # garantir que o nome apareça
        uploaded_name = page.locator("#uploadedFilePath").inner_text()
        upload_result = {"arquivo_enviado": uploaded_name}
        with open("outputs/upload_result.json", "w", encoding="utf-8") as f:
            json.dump(upload_result, f, indent=4, ensure_ascii=False)
        print("[OK] Cenário 4 salvo.")

        # -------------------------
        # FINALIZAÇÃO
        # -------------------------
        print("[LOG] - Automação concluída. Fechando navegador...")
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    run_challenge()