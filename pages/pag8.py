import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import requests
from datetime import datetime
import pandas as pd

# =============================
# Registro de Página
# =============================
dash.register_page(__name__, path="/pagina8", name="Pagina 8")

# =============================
# Layout
# =============================
layout = html.Div(
    [
        # --------------------- COLUMNA IZQUIERDA ---------------------
        html.Div(
            [
                html.H2("Dashboard COVID-19 Global", className="title"),

                # Selector país
                html.Div(
                    [
                        html.Label("Selecciona un país:"),
                        dcc.Dropdown(
                            id="dropdown-pais",
                            options=[
                                {'label': '🌎 Perú', 'value': 'Peru'},
                                {'label': '🇺🇸 Estados Unidos', 'value': 'US'},
                                {'label': '🇪🇸 España', 'value': 'Spain'},
                                {'label': '🇲🇽 México', 'value': 'Mexico'},
                                {'label': '🇦🇷 Argentina', 'value': 'Argentina'},
                                {'label': '🇧🇷 Brasil', 'value': 'Brazil'},
                                {'label': '🇨🇴 Colombia', 'value': 'Colombia'},
                                {'label': '🇨🇱 Chile', 'value': 'Chile'},
                                {'label': '🇮🇹 Italia', 'value': 'Italy'},
                                {'label': '🇫🇷 Francia', 'value': 'France'},
                            ],
                            value="Peru",
                            className="dropdown-clima",
                            style={"width": "100%"},
                        ),
                    ],
                    className="input-group",
                ),

                # Selector histórico
                html.Div(
                    [
                        html.Label("Días de histórico:"),
                        dcc.Dropdown(
                            id="dropdown-dias-covid",
                            options=[
                                {'label': '30 días', 'value': 30},
                                {'label': '60 días', 'value': 60},
                                {'label': '90 días', 'value': 90},
                                {'label': 'Todo el histórico', 'value': 'all'},
                            ],
                            value=90,
                            className="dropdown-clima",
                            style={"width": "100%"},
                        ),
                    ],
                    className="input-group",
                ),

                html.Button(
                    "Actualizar Datos",
                    id="btn-actualizar-covid",
                    className="btn-generar",
                ),

                html.Div(
                    id="info-actualizado-covid",
                    className="clima-info-box",
                ),
            ],
            className="content left",
        ),

        # --------------------- COLUMNA DERECHA ---------------------
        html.Div(
            [
                html.H2("Estadísticas en Tiempo Real", className="title"),

                # Cards estilo Pag8
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("Total Casos", className="card-title temp"),
                                html.H3(id="total-casos", className="card-value temp"),
                            ],
                            className="clima-card",
                        ),
                        html.Div(
                            [
                                html.H4("Casos Nuevos Hoy", className="card-title humedad"),
                                html.H3(id="casos-nuevos", className="card-value humedad"),
                            ],
                            className="clima-card",
                        ),
                        html.Div(
                            [
                                html.H4("Total Muertes", className="card-title viento"),
                                html.H3(id="total-muertes", className="card-value viento"),
                            ],
                            className="clima-card",
                        ),
                        html.Div(
                            [
                                html.H4("Recuperados", className="card-title temp"),
                                html.H3(id="total-recuperados", className="card-value temp"),
                            ],
                            className="clima-card",
                        ),
                    ],
                    className="clima-card-container",
                ),

                dcc.Graph(
                    id="grafica-covid",
                    style={"height": "380px", "width": "100%"},
                ),
            ],
            className="content right",
        ),
    ],
    className="page-container page8-container",
)

# ==========================================================
# Funciones API disease.sh
# ==========================================================
def obtener_datos_pais(pais):
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{pais}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None


def obtener_historico_pais(pais, dias):
    try:
        url = f"https://disease.sh/v3/covid-19/historical/{pais}"
        params = {"lastdays": dias}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None


def formatear_numero(n):
    if n is None:
        return "N/A"
    return f"{n:,}"


# ==========================================================
# CALLBACK
# ==========================================================
@callback(
    [
        Output("grafica-covid", "figure"),
        Output("total-casos", "children"),
        Output("casos-nuevos", "children"),
        Output("total-muertes", "children"),
        Output("total-recuperados", "children"),
        Output("info-actualizado-covid", "children"),
    ],
    [
        Input("btn-actualizar-covid", "n_clicks"),
        State("dropdown-pais", "value"),
        State("dropdown-dias-covid", "value"),
    ],
    prevent_initial_call=False,
)
def actualizar_dashboard_covid(n_clicks, pais, dias):
    datos_actuales = obtener_datos_pais(pais)
    historico = obtener_historico_pais(pais, dias)

    if not datos_actuales or not historico:
        fig = go.Figure()
        fig.update_layout(
            title="⚠️ Error de conexión con la API",
            paper_bgcolor="rgb(40,40,40)",
            plot_bgcolor="rgb(50,48,47)",
            font=dict(color="rgb(213,196,161)", size=14),
        )
        return fig, "-", "-", "-", "-", "❌ Error al actualizar datos"

    # Extraer valores actuales
    total_casos = formatear_numero(datos_actuales.get("cases"))
    casos_hoy = "+" + formatear_numero(datos_actuales.get("todayCases"))
    total_muertes = formatear_numero(datos_actuales.get("deaths"))
    total_recuperados = formatear_numero(datos_actuales.get("recovered"))

    # Histórico
    timeline = historico.get("timeline", {})
    casos_hist = timeline.get("cases", {})
    muertes_hist = timeline.get("deaths", {})

    fechas = list(casos_hist.keys())
    fechas_dt = [datetime.strptime(f, "%m/%d/%y") for f in fechas]

    casos_val = list(casos_hist.values())
    muertes_val = list(muertes_hist.values())

    # ================
    # Gráfica estilo GRUVBOX
    # ================
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=fechas_dt,
            y=casos_val,
            mode="lines",
            name="Casos",
            line=dict(color="rgb(250,189,47)", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(250,189,47,0.15)",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=fechas_dt,
            y=muertes_val,
            mode="lines",
            name="Muertes",
            line=dict(color="rgb(204,36,29)", width=2),
        )
    )

    fig.update_layout(
        title=dict(
            text=f"<b>Evolución COVID-19 en {pais}</b>",
            x=0.5,
            font=dict(size=20, color="rgb(250,189,47)"),
        ),
        xaxis_title="Fecha",
        yaxis_title="Casos Totales",
        plot_bgcolor="rgb(50,48,47)",
        paper_bgcolor="rgb(40,40,40)",
        font=dict(family="Outfit", size=12, color="rgb(213,196,161)"),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgb(80,73,69)",
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgb(80,73,69)",
    )

    # Mensaje
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    msg = f"✅ Datos COVID actualizados: {ahora}"

    return fig, total_casos, casos_hoy, total_muertes, total_recuperados, msg
