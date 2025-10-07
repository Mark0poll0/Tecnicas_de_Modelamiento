import dash
from dash import html

dash.register_page(__name__, path="/", name="Sobre mí")

layout = html.Div(
    className="page-container about-page",
    children=[
        html.Div(
            className="about-header",
            children=[
                html.H1("Sobre mí", className="title"),
                html.Div(
                    className="about-photo-box",
                    children=html.Img(
                        src="/assets/images/foto.jpg",
                        alt="Foto de perfil",
                        className="about-photo"
                    )
                ),
            ],
        ),

        html.Div(
            className="about-content",
            children=[
                html.H2("Mark Quispe Gonzales", className="about-name"),

                html.P(
                    (
                        "Estudiante de Computación Científica en la UNMSM (Facultad de Ciencias "
                        "Matemáticas). Reciente interes en el modelamiento matemático, data science y "
                        "manejo de datos. Actualmente desarrollando pequeños proyectos en Python, "
                        "Mejorando habilidades en  LaTeX."
                    ),
                    className="content"
                ),

                html.Div(
                    className="about-grid",
                    children=[
                        html.Div(
                            className="about-card",
                            children=[
                                html.H3("Perfil", className="about-card-title"),
                                html.Ul([
                                    html.Li("UNMSM — Computación Científica"),
                                    html.Li("Ciclo: 6° "),
                                    html.Li("Intereses: Redaccion en Latex, Portafolios,Sql para manejo de Datos "),
                                ])
                            ],
                        ),
                        html.Div(
                            className="about-card",
                            children=[
                                html.H3("Habilidades", className="about-card-title"),
                                html.Ul([
                                    html.Li("Python (NumPy, Pandas, Matplotlib, TensorFlow)"),
                                    html.Li("Latex / ofimatica / C++"),
                                    html.Li("Git & GitHub"),
                                    html.Li("LaTeX (beamer, artículos)"),
                                ])
                            ],
                        ),
                        html.Div(
                            className="about-card",
                            children=[
                                html.H3("Proyectos recientes", className="about-card-title"),
                                html.Ul([
                                    html.Li("Animacion de un Sistema solar"),
                                    html.Li("Web scrapping a pequeños datos publicos"),
                                    html.Li("Dashboards y apps con Dash"),
                                ])
                            ],
                        ),
                        html.Div(
                            className="about-card",
                            children=[
                                html.H3("Contacto", className="about-card-title"),
                                html.Ul([
                                    html.Li("Email: mark.quispe2@unmsm.edu.pe"),
                                    html.Li("GitHub: github.com/Mark0poll0"),
                                    html.Li("LinkedIn: linkedin.com/in/mark-quispe-gonzales"),
                                ])
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
