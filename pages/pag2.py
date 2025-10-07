# pages/pagina2.py
import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

# Página 2
dash.register_page(__name__, path="/pagina2", name="Página 2")
# ===========================================
# Crecimiento logístico y capacidad de carga (solo 2 curvas)
# ===========================================


P0 = 900_000
r  = 0.2311
K  = 1_072_764

# Rango temporal igual que en la referencia
t = np.linspace(-15, 15, 12)

# Ecuación logística
A = (K - P0) / P0
P_log = K / (1 + A * np.exp(-r * t))

# --- Curva logística (azul con nodos más oscuros) ---
trace_log = go.Scatter(
    x=t, y=P_log,
    mode='lines+markers',
    line=dict(color='rgb(80,160,255)', width=3),
    marker=dict(color='rgb(50,120,220)', symbol='square', size=8),
    name='Crecimiento logístico'
)

# --- Línea de capacidad de carga K (naranja punteada y gruesa) ---
trace_K = go.Scatter(
    x=[t.min(), t.max()],
    y=[K, K],
    mode='lines',
    line=dict(color='rgb(250,189,47)', width=3.5, dash='dot'),
    name='Capacidad de carga K'
)

# Figura
fig = go.Figure(data=[trace_log, trace_K])

# --- Layout general ---
fig.update_layout(
    title=dict(
        text='<b>Crecimiento logístico y capacidad de carga</b>',
        font=dict(size=20, color='rgb(250,189,47)'),
        x=0.5
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=50, b=40),
    paper_bgcolor='rgb(40,40,40)',
    plot_bgcolor='rgb(50,48,47)',
    font=dict(family='Outfit', size=12, color='rgb(213,196,161)'),
    legend=dict(bgcolor='rgba(0,0,0,0)')
)

# --- Ejes (verde-limón) ---
fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='rgb(80,73,69)',
    zeroline=True, zerolinewidth=2, zerolinecolor='rgb(184,187,38)',
    showline=True, linecolor='rgb(102,92,84)', linewidth=2, mirror=True,
    range=[-15, 15]
)
fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='rgb(80,73,69)',
    zeroline=True, zerolinewidth=2, zerolinecolor='rgb(184,187,38)',
    showline=True, linecolor='rgb(102,92,84)', linewidth=2, mirror=True,
    range=[-200_000, 1_500_000],
    tickformat=',.0f'
)

# --- Anotaciones ---
fig.add_annotation(
    x=0, y=P0,
    text='P₀ = 900,000',
    showarrow=True, arrowhead=2, ax=40, ay=-30,
    font=dict(color='rgb(80,160,255)', size=12),
    bgcolor='rgba(50,48,47,0.5)'
)

fig.add_annotation(
    x=8, y=K,
    text='P = 1,072,764',
    showarrow=False,
    font=dict(color='rgb(250,189,47)', size=13),
    bgcolor='rgba(50,48,47,0.5)',
    yshift=-18
)

# --- Flechas de ejes ---
fig.add_shape(type="line", x0=-15, x1=15.5, y0=0, y1=0,
              line=dict(color='rgb(184,187,38)', width=2))
fig.add_shape(type="line", x0=0, x1=0, y0=-200_000, y1=1_500_000,
              line=dict(color='rgb(184,187,38)', width=2))




layout = html.Div(children=[
    html.Div(children=[
        html.H2("Crecimiento logístico y capacidad de carga", className="title"),
        dcc.Markdown(r"""
        El **modelo logístico** describe el crecimiento de una población $P(t)$ que se ralentiza al aproximarse
        a la **capacidad de carga** $K$ del entorno. La dinámica viene dada por la ecuación diferencial

        $$
        \frac{dP}{dt} = r\,P\left(1 - \frac{P}{K}\right),
        $$

        donde $r>0$ es la **tasa intrínseca** de crecimiento y $K>0$ es el **límite ambiental**.
        Con la condición inicial $P(0)=P_0$, la solución cerrada es

        $$
        P(t) = \frac{K}{1 + A\,e^{-rt}}, \qquad A=\frac{K-P_0}{P_0}.
        $$

        Propiedades clave:
        - **Equilibrios:** $P^*=0$ (inestable) y $P^*=K$ (estable).
        - **Asíntota:** si $0<P_0<K$, entonces $P(t)<K$ para todo $t$ y $P(t)\to K$ cuando $t\to\infty$.
        - **Punto de inflexión:** ocurre en $P=K/2$, donde el crecimiento absoluto $\tfrac{dP}{dt}$ es máximo.
        """, mathjax=True),

        dcc.Markdown(r"""
        **Parámetros usados en la gráfica:**  
        - $P_0 = 900{,}000$  
        - $r = 0.2311$  
        - $K = 1{,}072{,}764$  

        **Detalles de visualización:**  
        - Rango temporal: $t \in [-15,\,15]$  
        - Rango vertical: $P \in [-200{,}000,\,1{,}500{,}000]$  
        - Se dibuja la **línea punteada** en $y=K$ para resaltar la capacidad de carga y se muestran **nodos** en la curva logística.
        """, mathjax=True),
    ], className="content left"),


    html.Div(children=[
        html.H2("Gráfica", className="title"),
        dcc.Graph(figure=fig, style={'height': '350px', 'width': '100%'}),
    ], className="content right")
], className="page-container")

