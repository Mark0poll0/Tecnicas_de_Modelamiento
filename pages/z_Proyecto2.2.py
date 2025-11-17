import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/Proyecto2.2", name="PROYECTO 2.2")


# =====================================================
# LAYOUT
# =====================================================

layout = html.Div(
    [
        html.Div(
            [

                # ========================= COLUMNA IZQUIERDA =========================
                html.Div(
                    [
                        html.H2("PARÁMETROS", className="card-title", style={"textAlign": "left"}),

                        html.Label("Ignorantes Iniciales (S₀):", className="small"),
                        dcc.Input(id="sir-s0-p22", type="number", value=266, min=0, className="input-text"),

                        html.Label("Divulgadores Iniciales (I₀):", className="small"),
                        dcc.Input(id="sir-i0-p22", type="number", value=1, min=1, className="input-text"),

                        html.Label("Racionales Iniciales (R₀):", className="small"),
                        dcc.Input(id="sir-r0-p22", type="number", value=1, min=0, className="input-text"),

                        html.Label("Tasa de divulgación (β):", className="small"),
                        dcc.Input(id="sir-beta-p22", type="number", value=0.004, step=0.001, className="input-text"),

                        html.Label("Tasa de le da lo mismo (γ):", className="small"),
                        dcc.Input(id="sir-gamma-p22", type="number", value=0.02, step=0.01, className="input-text"),

                        html.Label("Tiempo máximo (tₘₐₓ):", className="small"),
                        dcc.Input(id="sir-tmax-p22", type="number", value=15, min=1, step=1, className="input-text"),

                        html.Div(id="sir-result-p22", className="text-output"),
                    ],
                    className="card card-body",
                    style={
                        "width": "310px",
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "12px",
                        "padding": "30px",
                        "flexShrink": "0",    # evita colapsar
                    },
                ),

                # ========================= COLUMNA DERECHA =========================
                html.Div(
                    [
                        html.H3(
                            "Dinámica del Modelo SIR",
                            className="card-title",
                            style={"textAlign": "center"}
                        ),

                        dcc.Graph(
                            id="sir-graph-p22",
                            style={
                                "height": "550px",
                                "width": "100%",
                                "minWidth": "750px",    # <= ANCHO MÍNIMO REAL
                            },
                            config={"responsive": True},
                        ),
                    ],
                    className="card card-body right-panel",
                    style={
                        "flex": "1",
                        "padding": "30px",
                        "minWidth": "780px",        # <= EXPANDE ANCHO
                    },
                ),

            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "gap": "40px",        # separación entre columnas
                "justifyContent": "flex-start",
                "width": "100%",      # ocupa todo el ancho disponible
            },
        )
    ],
    className="proyecto2-2-container",
)



# =====================================================
# CALLBACK SIR
# =====================================================

@callback(
    Output("sir-graph-p22", "figure"),
    Output("sir-result-p22", "children"),
    Input("sir-s0-p22", "value"),
    Input("sir-i0-p22", "value"),
    Input("sir-r0-p22", "value"),
    Input("sir-beta-p22", "value"),
    Input("sir-gamma-p22", "value"),
    Input("sir-tmax-p22", "value")
)
def update_sir(s0, i0, r0, beta, gamma, tmax):

    if None in (s0, i0, r0, beta, gamma, tmax):
        return dash.no_update, ""

    N = s0 + i0 + r0

    # =====================================================
    # SISTEMA DIFERENCIAL SIR
    # =====================================================
    def sir_eq(y, t):
        S, I, R = y
        dSdt = -beta * S * I
        dIdt = beta * S * I - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    t = np.linspace(0, tmax, 300)
    sol = odeint(sir_eq, (s0, i0, r0), t)
    S, I, R = sol.T

    # =====================================================
    # GRÁFICA
    # =====================================================
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, name="Ignorante", line=dict(color="#4a66ff", width=3)))
    fig.add_trace(go.Scatter(x=t, y=I, name="Divulgadores", line=dict(color="#ff533d", width=3)))
    fig.add_trace(go.Scatter(x=t, y=R, name="Racionales", line=dict(color="#38c172", width=3)))

    fig.update_layout(
        xaxis_title="Tiempo",
        yaxis_title="Población",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        margin=dict(l=40, r=40, t=40, b=40),
    )

    # =====================================================
    # RESULTADO DEL PICO
    # =====================================================
    peak = np.max(I)
    return fig, f"Pico máximo de infectados: {peak:.2f}"
