import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, send_file
import requests
import io

app = Flask(__name__)

URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQM-bgAgav2avRRbMiSI_Qz4-w7MZ5b6NdnOeAZxpi7rYr1AarsQa9fFhEsnyBJGBe_jrc6jPNRuxu5/pub?gid=165088231&single=true&output=csv"

@app.route("/")
def grafico():
    r = requests.get(URL_CSV)
    df = pd.read_csv(io.StringIO(r.text))

    puntaje_cols = [col for col in df.columns if "(puntaje)" in col]
    df[puntaje_cols] = df[puntaje_cols].apply(pd.to_numeric, errors="coerce")
    df["Promedio"] = df[puntaje_cols].mean(axis=1)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.scatter(df["Promedio"], [1] * len(df), color="black", s=60)

    ax.set_yticks([])
    ax.set_xlabel("Promedio de madurez (1 a 5)", fontsize=12)
    ax.set_title("Distribución de las organizaciones según su nivel de madurez", fontsize=14, weight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.set_xlim(1, 5)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
