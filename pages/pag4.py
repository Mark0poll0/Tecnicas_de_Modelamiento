import dash
from dash import html, dcc, Input, Output, callback
import numpy as np
import plotly.graph_objects as go

# ==================================================
# Registro de página
# ==================================================
dash.register_page(__name__, path='/pagina4', name='Modelo SIR')

# ==================================================
# Layout — Modelo SIR
# ==================================================
layout = html.Div([
    # ------------------------- IZQUIERDA -------------------------
    html.Div([
        html.H2("Modelo SIR – Epidemiología", className="title"),

        html.Br(),

        html.Label("Población Total (N):"),
        dcc.Input(id="input-N", type="number", value=1000, className="input-field"),

        html.Label("Tasa de transmisión (β):"),
        dcc.Input(id="input-beta", type="number", value=0.3, className="input-field"),

        html.Label("Tasa de recuperación (γ):"),
        dcc.Input(id="input-gamma", type="number", value=0.1, className="input-field"),

        html.Label("Infectados iniciales (I₀):"),
        dcc.Input(id="input-I0", type="number", value=1, className="input-field"),

        html.Label("Tiempo de simulación (días):"),
        dcc.Input(id="input-tmax", type="number", value=100, className="input-field"),

        html.Br(),
        html.Button("Reiniciar Grafica al Ejemplo", id="btn-reiniciar", className="btn-generar"),

        dcc.Interval(id='intervalo', interval=200, n_intervals=0, disabled=True),
        html.Br(), html.Br()
    ], className="content left"),

    # ------------------------- DERECHA -------------------------
    html.Div([
        html.H2("Evolución de la Epidemia", className="title"),
        dcc.Graph(id='grafica-sir', style={'height': '400px', 'width': '100%'}),
        html.Div(id="interpretacion", className="markdown-text", style={
            "marginTop": "25px",
            "fontSize": "15px",
            "textAlign": "justify",
            "color": "rgb(213,196,161)",
            "lineHeight": "1.6",
        })
    ], className="content right")

], className="page-container page4-container")


# ==================================================
# Callback — Actualización automática del gráfico e interpretación
# ==================================================
@callback(
    Output('grafica-sir', 'figure'),
    Output('interpretacion', 'children'),
    Input('input-N', 'value'),
    Input('input-beta', 'value'),
    Input('input-gamma', 'value'),
    Input('input-I0', 'value'),
    Input('input-tmax', 'value')
)
def actualizar_en_tiempo_real(N, beta, gamma, I0, tmax):
    """Simula el modelo SIR y genera la gráfica e interpretación."""
    N = float(N or 1000)
    beta = float(beta or 0.3)
    gamma = float(gamma or 0.1)
    I0 = float(I0 or 1)
    tmax = int(tmax or 100)

    S0, I0, R0 = N - I0, I0, 0
    t = np.linspace(0, tmax, tmax)
    S, I, R = np.zeros(tmax), np.zeros(tmax), np.zeros(tmax)
    S[0], I[0], R[0] = S0, I0, R0

    for k in range(1, tmax):
        dS = -beta * S[k-1] * I[k-1] / N
        dI = beta * S[k-1] * I[k-1] / N - gamma * I[k-1]
        dR = gamma * I[k-1]
        S[k] = S[k-1] + dS
        I[k] = I[k-1] + dI
        R[k] = R[k-1] + dR

    # Crear figura
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)',
                             line=dict(color='rgb(69,133,136)', width=3)))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados (I)',
                             line=dict(color='rgb(251,73,52)', width=3)))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados (R)',
                             line=dict(color='rgb(184,187,38)', width=3)))

    fig.update_layout(
        title=dict(text="<b>Evolución del Modelo SIR</b>", x=0.5, y=0.93,
                   font=dict(size=20, color='rgb(250,189,47)')),
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
        plot_bgcolor='rgb(50,48,47)',
        paper_bgcolor='rgb(40,40,40)',
        font=dict(family='Outfit', size=12, color='rgb(213,196,161)'),
        margin=dict(l=40, r=40, t=90, b=40),
        legend=dict(orientation='h', yanchor='bottom', y=1.1,
                    xanchor='center', x=0.5, bgcolor='rgba(0,0,0,0)')
    )
    fig.update_xaxes(showgrid=True, gridcolor='rgb(80,73,69)',
                     linecolor='rgb(102,92,84)', mirror=True)
    fig.update_yaxes(showgrid=True, gridcolor='rgb(80,73,69)',
                     linecolor='rgb(102,92,84)', mirror=True)

    # Datos interpretativos dinámicos
    pico_I = int(np.argmax(I))
    valor_max_I = int(max(I))
    R0 = beta / gamma

    # Texto con formato (valores resaltados)
    interpretacion = html.Div([
        html.Span("Con los parámetros actuales, el número básico de reproducción es "),
        html.Span(f"R₀ ≈ {R0:.2f}", style={"fontWeight": "bold", "color": "rgb(250,189,47)"}),
        html.Span(". La cantidad de infectados alcanza su valor máximo de aproximadamente "),
        html.Span(f"{valor_max_I} personas", style={"fontWeight": "bold", "color": "rgb(251,73,52)"}),
        html.Span(" alrededor del día "),
        html.Span(f"{pico_I}", style={"fontWeight": "bold", "color": "rgb(184,187,38)"}),
        html.Span(". A medida que los recuperados aumentan, los susceptibles disminuyen, mostrando el ciclo de expansión y estabilización del brote epidémico."),
    ])

    return fig, interpretacion


# ==================================================
# Callback — Botón de reinicio (restaura valores)
# ==================================================
@callback(
    Output('intervalo', 'disabled'),
    Output('input-N', 'value'),
    Output('input-beta', 'value'),
    Output('input-gamma', 'value'),
    Output('input-I0', 'value'),
    Output('input-tmax', 'value'),
    Input('btn-reiniciar', 'n_clicks'),
    prevent_initial_call=True
)
def reiniciar_simulacion(_):
    """Restaura los valores base del ejemplo."""
    return False, 1000, 0.3, 0.1, 1, 100
