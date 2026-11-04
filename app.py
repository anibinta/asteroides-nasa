import requests
import pandas as pd
import streamlit as st
from datetime import date, timedelta

from theme import appliquer_theme, COULEURS

st.set_page_config(page_title="Astéroïdes proches de la Terre", page_icon="☄️", layout="wide")
appliquer_theme()

URL = "https://api.nasa.gov/neo/rest/v1/feed"
try:
    CLE_API = st.secrets["NASA_API_KEY"]
except Exception:
    CLE_API = "DEMO_KEY"

st.markdown('<span class="pastille">☄ DONNÉES NASA · NEOWS</span>', unsafe_allow_html=True)
st.markdown('<h1 class="titre">Astéroïdes <span class="astre">proches de la Terre</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="sous-titre">Quels objets célestes frôlent notre planète ces jours-ci ?</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filtres")
    debut = st.date_input("Date de début", value=date.today() - timedelta(days=2))
    fin = st.date_input("Date de fin", value=date.today())
    seulement_dangereux = st.checkbox("Seulement les astéroïdes potentiellement dangereux")


@st.cache_data
def charger(debut, fin):
    params = {"start_date": str(debut), "end_date": str(fin), "api_key": CLE_API}
    reponse = requests.get(URL, params=params)
    reponse.raise_for_status()
    donnees = reponse.json()

    lignes = []
    for jour, asteroides in donnees["near_earth_objects"].items():
        for a in asteroides:
            approche = a["close_approach_data"][0]
            lignes.append({
                "date": jour,
                "nom": a["name"],
                "diametre_max_m": round(a["estimated_diameter"]["meters"]["estimated_diameter_max"]),
                "vitesse_km_h": round(float(approche["relative_velocity"]["kilometers_per_hour"])),
                "distance_km": round(float(approche["miss_distance"]["kilometers"])),
                "dangereux": a["is_potentially_hazardous_asteroid"],
            })
    return pd.DataFrame(lignes)


if fin < debut:
    st.error("La date de fin doit être après la date de début.")
    st.stop()
if (fin - debut).days > 6:
    st.warning("L'API accepte 7 jours maximum à la fois.")
    st.stop()

try:
    df = charger(debut, fin)
except Exception as e:
    st.error(f"Impossible de récupérer les données : {e}")
    st.stop()

if seulement_dangereux:
    df = df[df["dangereux"]]

if df.empty:
    st.info("Aucun astéroïde ne correspond à ces critères.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Astéroïdes", len(df))
c2.metric("Plus gros (m)", int(df["diametre_max_m"].max()))
c3.metric("Plus proche (km)", f"{int(df['distance_km'].min()):,}".replace(",", " "))

onglet1, onglet2, onglet3 = st.tabs(["📋 Tableau", "📊 Par jour", "🔵 Taille et distance"])

with onglet1:
    st.dataframe(df.rename(columns={
        "date": "Date",
        "nom": "Nom",
        "diametre_max_m": "Diamètre max (m)",
        "vitesse_km_h": "Vitesse (km/h)",
        "distance_km": "Distance (km)",
        "dangereux": "Dangereux",
    }))

with onglet2:
    st.bar_chart(df.groupby("date").size(), color=COULEURS["neptune"])

with onglet3:
    df_points = df.assign(couleur=df["dangereux"].map({True: COULEURS["mars"], False: COULEURS["uranus"]}))
    st.scatter_chart(df_points, x="distance_km", y="diametre_max_m", color="couleur")
    st.markdown(
        f'<span style="color:{COULEURS["mars"]}">●</span> potentiellement dangereux &nbsp;&nbsp; '
        f'<span style="color:{COULEURS["uranus"]}">●</span> autres',
        unsafe_allow_html=True,
    )