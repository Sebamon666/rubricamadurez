
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Inicializar la app
app = dash.Dash(__name__)

# Cargar datos (asegúrate de que la ruta del archivo o URL sea correcta)
df = pd.read_csv("https://docs.google.com/spreadsheets/d/ID/export?format=csv")  # Coloca el enlace real aquí
dimensiones = [
    "1. Objetivos Estratégicos", "2. Órgano de gobierno", "3. Modelo de Financiamiento", 
    "4. Rol del Líder", "5. Organigrama y gestión de talento", "6. Modelo de intervención", 
    "7. Comunicación y marketing", "8. Redes", "9. Monitoreo y evaluación", 
    "10. Transparencia & cumplimiento", "11. Sistemas Admin./ Operaciones"
]

df["Promedio"] = df[dimensiones].mean(axis=1, skipna=True)

# Crear gráfico con plotly
fig = px.scatter(
    df,
    x="Promedio",
    y=[0]*len(df),
    color="Promedio",
    color_continuous_scale="RdYlGn",
    size=[10]*len(df),
    height=250
)
fig.update_traces(marker=dict(line=dict(width=1, color='black')))
fig.update_layout(
    xaxis_title="Promedio de madurez (1 a 5)",
    yaxis=dict(visible=False),
    margin=dict(l=10, r=10, t=10, b=10),
    coloraxis_showscale=False
)

# Layout de la app en Dash
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)  # Cambia el puerto si es necesario en Render
