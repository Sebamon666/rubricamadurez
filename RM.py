import pandas as pd
import plotly.express as px
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

# Graficar con Plotly
fig = px.bar(
    df_agrupado,
    x=df_agrupado.index,
    y="Promedio",
    labels={"Promedio": "Promedio de Madurez"},
    title="Promedio de Madurez por Organización",
    color="Promedio",
    color_continuous_scale="RdYlGn",
    height=500
)

fig.update_layout(
    xaxis_title="Organización",
    yaxis_title="Promedio de Madurez",
    xaxis_tickangle=-45,
    yaxis=dict(range=[0, 5]),
    margin=dict(l=10, r=10, t=10, b=10)
)

fig.show()
