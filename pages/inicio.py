import dash
from dash import html

# ------------------------------------------------------------
# Página "Inicio" (Sobre mí)
# ------------------------------------------------------------
dash.register_page(__name__, path="/", name="Inicio")

layout = html.Div(
    className="page-container about-page",
    children=[
        # ================== COLUMNA IZQUIERDA ==================
        html.Div(
            className="about-left",
            children=[
                html.H1("Sobre mí", className="title"),
                html.Div(
                    className="about-photo-box",
                    children=html.Img(
                        src="assets/images/perfil.jpg",  
                        alt="Foto de perfil",
                        className="about-photo"
                    )
                ),
            ],
        ),

        # ===== Separador vertical entre columnas (desktop) =====
        html.Div(className="about-divider"),

        # ================== COLUMNA DERECHA ==================
        html.Div(
            className="about-right",
            children=[
                html.H2("Mark Quispe Gonzales", className="about-name"),

                html.P(
                    (
                        "Estudiante de Computación Científica en la UNMSM (Facultad de Ciencias "
                        "Matemáticas). Reciente interés en el modelamiento matemático, data science y "
                        "manejo de datos. Actualmente desarrollando pequeños proyectos en Python y "
                        "mejorando habilidades en LaTeX."
                    ),
                    className="content"
                ),

                # ---------- GRID DE TARJETAS ----------
                html.Div(
                    className="about-grid",
                    children=[
                        html.Div(
                            className="about-card",
                            children=[
                                html.H3("Perfil", className="about-card-title"),
                                html.Ul([
                                    html.Li("UNMSM — Computación Científica"),
                                    html.Li("Ciclo: 6°"),
                                    html.Li("Intereses: Redacción en LaTeX, Portafolios, SQL para manejo de datos"),
                                ])
                            ],
                        ),
                        html.Div(
                            className="about-card",
                            children=[
                                html.H3("Habilidades", className="about-card-title"),
                                html.Ul([
                                    html.Li("Python (NumPy, Pandas, Matplotlib, TensorFlow)"),
                                    html.Li("LaTeX / Ofimática / C++"),
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
                                    html.Li("Animación de un Sistema Solar"),
                                    html.Li("Web scraping a pequeños datos públicos"),
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
                        # ---------- TARJETA DESTACADA ----------
                        html.Div(
                            className="about-card update",
                            children=[
                                html.H3("⚡ ACTUALIZACIÓN DE PÁGINA", className="about-card-title"),
                                html.Ul([
                                    html.Li("Se Agrego Modelo SIR y SEIR"),
                                    html.Li("Las graficas SIR y SEIR en estos nuevos modelos se actualizan en tiempo real conforme uno mueve los valores"),
                                    html.Li("Las graficas SIR y SEIR traen interpretacion que te actualiza conforme la grafica cambia en tiempo real"),

                                ]),
                                html.Small(
                                    "Última actualización: 03 de Noviembre 2025",
                                    className="update-date"
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
