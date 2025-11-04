import dash
from dash import html, dcc, Input, Output, callback
import numpy as np
import plotly.graph_objects as go

# ==================================================
# Registro de página
# ==================================================
dash.register_page(__name__, path='/pagina5', name='Modelo SEIR')

# ==================================================
# Layout — Modelo SEIR
# ==================================================
layout = html.Div([
    # ------------------------- IZQUIERDA -------------------------
    html.Div([
        html.H2("Modelo SEIR – Epidemiología", className="title"),

        html.Br(),

        html.Label("Población Total (N):"),
        dcc.Input(id="input-N-seir", type="number", value=1000, className="input-field"),

        html.Label("Tasa de transmisión (β):"),
        dcc.Input(id="input-beta-seir", type="number", value=0.3, className="input-field"),

        html.Label("Tasa de incubación (σ):"),
        dcc.Input(id="input-sigma-seir", type="number", value=0.2, className="input-field"),

        html.Label("Tasa de recuperación (γ):"),
        dcc.Input(id="input-gamma-seir", type="number", value=0.1, className="input-field"),

        html.Label("Expuestos iniciales (E₀):"),
        dcc.Input(id="input-E0-seir", type="number", value=0, className="input-field"),

        html.Label("Infectados iniciales (I₀):"),
        dcc.Input(id="input-I0-seir", type="number", value=1, className="input-field"),

        html.Label("Tiempo de simulación (días):"),
        dcc.Input(id="input-tmax-seir", type="number", value=160, className="input-field"),

        html.Br(),
        html.Button("Reiniciar Valores Ejemplo", id="btn-reiniciar-seir", className="btn-generar"),

        dcc.Interval(id='intervalo-seir', interval=200, n_intervals=0, disabled=True),
        html.Br(), html.Br()
    ], className="content left"),

    # ------------------------- DERECHA -------------------------
    html.Div([
        html.H2("Evolución de la Epidemia (Modelo SEIR)", className="title"),
        dcc.Graph(id='grafica-seir', style={'height': '400px', 'width': '100%'}),
        html.Div(id="interpretacion-seir", className="markdown-text", style={
            "marginTop": "25px",
            "fontSize": "15px",
            "textAlign": "justify",
            "color": "rgb(213,196,161)",
            "lineHeight": "1.6",
        })
    ], className="content right")

], className="page-container page5-container")


# ==================================================
# Callback — Actualización automática del gráfico e interpretación
# ==================================================
@callback(
    Output('grafica-seir', 'figure'),
    Output('interpretacion-seir', 'children'),
    Input('input-N-seir', 'value'),
    Input('input-beta-seir', 'value'),
    Input('input-sigma-seir', 'value'),
    Input('input-gamma-seir', 'value'),
    Input('input-E0-seir', 'value'),
    Input('input-I0-seir', 'value'),
    Input('input-tmax-seir', 'value')
)
def actualizar_en_tiempo_real(N, beta, sigma, gamma, E0, I0, tmax):
    """Simula el modelo SEIR y genera la gráfica e interpretación."""
    N = float(N or 1000)
    beta = float(beta or 0.3)
    sigma = float(sigma or 0.2)
    gamma = float(gamma or 0.1)
    E0 = float(E0 or 0)
    I0 = float(I0 or 1)
    tmax = int(tmax or 160)

    S0 = N - E0 - I0
    R0 = 0

    t = np.linspace(0, tmax, tmax)
    S, E, I, R = np.zeros(tmax), np.zeros(tmax), np.zeros(tmax), np.zeros(tmax)
    S[0], E[0], I[0], R[0] = S0, E0, I0, R0

    for k in range(1, tmax):
        dS = -beta * S[k-1] * I[k-1] / N
        dE = beta * S[k-1] * I[k-1] / N - sigma * E[k-1]
        dI = sigma * E[k-1] - gamma * I[k-1]
        dR = gamma * I[k-1]
        S[k] = S[k-1] + dS
        E[k] = E[k-1] + dE
        I[k] = I[k-1] + dI
        R[k] = R[k-1] + dR

    # Crear figura
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)',
                             line=dict(color='rgb(69,133,136)', width=3)))
    fig.add_trace(go.Scatter(x=t, y=E, mode='lines', name='Expuestos (E)',
                             line=dict(color='rgb(142,192,124)', width=3)))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados (I)',
                             line=dict(color='rgb(251,73,52)', width=3)))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados (R)',
                             line=dict(color='rgb(184,187,38)', width=3)))

    fig.update_layout(
        title=dict(text="<b>Evolución del Modelo SEIR</b>", x=0.5, y=0.93,
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
    R0_num = beta / gamma

    interpretacion = html.Div([
        html.Span("Con los parámetros actuales, el número básico de reproducción es "),
        html.Span(f"R₀ ≈ {R0_num:.2f}", style={"fontWeight": "bold", "color": "rgb(250,189,47)"}),
        html.Span(". La cantidad de infectados alcanza su valor máximo de aproximadamente "),
        html.Span(f"{valor_max_I} personas", style={"fontWeight": "bold", "color": "rgb(251,73,52)"}),
        html.Span(" alrededor del día "),
        html.Span(f"{pico_I}", style={"fontWeight": "bold", "color": "rgb(184,187,38)"}),
        html.Span(". La presencia de la fase de exposición (E) retrasa el inicio del brote, produciendo un pico más suave y una propagación más lenta en comparación con el modelo SIR."),
    ])

    return fig, interpretacion


# ==================================================
# Callback — Botón de reinicio (restaura valores)
# ==================================================
@callback(
    Output('intervalo-seir', 'disabled'),
    Output('input-N-seir', 'value'),
    Output('input-beta-seir', 'value'),
    Output('input-sigma-seir', 'value'),
    Output('input-gamma-seir', 'value'),
    Output('input-E0-seir', 'value'),
    Output('input-I0-seir', 'value'),
    Output('input-tmax-seir', 'value'),
    Input('btn-reiniciar-seir', 'n_clicks'),
    prevent_initial_call=True
)
def reiniciar_simulacion(_):
    """Restaura los valores base del ejemplo."""
    return False, 1000, 0.3, 0.2, 0.1, 0, 1, 160
