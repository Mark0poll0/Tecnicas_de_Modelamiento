import dash
from dash import html, dcc

app = dash.Dash(__name__, use_pages=True)
server = app.server  # opcional para despliegue

app.layout = html.Div([
    html.H1("Técnicas de Modelamiento Matemático", className='app-header'),

    html.Div([
        dcc.Link(f"{page['name']}", href=page["relative_path"], className='nav-link')
        for page in dash.page_registry.values()
    ], className='navigation'),

    dash.page_container
], className='app-container')

if __name__ == "__main__":
    app.run(debug=True)
