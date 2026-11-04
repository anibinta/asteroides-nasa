import random
import streamlit as st

COULEURS = {
    "fond": "#04050D",      # noir de l'espace
    "soleil": "#FFC857",    # jaune doré
    "mars": "#FF6B4A",      # orange-rouge
    "saturne": "#F1DFA6",   # beige clair
    "uranus": "#6FE3E0",    # cyan glacé
    "neptune": "#4C7DFF",   # bleu profond
    "texte": "#EAF0FF",     # blanc légèrement bleuté
}


def _etoiles(nombre, graine, flou, hauteur=2000, largeur=2600):
    """Fabrique la liste des positions d'étoiles pour le CSS (box-shadow).
    Chaque étoile est dessinée deux fois (y et y + hauteur) pour que
    la boucle de l'animation soit invisible."""
    hasard = random.Random(graine)
    points = []
    for _ in range(nombre):
        x = hasard.randint(0, largeur)
        y = hasard.randint(0, hauteur)
        couleur = hasard.choice(["#FFFFFF", "#FFFFFF", "#CFE3FF", "#FFE9C7"])
        points.append(f"{x}px {y}px {flou}px {couleur}")
        points.append(f"{x}px {y + hauteur}px {flou}px {couleur}")
    return ",".join(points)


def appliquer_theme():
    c = COULEURS
    petites = _etoiles(700, graine=1, flou=0)
    grosses = _etoiles(160, graine=2, flou=3)

    css = f"""
    <style>
    /* ---------- Fond : noir lumineux avec lueurs de nébuleuse ---------- */
    .stApp {{
        background:
            radial-gradient(ellipse 60% 45% at 88% 0%, rgba(76,125,255,.22), transparent 62%),
            radial-gradient(ellipse 50% 40% at 0% 100%, rgba(255,107,74,.14), transparent 62%),
            radial-gradient(ellipse 45% 30% at 50% 55%, rgba(138,92,255,.08), transparent 70%),
            {c["fond"]};
    }}
    [data-testid="stHeader"] {{ background: transparent; }}

    /* ---------- Étoiles qui dérivent (deux couches) ---------- */
    .stApp::before, .stApp::after {{
        content: "";
        position: fixed;
        top: 0; left: 0;
        border-radius: 50%;
        background: transparent;
        pointer-events: none;
        z-index: 0;
    }}
    .stApp::before {{
        width: 1.5px; height: 1.5px;
        box-shadow: {petites};
        animation: derive 200s linear infinite;
    }}
    .stApp::after {{
        width: 3px; height: 3px;
        box-shadow: {grosses};
        animation: derive 110s linear infinite, scintille 5s ease-in-out infinite alternate;
    }}
    @keyframes derive {{ to {{ transform: translateY(-2000px); }} }}
    @keyframes scintille {{ from {{ opacity: .45; }} to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{
        .stApp::before, .stApp::after {{ animation: none; }}
    }}

    /* Le contenu passe devant les étoiles */
    [data-testid="stAppViewContainer"] {{ position: relative; z-index: 1; background: transparent; }}
    [data-testid="stHeader"] {{ position: relative; z-index: 2; }}

    /* ---------- Titre et pastille ---------- */
    .pastille {{
        display: inline-block;
        padding: 4px 14px;
        border: 1px solid {c["uranus"]};
        border-radius: 999px;
        color: {c["uranus"]};
        font-size: .78rem;
        letter-spacing: .12em;
        font-weight: 600;
        box-shadow: 0 0 14px rgba(111,227,224,.25);
    }}
    .titre {{
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        margin: .6rem 0 .2rem 0;
        padding: 0;
        color: {c["texte"]};
    }}
    .titre .astre {{
        background: linear-gradient(90deg, {c["soleil"]}, {c["mars"]});
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }}
    .sous-titre {{ color: #9AA6D0; margin-bottom: 1.2rem; }}

    /* ---------- Barre latérale en verre sombre ---------- */
    [data-testid="stSidebar"] {{
        background: rgba(10,14,40,.62);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,.08);
    }}

    /* ---------- Chiffres clés : une planète par carte ---------- */
    [data-testid="stMetric"] {{
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.10);
        border-radius: 16px;
        padding: 16px 20px;
        backdrop-filter: blur(6px);
    }}
    [data-testid="stMetricLabel"] {{ color: #9AA6D0; }}
    [data-testid="stMetricValue"] {{ font-weight: 800; }}
    [data-testid="stColumn"]:nth-child(1) [data-testid="stMetricValue"] {{ color: {c["soleil"]}; }}
    [data-testid="stColumn"]:nth-child(2) [data-testid="stMetricValue"] {{ color: {c["mars"]}; }}
    [data-testid="stColumn"]:nth-child(3) [data-testid="stMetricValue"] {{ color: {c["uranus"]}; }}
    [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {{ box-shadow: 0 0 26px rgba(255,200,87,.10); }}
    [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {{ box-shadow: 0 0 26px rgba(255,107,74,.10); }}
    [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {{ box-shadow: 0 0 26px rgba(111,227,224,.10); }}

    /* ---------- Onglets ---------- */
    button[data-baseweb="tab"][aria-selected="true"] {{ color: {c["soleil"]}; }}
    div[data-baseweb="tab-highlight"] {{ background-color: {c["soleil"]}; }}

    /* ---------- Titres de sections ---------- */
    h2, h3 {{ color: {c["saturne"]}; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)