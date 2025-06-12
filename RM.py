import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
import base64
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def render_plot():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQM-bgAgav2avRRbMiSI_Qz4-w7MZ5b6NdnOeAZxpi7rYr1AarsQa9fFhEsnyBJGBe_jrc6jPNRuxu5/pub?gid=165088231&single=true&output=csv"
    response = requests.get(url)
    data = StringIO(response.text)
    df = pd.read_csv(data)

    puntaje_cols = [col for col in df.columns if "(puntaje)" in col]
    df["Promedio"] = df[puntaje_cols].mean(axis=1)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.scatter(df["Promedio"], [1]*len(df), color='black', s=60)
    ax.set_yticks([])
    ax.set_xlabel("Promedio de madurez (1 a 5)", fontsize=12)
    ax.set_title("Distribución de organizaciones según su nivel de madurez", fontsize=14, weight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.set_xlim(1, 5)
    plt.tight_layout()

    img = StringIO()
    plt.savefig(img, format='svg')
    plt.close(fig)
    img.seek(0)
    return Response(img.getvalue(), mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=False)