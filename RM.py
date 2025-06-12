
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# Configurar acceso a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# Abrir Google Sheet y leer hoja
spreadsheet = client.open_by_key("1NZ10wA1eN1zjUw6dLLZyXEUSmgJvl7ZI-xP-2B0BQj8")
sheet = spreadsheet.worksheet("Form responses")
data = sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

# Eliminar columnas innecesarias
columnas_a_eliminar = [
    "Año de inicio de la organización (expresado en número)",
    "Selecciona aquella(s) F. Filantrópica(s) con la que tu organización tiene un convenio activo y/o ha trabajado en los últimos años. >> F. Mustakis >> Colaboración",
    "Selecciona aquella(s) F. Filantrópica(s) con la que tu organización tiene un convenio activo y/o ha trabajado en los últimos años. >> F. MC >> Colaboración",
    "Selecciona aquella(s) F. Filantrópica(s) con la que tu organización tiene un convenio activo y/o ha trabajado en los últimos años. >> F. Olivo >> Colaboración",
    "Selecciona aquella(s) F. Filantrópica(s) con la que tu organización tiene un convenio activo y/o ha trabajado en los últimos años. >> F. Colunga >> Colaboración",
    "Selecciona aquella(s) F. Filantrópica(s) con la que tu organización tiene un convenio activo y/o ha trabajado en los últimos años. >> F. Luksic >> Colaboración",
]
columnas_a_eliminar += [col for col in df.columns if col.startswith("Si tienes algún comentario o sugerencia acerca de esta sección")]
df = df.drop(columns=columnas_a_eliminar, errors="ignore")

# Filtrar y convertir puntajes
dimension_cols = [col for col in df.columns if re.match(r"^([1-9]|10|11)\.", col)]
for col in dimension_cols:
    df[col + " (puntaje)"] = df[col].str.extract(r"^(\d+)").astype(float)

puntaje_cols = [col for col in df.columns if col.endswith("(puntaje)")]
df["Promedio"] = df[puntaje_cols].mean(axis=1)

# Diagnóstico de columnas reales
print("Columnas reales:", df.columns.tolist())

# Agrupación
df_agrupado = df.groupby("Nombre de la organización")["Promedio"].mean().sort_values()

# Graficar
plt.figure(figsize=(10, 8))
df_agrupado.plot(kind="barh")
plt.xlabel("Promedio de Madurez")
plt.title("Promedio de Madurez por Organización")
plt.xlim(0, 5)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f"))

plt.tight_layout()
plt.savefig("madurez.png")
