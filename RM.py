
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurar acceso a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# Abrir Google Sheet y leer hoja
spreadsheet = client.open("Diagnóstico Madurez")
sheet = spreadsheet.worksheet("Vaciado")
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Calcular promedio
puntaje_cols = [col for col in df.columns if "(puntaje)" in col]
df["Promedio"] = df[puntaje_cols].mean(axis=1)

# Mostrar promedio (para debugging)
print(df["Promedio"].head())

# Agrupar por organización
df_agrupado = df.groupby("Organización")["Promedio"].mean().sort_values()

# Graficar
plt.figure(figsize=(10, 8))
df_agrupado.plot(kind="barh")
plt.xlabel("Promedio de Madurez")
plt.title("Promedio de Madurez por Organización")
plt.xlim(0, 100)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter())

plt.tight_layout()
plt.savefig("madurez.png")
