import dash
from dash import html, dcc, Input, Output, callback
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

# ==================================================
# Registro de página
# ==================================================
dash.register_page(__name__, path="/Proyecto2.1", name="PROYECTO 2.1")


# ==================================================
# Layout
# ==================================================
layout = html.Div([
    # ------------------------- IZQUIERDA -------------------------
    html.Div([
        html.H2("Modelo SIR Modificado – Rumor", className="title"),

        html.Label("Población total (N):"),
        dcc.Input(id="sirN", type="number", value=275, className="input-field"),

        html.Label("Tasa de transmisión del rumor (b):"),
        dcc.Input(id="sirB", type="number", value=0.004, step=0.0001, className="input-field"),

        html.Label("Constante de racionalización (k):"),
        dcc.Input(id="sirK", type="number", value=0.01, step=0.0001, className="input-field"),

        html.Label("Ignorantes iniciales S₀:"),
        dcc.Input(id="sirS0", type="number", value=266, className="input-field"),

        html.Label("Divulgadores iniciales I₀:"),
        dcc.Input(id="sirI0", type="number", value=1, className="input-field"),

        html.Label("Racionales iniciales R₀:"),
        dcc.Input(id="sirR0", type="number", value=8, className="input-field"),

        html.Label("Duración de la simulación (días):"),
        dcc.Input(id="sirTmax", type="number", value=15, className="input-field"),

        html.Br(),
        html.Button("Reiniciar valores", id="btnResetSir6", className="btn-generar"),

        html.Br(), html.Br(),

        html.Div(
            "Se simula la propagación de un rumor con los valores iniciales observados en un grupo de 275 personas.",
            className="text-explain"
        )
    ], className="content left"),

    # ------------------------- DERECHA -------------------------
    html.Div([
        html.H2("Evolución del rumor", className="title"),
        dcc.Graph(id='graficaSIR6', style={'height': '420px', 'width': '100%'}),
        html.Div(id="interpretacionSIR6", className="markdown-text", style={
            "marginTop": "25px",
            "fontSize": "15px",
            "textAlign": "justify",
            "color": "rgb(213,196,161)",
            "lineHeight": "1.6",
        })
    ], className="content right")

], className="page-container page6-container")


# ==================================================
# Callback — Actualización del gráfico e interpretación
# ==================================================
@callback(
    Output('graficaSIR6', 'figure'),
    Output('interpretacionSIR6', 'children'),
    Input('sirN', 'value'),
    Input('sirB', 'value'),
    Input('sirK', 'value'),
    Input('sirS0', 'value'),
    Input('sirI0', 'value'),
    Input('sirR0', 'value'),
    Input('sirTmax', 'value')
)
def actualizar_sir_modificado(N, b, k, S0, I0, R0, tmax):

    N = float(N or 275)
    b = float(b or 0.004)
    k = float(k or 0.01)
    S0 = float(S0 or 266)
    I0 = float(I0 or 1)
    R0 = float(R0 or 8)
    tmax = int(tmax or 15)

    # Modelo SIR del rumor
    def sir_rumor(y, t, b, k):
        S, I, R = y
        dSdt = -b * S * I
        dIdt = b * S * I - k * I
        dRdt = k * I
        return [dSdt, dIdt, dRdt]

    t = np.linspace(0, tmax, 500)
    sol = odeint(sir_rumor, (S0, I0, R0), t, args=(b, k))
    S, I, R = sol.T

    # Pico del rumor
    pico_idx = np.argmax(I)
    dia_pico = t[pico_idx]
    maxI = I[pico_idx]

    # ==================================================
    # GRÁFICA — Misma paleta que Página 4
    # ==================================================
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines', name='Ignorantes (S)',
        line=dict(color='rgb(69,133,136)', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines', name='Divulgadores (I)',
        line=dict(color='rgb(251,73,52)', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines', name='Racionales (R)',
        line=dict(color='rgb(184,187,38)', width=3)
    ))

    # Línea del pico
    fig.add_vline(
        x=dia_pico,
        line=dict(color='rgb(250,189,47)', width=2, dash='dot'),
        annotation_text=f"Pico del rumor (día {dia_pico:.1f})",
        annotation_position="top right",
        annotation_font=dict(color='rgb(250,189,47)', size=12)
    )

    fig.update_layout(
        title=dict(
            text="<b>Modelo SIR – Difusión del rumor</b>",
            x=0.5, y=0.9,
            font=dict(size=20, color='rgb(250,189,47)')
        ),
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',

        plot_bgcolor='rgb(50,48,47)',
        paper_bgcolor='rgb(40,40,40)',

        font=dict(family='Outfit', size=12, color='rgb(213,196,161)'),
        margin=dict(l=40, r=40, t=90, b=60),

        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02,
            xanchor='center', x=0.5,
            bgcolor='rgba(0,0,0,0)'
        )
    )

    fig.update_xaxes(
        showgrid=True, gridcolor='rgb(80,73,69)',
        linecolor='rgb(102,92,84)', mirror=True
    )
    fig.update_yaxes(
        showgrid=True, gridcolor='rgb(80,73,69)',
        linecolor='rgb(102,92,84)', mirror=True
    )

    # ==================================================
    # Interpretación
    # ==================================================
    interpretacion = html.Div([
        html.Span(f"Se simula un grupo de {int(N)} personas, con {int(S0)} ignorantes, {int(I0)} divulgadores y {int(R0)} racionales iniciales. "),
        html.Span(f"La tasa de transmisión del rumor es b = {b} y la constante de racionalización k = {k}. "),
        html.Span(f"El máximo número de divulgadores se alcanza alrededor del día {dia_pico:.1f} con aproximadamente {int(maxI)} personas. "),
        html.Span("Posteriormente, la cantidad de racionales aumenta a medida que el rumor pierde interés.")
    ])

    return fig, interpretacion


# ==================================================
# Callback — Reinicio
# ==================================================
@callback(
    Output('sirN', 'value'),
    Output('sirB', 'value'),
    Output('sirK', 'value'),
    Output('sirS0', 'value'),
    Output('sirI0', 'value'),
    Output('sirR0', 'value'),
    Output('sirTmax', 'value'),
    Input('btnResetSir6', 'n_clicks'),
    prevent_initial_call=True
)
def reiniciar_valores(_):
    return 275, 0.004, 0.01, 266, 1, 8, 15
