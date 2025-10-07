import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/pagina1', name='Página 1')

#############################################

P0 = 100   # Población inicial
r = 0.03   # Tasa de crecimiento
t = np.linspace(0, 100, 10)
P = P0 * np.exp(r * t)

trace = go.Scatter(
    x=t,
    y=P,
    mode='lines+markers',
    line=dict(dash='dot', color='rgb(235, 219, 178)', width=2),
    marker=dict(color='rgb(180, 205, 186)', symbol='square', size=8),
    name='P(t) = P0 * e^(rt)',
    hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
)

fig = go.Figure(data=trace)

fig.update_layout(
    title=dict(
        text='<b>Crecimiento de la población</b>',
        font=dict(size=20, color='rgb(250, 189, 47)'),
        x=0.5, y=0.93
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=50, b=40),
    paper_bgcolor='rgb(40, 40, 40)',
    plot_bgcolor='rgb(50, 48, 47)',
    font=dict(family='Outfit', size=12, color='rgb(213, 196, 161)')
)

fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='rgb(80, 73, 69)',
    zeroline=True, zerolinewidth=2, zerolinecolor='rgb(184, 187, 38)',
    showline=True, linecolor='rgb(102, 92, 84)', linewidth=2, mirror=True
)
fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='rgb(80, 73, 69)',
    zeroline=True, zerolinewidth=2, zerolinecolor='rgb(184, 187, 38)',
    showline=True, linecolor='rgb(102, 92, 84)', linewidth=2, mirror=True
)

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Crecimiento de la población y capacidad de carga", className="title"),
        dcc.Markdown(r"""
        Para modelar el crecimiento de la población mediante una ecuación diferencial, primero 
        tenemos que introducir algunas variables y términos relevantes. La variable $t$ 
        representará el tiempo. Las unidades de tiempo pueden ser horas, días, semanas, 
        meses o incluso años. Cualquier problema dado debe especificar las unidades utilizadas 
        en ese problema en particular. La variable $P$ representará a la población. 
        Como la población varía con el tiempo, se entiende que es una función del tiempo. 
        Por lo tanto, utilizamos la notación $P(t)$ para la población en función del tiempo. 

        Si $P(t)$ es una función diferenciable, entonces la primera derivada 
        $\frac{dP}{dt}$ representa la tasa instantánea de cambio de la población 
        en función del tiempo.
        """, mathjax=True),
                dcc.Markdown(r"""
        Un ejemplo de función de crecimiento exponencial es 
        $P(t) = P_0 e^{rt}$.

        En esta función, $P(t)$ representa la población en el momento $t$, 
        $P_0$ representa la población inicial (población en el tiempo $t = 0$), 
        y la constante $r > 0$ se denomina tasa de crecimiento. 

        Aquí $P_0 = 100$ y $r = 0.03$.
""", mathjax=True),
    ], className="content left"),

    html.Div(children=[
        html.H2("Gráfica", className="title"),
        dcc.Graph(figure=fig, style={'height': '350px', 'width': '100%'}),
    ], className="content right")
], className="page-container")
