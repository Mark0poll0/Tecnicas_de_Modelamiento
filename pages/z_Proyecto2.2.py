import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path='/Proyecto2.2', name='Proyecto2.2')

def modelo_sir(y, t, beta, gamma, N):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

def generar_grafico_sir(S0, I0, R0, beta, gamma, t_max):
    N = S0 + I0 + R0
    t = np.linspace(0, t_max, 1000)
    y0 = [S0, I0, R0]
    solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, N))
    S, I, R = solucion.T
    
    R0_val = beta / gamma if gamma != 0 else float('inf')
    idx_pico = np.argmax(I)
    tiempo_pico = t[idx_pico]
    valor_pico = I[idx_pico]
    S_final = S[-1]
    R_final = R[-1]
    tasa_ataque_final = (R_final / N) * 100
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='green', width=2)))
    fig.add_vline(x=tiempo_pico, line_dash="dash", line_color="orange", annotation_text=f"Pico: día {tiempo_pico:.1f}")
    fig.add_trace(go.Scatter(x=[tiempo_pico], y=[valor_pico], mode='markers', marker=dict(size=10, color='orange'), name='Pico de infección', showlegend=True))
    
    fig.update_layout(
        title=f'Modelo SIR - R₀ = {R0_val:.2f}',
        xaxis_title='Tiempo (días)',
        yaxis_title='Población',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=0.98, xanchor="right", x=1)
    )
    
    return fig, R0_val, tiempo_pico, valor_pico, S_final, R_final, tasa_ataque_final

layout = html.Div(children=[  
    html.Div(children=[
        html.Div(children=[  
            html.H2("Modelo SIR Interactivo", className="title"),  
            html.Div([
                html.H3("Población Inicial", className="subtitle"),
                html.Div([
                    html.Label("Población Total (N):", className="sir-input-label"),
                    dcc.Input(id="input-n-sir", type="number", value=100000, min=1, className="sir-input-field")
                ], className="sir-input-group"),
                html.Div([
                    html.Label("Susceptibles Iniciales (S₀):", className="sir-input-label"),
                    dcc.Input(id="input-s0-sir", type="number", value=99500, min=0, className="sir-input-field")
                ], className="sir-input-group"),
                html.Div([
                    html.Label("Infectados Iniciales (I₀):", className="sir-input-label"),
                    dcc.Input(id="input-i0-sir", type="number", value=500, min=0, className="sir-input-field")
                ], className="sir-input-group"),
                html.Div([
                    html.Label("Recuperados Iniciales (R₀):", className="sir-input-label"),
                    dcc.Input(id="input-r0-sir", type="number", value=0, min=0, className="sir-input-field")
                ], className="sir-input-group"),
            ], className="controls-container"),
            html.Div([
                html.H3("Parámetros Epidemiológicos", className="subtitle"),
                html.Div([
    html.Label("Tasa de Infección (β) [1/día]:", className="sir-input-label"),
    dcc.Input(
        id="input-beta-sir", 
        type="number", 
        value=0.1143, 
        step="any",  # ← Cambia esto
        min=0, 
        className="sir-input-field"
    ),
    ], className="sir-input-group"),

    html.Div([
        html.Label("Tasa de Recuperación (γ) [1/día]:", className="sir-input-label"),
        dcc.Input(
            id="input-gamma-sir", 
            type="number", 
            value=0.0286, 
            step="any",  # ← Cambia esto
            min=0, 
            className="sir-input-field"
        ),
    ], className="sir-input-group"),
                html.Div([
                    html.Label("Tiempo máximo (días):", className="sir-input-label"),
                    dcc.Input(id="input-t-max-sir", type="number", value=365, min=10, className="sir-input-field")
                ], className="sir-input-group"),
            ], className="controls-container"),
            html.Div([
                html.Div([
                    html.Div("Número Reproductivo Básico:", className="r0-label"),
                    html.Div(id="r0-value-display", className="r0-value")
                ], className="r0-display-panel"),
                html.Button("Generar simulación", id="btn-generar", className="btn-generar", n_clicks=0)
            ], className="controls-footer")
        ], className="left-container"),
        html.Div(children=[
            html.H2("Simulación del Modelo SIR", className="title"),
            html.Div([
                dcc.Graph(
                    id='grafico-sir-interactivo',
                    config={'displayModeBar': True},
                    style={'height': '500px', 'width': '100%'}
                )
            ], className="sir-graph-container"),
            html.Div([
                html.H3("Información de la Simulación"),
                html.Div(id="simulation-info", className="sir-info-panel")
            ])
        ], className="right-container")
    ], className="main-container")
])

@callback(
    Output('r0-value-display', 'children'),
    Input('input-beta-sir', 'value'),
    Input('input-gamma-sir', 'value')
)
def actualizar_r0(beta, gamma):
    if beta is not None and gamma is not None and gamma > 0:
        r0 = beta / gamma
        return f"R₀ = {r0:.2f}"
    return "R₀ = No definido"

@callback(
    [Output('input-s0-sir', 'value'),
     Output('input-i0-sir', 'value'),
     Output('input-r0-sir', 'value')],
    Input('input-n-sir', 'value'),
    [State('input-s0-sir', 'value'),
     State('input-i0-sir', 'value'),
     State('input-r0-sir', 'value')]
)
def actualizar_poblacion_total(N, S0, I0, R0):
    if N is not None and S0 is not None and I0 is not None and R0 is not None:
        total_actual = S0 + I0 + R0
        if total_actual != N:
            if total_actual > 0:
                factor = N / total_actual
                nuevo_S0 = int(S0 * factor)
                nuevo_I0 = int(I0 * factor)
                nuevo_R0 = N - nuevo_S0 - nuevo_I0
                return nuevo_S0, nuevo_I0, nuevo_R0
            else:
                return N, 0, 0
    return S0, I0, R0

@callback(
    [Output('grafico-sir-interactivo', 'figure'),
     Output('simulation-info', 'children')],
    Input('btn-generar', 'n_clicks'),
    [State('input-s0-sir', 'value'),
     State('input-i0-sir', 'value'),
     State('input-r0-sir', 'value'),
     State('input-beta-sir', 'value'),
     State('input-gamma-sir', 'value'),
     State('input-t-max-sir', 'value')]
)
def actualizar_grafica_sir(n_clicks, S0, I0, R0, beta, gamma, t_max):
    if None in [S0, I0, R0, beta, gamma, t_max]:
        fig = go.Figure()
        fig.update_layout(
            title="Error: Complete todos los campos",
            xaxis_title='Tiempo (días)',
            yaxis_title='Población',
            template='plotly_white',
            height=500
        )
        return fig, "Error: Todos los campos deben estar completos"
    
    if S0 + I0 + R0 <= 0:
        fig = go.Figure()
        fig.update_layout(
            title="Error: Población total debe ser mayor a 0",
            xaxis_title='Tiempo (días)',
            yaxis_title='Población',
            template='plotly_white',
            height=500
        )
        return fig, "Error: La población total debe ser mayor a 0"
    
    N = S0 + I0 + R0
    
    try:
        fig, R0_val, tiempo_pico, valor_pico, S_final, R_final, tasa_ataque_final = generar_grafico_sir(
            S0, I0, R0, beta, gamma, t_max
        )
        
        if R0_val > 1:
            comportamiento = "Epidemia en crecimiento (el juego se propagará)"
        elif R0_val < 1:
            comportamiento = "Epidemia en declive (el juego no se propagará)"
        else:
            comportamiento = "Estado estacionario"
        
        info_content = [
            html.Div([
                html.H4("Resumen de la Simulación", className="info-title"),
                html.Div([
                    html.P([html.Strong("Población total: "), f"{N:,} personas"]),
                    html.P([html.Strong("Número reproductivo básico: "), f"R₀ = {R0_val:.2f}"]),
                    html.P([html.Strong("Comportamiento: "), comportamiento]),
                    html.Hr(),
                    html.P([html.Strong("Pico de infección: "), f"{valor_pico:,.0f} jugadores activos"]),
                    html.P([html.Strong("Día del pico: "), f"día {tiempo_pico:.1f}"]),
                    html.Hr(),
                    html.P([html.Strong("Susceptibles finales: "), f"{S_final:,.0f} personas ({S_final/N*100:.1f}%)"]),
                    html.P([html.Strong("Recuperados finales: "), f"{R_final:,.0f} personas ({tasa_ataque_final:.1f}%)"]),
                    html.P([html.Strong("Inserción del juego: "), f"{(N - S_final)/N*100:.1f}% de la población"])
                ], className="info-details")
            ], className="simulation-summary")
        ]
        
        return fig, info_content
        
    except Exception as e:
        fig = go.Figure()
        fig.update_layout(
            title="Error en la simulación",
            xaxis_title='Tiempo (días)',
            yaxis_title='Población',
            template='plotly_white',
            height=500
        )
        return fig, f"Error: {str(e)}"