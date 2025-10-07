import dash
from dash import html

dash.register_page(__name__, path='/', name='Inicio')

layout = html.Div([
    html.H1("Bienvenido a Técnicas de Modelamiento Matemático", className="title"),
    html.P("Selecciona una página del menú superior para comenzar.", className="content")
], className="page-container")
