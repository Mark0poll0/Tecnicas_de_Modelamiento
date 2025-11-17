import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# ==================================================
# Registro de página
# ==================================================
dash.register_page(__name__, path="/pagina7", name="Pagina 7")

# ==================================================
# Layout
# ==================================================
layout = html.Div(
    [
        # ------------------------- IZQUIERDA -------------------------
        html.Div(
            [
                html.H2(
                    "Dashboard de Clima en Tiempo Real",
                    className="title",
                ),
                # --- Selector de ciudad ---
                html.Div(
                    [
                        html.Label("Selecciona una ciudad:"),
                        dcc.Dropdown(
                            id="dropdown-ciudad",
                            value="lima",
                            options=[
                                {"label": "🏛️ Lima, Perú", "value": "lima"},
                                {"label": "🗽 Nueva York, USA", "value": "nueva_york"},
                                {"label": "🌆 Madrid, España", "value": "madrid"},
                                {
                                    "label": "🌴 Ciudad de México",
                                    "value": "mexico",
                                },
                                {
                                    "label": "🏖️ Buenos Aires, Argentina",
                                    "value": "buenos_aires",
                                },
                                {"label": "🌃 São Paulo, Brasil", "value": "sao_paulo"},
                                {"label": "🗼 París, Francia", "value": "paris"},
                                {"label": "🏰 Londres, Inglaterra", "value": "londres"},
                                {"label": "🎌 Tokio, Japón", "value": "tokio"},
                                {"label": "🕌 Dubái, EAU", "value": "dubai"},
                            ],
                            className="dropdown-clima",
                            style={"width": "100%"},
                        ),
                    ],
                    className="input-group",
                ),
                # --- Tipo de gráfica ---
                html.Div(
                    [
                        html.Label("Tipo de visualización:"),
                        dcc.RadioItems(
                            id="radio-tipo-grafica",
                            options=[
                                {"label": " Temperatura", "value": "temperatura"},
                                {"label": " Precipitación", "value": "precipitacion"},
                                {"label": " Viento", "value": "viento"},
                            ],
                            value="temperatura",
                            className="radio-gold",  # clase propia para CSS
                        ),
                    ],
                    className="input-group",
                ),
                # --- Botón ---
                html.Button(
                    "Actualizar Clima",
                    id="btn-actualizar-clima",
                    className="btn-generar",
                ),
                # --- Info de actualización ---
                html.Div(
                    id="info-actualizado-clima",
                    className="clima-info-box",
                ),
            ],
            className="content left",
        ),
        # ------------------------- DERECHA -------------------------
        html.Div(
            [
                html.H2("Pronóstico de 7 Días", className="title"),
                # --- Tarjetas de valores actuales ---
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "Temperatura",
                                    className="card-title temp",
                                ),
                                html.H3(
                                    id="temp-actual",
                                    className="card-value temp",
                                ),
                            ],
                            className="clima-card",
                        ),
                        html.Div(
                            [
                                html.H4(
                                    "Humedad",
                                    className="card-title humedad",
                                ),
                                html.H3(
                                    id="humedad-actual",
                                    className="card-value humedad",
                                ),
                            ],
                            className="clima-card",
                        ),
                        html.Div(
                            [
                                html.H4(
                                    "Viento",
                                    className="card-title viento",
                                ),
                                html.H3(
                                    id="viento-actual",
                                    className="card-value viento",
                                ),
                            ],
                            className="clima-card",
                        ),
                    ],
                    className="clima-card-container",
                ),
                # --- Gráfica ---
                dcc.Graph(
                    id="grafica-clima",
                    style={"height": "380px", "width": "100%"},
                ),
            ],
            className="content right",
        ),
    ],
    className="page-container page8-container",
)

# ==========================================
# COORDENADAS DE LAS CIUDADES
# ==========================================

CIUDADES = {
    "lima": {"lat": -12.0464, "lon": -77.0428, "nombre": "Lima"},
    "nueva_york": {"lat": 40.7128, "lon": -74.0060, "nombre": "Nueva York"},
    "madrid": {"lat": 40.4168, "lon": -3.7038, "nombre": "Madrid"},
    "mexico": {"lat": 19.4326, "lon": -99.1332, "nombre": "Ciudad de México"},
    "buenos_aires": {"lat": -34.6037, "lon": -58.3816, "nombre": "Buenos Aires"},
    "sao_paulo": {"lat": -23.5505, "lon": -46.6333, "nombre": "São Paulo"},
    "paris": {"lat": 48.8566, "lon": 2.3522, "nombre": "París"},
    "londres": {"lat": 51.5074, "lon": -0.1278, "nombre": "Londres"},
    "tokio": {"lat": 35.6762, "lon": 139.6503, "nombre": "Tokio"},
    "dubai": {"lat": 25.2048, "lon": 55.2708, "nombre": "Dubái"},
}


# ==========================================
# FUNCIONES PARA CONECTAR CON LA API
# ==========================================


def obtener_datos_clima(ciudad_key):
    """
    Intenta obtener datos del clima usando Open-Meteo.
    Si falla, devuelve None y el callback usará datos ficticios.
    """
    try:
        ciudad = CIUDADES[ciudad_key]
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": ciudad["lat"],
            "longitude": ciudad["lon"],
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto",
            "forecast_days": 7,
        }
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        # Si hay error de red / API, devolvemos None y no rompemos la app
        print(f"[CLIMA] Error al obtener datos reales: {e}")
        return None


# ==========================================
# CALLBACK PRINCIPAL
# ==========================================


@callback(
    Output("grafica-clima", "figure"),
    Output("temp-actual", "children"),
    Output("humedad-actual", "children"),
    Output("viento-actual", "children"),
    Output("info-actualizado-clima", "children"),
    Input("btn-actualizar-clima", "n_clicks"),
    State("dropdown-ciudad", "value"),
    State("radio-tipo-grafica", "value"),
)
def actualizar_dashboard_clima(n_clicks, ciudad_key, tipo_grafica):
    """
    Actualiza el dashboard con datos del clima.
    Si la API falla, usa datos sintéticos para que SIEMPRE haya gráfica.
    """

    nombre_ciudad = CIUDADES[ciudad_key]["nombre"]

    # ----------------------------------------------
    # 1. Intentamos usar datos REALES
    # ----------------------------------------------
    datos = obtener_datos_clima(ciudad_key)

    if datos:
        try:
            temp_actual = datos["hourly"]["temperature_2m"][0]
            humedad_actual = datos["hourly"]["relative_humidity_2m"][0]
            viento_actual = datos["hourly"]["wind_speed_10m"][0]

            fechas = datos["daily"]["time"]
            fechas_dt = [datetime.strptime(f, "%Y-%m-%d") for f in fechas]

            temp_max = datos["daily"]["temperature_2m_max"]
            temp_min = datos["daily"]["temperature_2m_min"]
            precipitacion = datos["daily"]["precipitation_sum"]
            viento_max = datos["daily"]["wind_speed_10m_max"]

        except Exception as e:
            print(f"[CLIMA] Error al procesar datos reales: {e}")
            datos = None  # forzar uso de fallback

    # ----------------------------------------------
    # 2. Fallback: datos SINTÉTICOS
    # ----------------------------------------------
    if not datos:
        hoy = datetime.now().date()
        fechas_dt = [datetime.combine(hoy + timedelta(days=i), datetime.min.time()) for i in range(7)]

        # Patrones simples distintos por ciudad, solo para variar un poco
        base = 20 + (abs(hash(ciudad_key)) % 7)  # base de temperatura por ciudad
        temp_max = [base + 2 + i * 0.5 for i in range(7)]
        temp_min = [t - 5 for t in temp_max]
        precipitacion = [max(0, 8 * abs(__import__("math").sin(i))) for i in range(7)]
        viento_max = [8 + 2 * i for i in range(7)]

        temp_actual = temp_max[0]
        humedad_actual = 65.0
        viento_actual = viento_max[0]

    # textos para tarjetas
    temp_texto = f"{temp_actual:.1f}°C"
    humedad_texto = f"{humedad_actual:.0f}%"
    viento_texto = f"{viento_actual:.1f} km/h"

    # ----------------------------------------------
    # 3. Construimos la figura según tipo seleccionado
    # ----------------------------------------------
    # ===========================================
    # FIGURA BASE — TEMA GRUVBOX APLICADO SIEMPRE
    # ===========================================
    fig = go.Figure()

    fig.update_layout(
        plot_bgcolor='rgb(50,48,47)',     # fondo interno
        paper_bgcolor='rgb(40,40,40)',    # fondo general
        font=dict(
            family='Outfit',
            size=12,
            color='rgb(213,196,161)'
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgb(80,73,69)',
            linecolor='rgb(102,92,84)',
            zerolinecolor='rgb(102,92,84)',
            mirror=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(80,73,69)',
            linecolor='rgb(102,92,84)',
            zerolinecolor='rgb(102,92,84)',
            mirror=True
        )
    )


    if tipo_grafica == "temperatura":
        fig.add_trace(
            go.Scatter(
                x=fechas_dt,
                y=temp_max,
                mode="lines+markers",
                name="Temp. Máxima",
                line=dict(color="#ffb74d", width=2.5),
                marker=dict(size=8),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=fechas_dt,
                y=temp_min,
                mode="lines+markers",
                name="Temp. Mínima",
                line=dict(color="#4fc3f7", width=2.5),
                marker=dict(size=8),
            )
        )
        titulo = f"<b>Temperatura en {nombre_ciudad} - Próximos 7 días</b>"
        yaxis_title = "Temperatura (°C)"

    elif tipo_grafica == "precipitacion":
        fig.add_trace(
            go.Bar(
                x=fechas_dt,
                y=precipitacion,
                name="Precipitación",
                marker_color="#4fc3f7",
            )
        )
        titulo = f"<b>Precipitación en {nombre_ciudad} - Próximos 7 días</b>"
        yaxis_title = "Precipitación (mm)"

    else:  # viento
        fig.add_trace(
            go.Scatter(
                x=fechas_dt,
                y=viento_max,
                mode="lines+markers",
                name="Velocidad del viento",
                line=dict(color="#4db6ac", width=2.5),
                marker=dict(size=8),
                fill="tozeroy",
                fillcolor="rgba(77,182,172,0.18)",
            )
        )
        titulo = f"<b>Viento en {nombre_ciudad} - Próximos 7 días</b>"
        yaxis_title = "Velocidad (km/h)"

    # ===============================================================
    # ESTILO GRUBOX — EXACTO AL DE PÁGINA 7
    # ===============================================================
    fig.update_layout(
        title=dict(
            text=titulo,
            x=0.5,
            font=dict(size=20, color='rgb(250,189,47)')  # dorado Gruvbox
        ),
        xaxis_title="Fecha",
        yaxis_title=yaxis_title,

        plot_bgcolor='rgb(50,48,47)',   # fondo interno
        paper_bgcolor='rgb(40,40,40)',  # fondo total

        font=dict(
            family='Outfit',
            size=12,
            color='rgb(213,196,161)'     # beige Gruvbox
        ),

        hovermode="x unified",

        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(0,0,0,0)'      # transparente
        ),

        margin=dict(l=40, r=40, t=60, b=40)
    )

    # GRID Y EJES AL ESTILO GRUBOX
    fig.update_xaxes(
        showgrid=True,
        gridcolor='rgb(80,73,69)',      # grid marrón suave
        linecolor='rgb(102,92,84)',     # eje Gruvbox
        zerolinecolor='rgb(102,92,84)',
        mirror=True
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgb(80,73,69)',
        linecolor='rgb(102,92,84)',
        zerolinecolor='rgb(102,92,84)',
        mirror=True
    )

    # ----------------------------------------------
    # 5. Mensaje de actualización
    # ----------------------------------------------
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensaje = f"✅ Clima actualizado: {ahora} — {nombre_ciudad}"

    return fig, temp_texto, humedad_texto, viento_texto, mensaje
