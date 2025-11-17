import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import requests
import numpy as np
from datetime import datetime, timedelta

dash.register_page(__name__, path="/pagina9", name="Pagina 9")

# ==================================================
# SUNAT API
# ==================================================
def obtener_tc_sunat():
    try:
        url = "https://api.apis.net.pe/v1/tipo-cambio-sunat"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except:
        return None

# ==================================================
# Layout
# ==================================================
layout = html.Div(
    [
        html.Div(
            [
                html.H2("Tipo de Cambio – SUNAT Perú", className="title"),

                html.Label("Tipo de análisis:"),
                dcc.RadioItems(
                    id="tipo-analisis",
                    options=[
                        {"label": " Compra", "value": "compra"},
                        {"label": " Venta", "value": "venta"},
                        {"label": " Spread", "value": "spread"},
                    ],
                    value="compra",
                    className="radio-gold",
                ),

                html.Br(),

                html.Button(
                    "Actualizar Valores",
                    id="btn-tc",
                    className="btn-generar",
                ),

                html.Div(
                    id="mensaje-sunat",
                    className="clima-info-box",
                    style={"marginTop": "10px"},
                ),
            ],
            className="content left",
        ),

        html.Div(
            [
                html.H2("Evolución Modelada del Tipo de Cambio", className="title"),

                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("Compra", className="card-title temp"),
                                html.H3(id="sunat-compra", className="card-value temp"),
                            ],
                            className="clima-card",
                        ),
                        html.Div(
                            [
                                html.H4("Venta", className="card-title humedad"),
                                html.H3(id="sunat-venta", className="card-value humedad"),
                            ],
                            className="clima-card",
                        ),
                        html.Div(
                            [
                                html.H4("Spread", className="card-title viento"),
                                html.H3(id="sunat-spread", className="card-value viento"),
                            ],
                            className="clima-card",
                        ),
                    ],
                    className="clima-card-container",
                ),

                dcc.Graph(id="grafico-sunat", style={"height": "380px"}),
            ],
            className="content right",
        ),
    ],
    className="page-container page8-container",
)

# ==================================================
# CALLBACK
# ==================================================
@callback(
    Output("grafico-sunat", "figure"),
    Output("sunat-compra", "children"),
    Output("sunat-venta", "children"),
    Output("sunat-spread", "children"),
    Output("mensaje-sunat", "children"),
    Input("btn-tc", "n_clicks"),
    State("tipo-analisis", "value"),
)
def actualizar_tc_sunat(n_clicks, tipo):
    datos = obtener_tc_sunat()

    if not datos:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgb(40,40,40)",
            plot_bgcolor="rgb(50,48,47)",
            font=dict(color="white"),
            title="No se pudo obtener datos."
        )
        return fig, "-", "-", "-", "❌ Error API SUNAT"

    compra = float(datos["compra"])
    venta = float(datos["venta"])
    spread = round(venta - compra, 4)

    # --------------------------------------
    # Modelo matemático: Proceso OU (realista)
    # --------------------------------------
    pasos = 14
    dt = 1 / pasos
    theta = 0.35
    sigma = 0.008

    if tipo == "compra":
        x0 = compra
    elif tipo == "venta":
        x0 = venta
    else:
        x0 = spread

    serie = [x0]
    for _ in range(pasos):
        dx = theta * (x0 - serie[-1]) * dt + sigma * np.random.randn()
        serie.append(serie[-1] + dx)

    fechas = [datetime.now() + timedelta(days=i) for i in range(pasos + 1)]

    # --------------------------------------
    # FIGURA — TEMA GRUVBOX
    # --------------------------------------
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=fechas,
            y=serie,
            mode="lines+markers",
            line=dict(color="#ffb74d", width=3),
            marker=dict(size=7),
            name="Predicción OU",
        )
    )

    fig.update_layout(
        title=f"Proyección SUNAT – {tipo.capitalize()}",
        plot_bgcolor="rgb(50,48,47)",
        paper_bgcolor="rgb(40,40,40)",
        font=dict(color="rgb(213,196,161)", family="Outfit"),
        xaxis_title="Fecha",
        yaxis_title="Tipo de cambio (S/.)",
        margin=dict(l=40, r=40, t=60, b=40),
    )

    mensaje = f"✔ Datos oficiales SUNAT — Fecha: {datos['fecha']}"

    return (
        fig,
        f"S/ {compra:.3f}",
        f"S/ {venta:.3f}",
        f"S/ {spread:.3f}",
        mensaje,
    )
