import subprocess

print("🚀 Iniciando RPA...")

subprocess.run(["python", "rpa/main.py"])

print("📊 Abrindo dashboard...")

subprocess.run(["streamlit", "run", "dashboard/app.py"])