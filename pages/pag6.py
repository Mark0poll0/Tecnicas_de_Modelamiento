import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go

# =======================================================
# Registro de página
# =======================================================
dash.register_page(__name__, path='/pagina6', name='Pagina 6')


# =======================================================
# Layout estandarizado (igual a tus páginas 4–7)
# =======================================================
layout = html.Div([

    # -------------------- IZQUIERDA --------------------
    html.Div([
        html.H2("Campo Vectorial 2D", className="title"),

        html.Div([
            html.Label("Ecuación dx/dt ="),
            dcc.Input(id="input-fx", type="text",
                      value="np.sin(X)", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Ecuación dy/dt ="),
            dcc.Input(id="input-fy", type="text",
                      value="np.sin(Y)", className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Rango del eje X (máx):"),
            dcc.Input(id="input-xmax", type="number",
                      value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Rango del eje Y (máx):"),
            dcc.Input(id="input-ymax", type="number",
                      value=5, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Resolución de la malla (n × n):"),
            dcc.Input(id="input-n", type="number",
                      value=15, className="input-field")
        ], className="input-group"),

        html.Button("Generar campo vectorial",
                    id="btn-generar", className="btn-generar"),

        html.Br(), html.Br(),

        # Caja explicativa tipo page 6
        html.Div([
            html.H3("Ejemplos útiles:", className="subtitle-small"),
            html.P("• dx/dt = X, dy/dt = Y  (radial)"),
            html.P("• dx/dt = -Y, dy/dt = X  (rotacional antihorario)"),
            html.P("• dx/dt = Y, dy/dt = -X  (rotacional horario)"),
            html.P("• dx/dt = np.sin(X), dy/dt = np.cos(Y)"),
        ], className="text-explain")

    ], className="content left"),


    # -------------------- DERECHA --------------------
    html.Div([
        html.H2("Visualización del Campo Vectorial", className="title"),
        dcc.Graph(id="grafica-campo",
                  style={'height': '470px', 'width': '100%'}),

        html.Div(id="info-campo",
                 className="text-explain",
                 style={"margin-top": "18px"})
    ], className="content right")

], className="page-container page6-container")
# usa estilos de page6 (ya definidos)


# =======================================================
# CALLBACK — Generación del Campo Vectorial
# =======================================================
@callback(
    [Output("grafica-campo", "figure"),
     Output("info-campo", "children")],
    Input("btn-generar", "n_clicks"),
    State("input-fx", "value"),
    State("input-fy", "value"),
    State("input-xmax", "value"),
    State("input-ymax", "value"),
    State("input-n", "value"),
    prevent_initial_call=False
)
def actualizar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):

    # ------------- Crear malla -------------
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)

    info_mensaje = ""

    # ------------- Evaluar expresiones -------------
    try:
        entorno_seguro = {
            'X': X, 'Y': Y,
            'np': np,
            'sin': np.sin, 'cos': np.cos,
            'tan': np.tan, 'exp': np.exp,
            'sqrt': np.sqrt,
            'pi': np.pi, 'e': np.e
        }

        fx = eval(fx_str, {"__builtins__": {}}, entorno_seguro)
        fy = eval(fy_str, {"__builtins__": {}}, entorno_seguro)

        magnitudes = np.sqrt(fx**2 + fy**2)
        mag_max = float(np.max(magnitudes))
        mag_min = float(np.min(magnitudes))

        info_mensaje = f"Magnitud del campo: min = {mag_min:.2f}, max = {mag_max:.2f}"

    except Exception as e:
        fx = np.zeros_like(X)
        fy = np.zeros_like(Y)
        info_mensaje = f"Error en la expresión: {str(e)}"


    # ======================================================
    # FIGURA — versión estilizada como tus otras páginas
    # ======================================================
    fig = go.Figure()

    # Dibujar vectores como flechas
    for i in range(n):
        for j in range(n):
            x0, y0 = X[i, j], Y[i, j]
            x1, y1 = x0 + fx[i, j], y0 + fy[i, j]

            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(color="rgb(250,189,47)", width=2),  # dorado Gruvbox
                hovertemplate=
                f"Punto ({x0:.1f},{y0:.1f})<br>Vector ({fx[i,j]:.2f},{fy[i,j]:.2f})<extra></extra>",
                showlegend=False
            ))

    # ---- Layout ----
    fig.update_layout(
        title=dict(text=f"<b>Campo Vectorial: dx/dt = {fx_str}, dy/dt = {fy_str}</b>",
                   x=0.5, font=dict(size=18, color="rgb(250,189,47)")),
        xaxis_title="x",
        yaxis_title="y",

        paper_bgcolor="rgb(40,40,40)",
        plot_bgcolor="rgb(50,48,47)",
        font=dict(family="Outfit", size=13, color="rgb(213,196,161)"),

        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(
        zeroline=True, zerolinecolor="rgb(250,189,47)", zerolinewidth=2,
        gridcolor="rgb(80,73,69)"
    )
    fig.update_yaxes(
        zeroline=True, zerolinecolor="rgb(250,189,47)", zerolinewidth=2,
        gridcolor="rgb(80,73,69)",
        scaleanchor="x", scaleratio=1
    )

    return fig, info_mensaje
