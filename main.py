# main.py
import streamlit as st
from src.utils.get_data import load_raw_data
from src.utils.clean_data import clean_tourism_data

# -----------------------------
# Chargement des données
# -----------------------------
@st.cache_data
def load_data():
    df_raw = load_raw_data()
    df_clean = clean_tourism_data(df_raw)
    return df_clean

df = load_data()

# -----------------------------
# Navigation multi-pages
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Accueil", "Régions", "International", "Économie"])

if page == "Accueil":
    from src.pages.home import show_home
    show_home(df)
elif page == "Régions":
    from src.pages.regional import show_regional
    show_regional(df)
elif page == "International":
    from src.pages.international import show_international
    show_international(df)
elif page == "Économie":
    from src.pages.economic import show_economic
    show_economic(df)
