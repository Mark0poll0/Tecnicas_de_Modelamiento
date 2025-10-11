import dash
from dash import html, dcc, Input, Output, callback, no_update
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path='/pagina3', name='Página 3')

# ==================================================
# Helper para etiquetas con MathJax + valor dinámico
# ==================================================
def md_label(texto_md: str, for_id: str, value_span_id: str = None):
    children = [dcc.Markdown(texto_md, mathjax=True, className="label-md")]
    if value_span_id:
        children.append(html.Span(id=value_span_id, className="label-val"))
    return html.Label(children=children, htmlFor=for_id, className="form-label")


# ==================================================
# Layout — Modelo Exponencial
# ==================================================
layout = html.Div([
    html.Div([
        html.H2("Modelo Exponencial Interactivo", className="title"),

        dcc.Markdown(r"""
El **modelo exponencial** describe el crecimiento (o decaimiento) de una población \(P(t)\)
proporcional a su tamaño:

$$
\frac{dP}{dt} = r\,P, \qquad P(0)=P_0.
$$

La solución analítica es:

$$
P(t) = P_0\,e^{r t}.
$$

- Si \(r>0\): crecimiento.
- Si \(r<0\): decaimiento.
""", mathjax=True),

        # ------- P0 -------
        html.Div([
            md_label(r"Población inicial $P_0$:", "input-p0", value_span_id="val-p0"),
            dcc.Input(id="input-p0", type="number", value=200, debounce=True, className="input-field"),
            dcc.Slider(
                id="slider-p0",
                min=1, max=2_000_000, step=1_000, value=200,
                tooltip={"always_visible": False, "placement": "bottom"},
                className="dash-slider"
            ),
        ], className="input-group"),

        # ------- r -------
        html.Div([
            md_label(r"Tasa de crecimiento $r$:", "input-r", value_span_id="val-r"),
            dcc.Input(id="input-r", type="number", value=0.04, debounce=True, className="input-field"),
            dcc.Slider(
                id="slider-r",
                min=-0.5, max=0.5, step=0.001, value=0.04,
                tooltip={"always_visible": False, "placement": "bottom"},
                className="dash-slider"
            ),
        ], className="input-group"),

        # ------- t_max -------
        html.Div([
            md_label(r"Tiempo máximo $t_{\max}$:", "input-t", value_span_id="val-t"),
            dcc.Input(id="input-t", type="number", value=100, debounce=True, className="input-field"),
            dcc.Slider(
                id="slider-t",
                min=1, max=200, step=1, value=100,
                tooltip={"always_visible": False, "placement": "bottom"},
                className="dash-slider"
            ),
        ], className="input-group"),

        html.Button("Generar gráfica", id="btn-generar", className="btn-generar")
    ], className="content left"),

    html.Div([
        html.H2("Crecimiento exponencial", className="title"),
        dcc.Graph(id='grafica-poblacion', style={'height': '380px', 'width': '100%'})
    ], className="content right")
], className="page-container page3-container")


# ==================================================
# SINCRONIZACIÓN SIN CICLOS (un callback por pareja)
# ==================================================
@callback(
    Output('input-p0', 'value'), Output('slider-p0', 'value'),
    Input('input-p0', 'value'),  Input('slider-p0', 'value'),
    prevent_initial_call=True
)
def sync_p0(p0_in, p0_sl):
    from dash import callback_context as ctx
    trig = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if trig == 'input-p0':   # editaste el input → mueve el slider
        return no_update, p0_in
    if trig == 'slider-p0':  # moviste el slider → mueve el input
        return p0_sl, no_update
    return no_update, no_update

@callback(
    Output('input-r', 'value'), Output('slider-r', 'value'),
    Input('input-r', 'value'),  Input('slider-r', 'value'),
    prevent_initial_call=True
)
def sync_r(r_in, r_sl):
    from dash import callback_context as ctx
    trig = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if trig == 'input-r':
        return no_update, r_in
    if trig == 'slider-r':
        return r_sl, no_update
    return no_update, no_update

@callback(
    Output('input-t', 'value'), Output('slider-t', 'value'),
    Input('input-t', 'value'),  Input('slider-t', 'value'),
    prevent_initial_call=True
)
def sync_t(t_in, t_sl):
    from dash import callback_context as ctx
    trig = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    if trig == 'input-t':
        return no_update, t_in
    if trig == 'slider-t':
        return t_sl, no_update
    return no_update, no_update


# ==================================================
# Callback — gráfico (depende solo de los INPUTS)
# ==================================================
@callback(
    Output('grafica-poblacion', 'figure'),
    Input('input-p0', 'value'),
    Input('input-r',  'value'),
    Input('input-t',  'value'),
    Input('btn-generar', 'n_clicks'),
    prevent_initial_call=False
)
def actualizar_grafica(P0, r, t_max, _n):
    # Sanitización
    try: P0 = float(P0)
    except: P0 = 1.0
    try: r = float(r)
    except: r = 0.1
    try: t_max = float(t_max)
    except: t_max = 10.0
    if t_max <= 0: t_max = 1.0
    if P0 <= 0: P0 = 1e-6

    t = np.linspace(0, t_max, 15)
    P = P0 * np.exp(r * t)
    y_max = float(np.nanmax(P)) or 1.0
    if y_max <= 0: y_max = 1.0

    trace_exp = go.Scatter(
        x=t, y=P,
        mode='lines+markers',
        line=dict(dash='dot', color='rgb(235, 219, 178)', width=2),
        marker=dict(color='rgb(180, 205, 186)', symbol='square', size=8),
        name='P(t) = P₀·e^{rt}',
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )

    fig = go.Figure(data=[trace_exp])
    fig.update_layout(
        title=dict(
            text="<b>Evolución poblacional (Exponencial)</b>",
            font=dict(size=20, color='rgb(250, 189, 47)'),
            x=0.5, y=0.93
        ),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        margin=dict(l=40, r=40, t=90, b=40),
        paper_bgcolor='rgb(40, 40, 40)',
        plot_bgcolor='rgb(50, 48, 47)',
        font=dict(family='Outfit', size=12, color='rgb(213, 196, 161)'),
        legend=dict(orientation='h', yanchor='bottom', y=1.15,
                    xanchor='center', x=0.5, bgcolor='rgba(0,0,0,0)')
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgb(80, 73, 69)',
                     zeroline=True, zerolinewidth=2, zerolinecolor='rgb(184, 187, 38)',
                     showline=True, linecolor='rgb(102, 92, 84)', linewidth=2, mirror=True)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgb(80, 73, 69)',
                     zeroline=True, zerolinewidth=2, zerolinecolor='rgb(184, 187, 38)',
                     showline=True, linecolor='rgb(102, 92, 84)', linewidth=2, mirror=True,
                     range=[0, y_max * 1.12])

    fig.add_shape(type="line", x0=0, x1=t_max * 1.02, y0=0, y1=0,
                  line=dict(color='rgb(184, 187, 38)', width=2))
    fig.add_shape(type="line", x0=0, x1=0, y0=0, y1=y_max * 1.12,
                  line=dict(color='rgb(184, 187, 38)', width=2))

    fig.add_annotation(x=0, y=P0, text=f"P₀ = {P0:.2f}",
                       showarrow=True, arrowhead=2, ax=40, ay=-30,
                       font=dict(color='rgb(235, 219, 178)', size=12),
                       bgcolor='rgba(50, 48, 47, 0.5)')

    idx = max(0, min(len(P)-1, int(len(P)*0.7)))
    fig.add_annotation(x=t[idx], y=P[idx], text=f"r = {r:.4f}",
                       showarrow=False, font=dict(color='rgb(235, 219, 178)', size=13),
                       bgcolor='rgba(50, 48, 47, 0.5)', yshift=18)
    return fig
