import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Estimateur de Loyer - MEDIABOX",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS PERSONNALISÉ (Thème MEDIABOX, coins vifs) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1F2937;
    }

    /* Variables de couleurs MEDIABOX */
    :root {
        --primary: #F97316;      /* Orange vif du logo */
        --primary-hover: #EA580C; /* Orange plus foncé au survol */
        --primary-light: #FFEDD5; /* Fond très clair */
        --gray-bg: #F3F4F6;
        --border-color: #E5E7EB;
    }

    /* En-tête Hero avec logo */
    .hero-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.5rem 0 1.5rem 0;
        border-bottom: 3px solid var(--primary);
        margin-bottom: 2rem;
    }
    .hero-header h1 {
        font-weight: 700;
        font-size: 2.4rem;
        color: #EE4609;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-header .subtitle {
        font-weight: 400;
        color: #6B7280;
        font-size: 1.1rem;
        margin-top: 0.2rem;
    }

    /* Cartes de saisie – coins vifs, ombre légère */
    .input-section {
        background: white;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .input-section h3 {
        font-weight: 600;
        margin-bottom: 0rem;
        color: #111827;
        border-left: 5px solid var(--primary);
        padding-left: 0.75rem;
    }

    /* Inputs & Selects - Style Flat & Sharp */
    .stNumberInput > label, .stSelectbox > label {
        font-weight: 600 !important;
        color: #374151 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.3rem !important;
    }
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 5px !important;
        border: 1px solid var(--border-color) !important;
        background-color: #374151 !important;
    }
    .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2) !important;
    }

    /* Checkbox stylisées en "boutons carrés" */
    .stCheckbox {
        display: flex;
        align-items: center;
        margin-bottom: 0rem;
    }
    .stCheckbox label {
        font-weight: 500 !important;
        background: #374151;
        padding: 0.4rem 0.7rem;
        border: 1px solid var(--border-color);
        border-radius: 5px !important; /* Coins vifs */
        width: 100%;
    }
    .stCheckbox div[data-testid="stCheckbox"] {
        border-radius: 0px !important;
    }
    
    /* Bouton principal */
    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        padding: 0.6rem 2rem !important;
        border: none !important;
        border-radius: 0px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Carte de résultat */
    .result-card {
        background: white;
        border: 2px solid var(--primary);
        padding: 2.5rem;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border-radius: 0px !important;
    }
    .result-card .label {
        font-size: 1rem;
        font-weight: 500;
        color: #6B7280;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .result-card .price {
        font-size: 4rem;
        font-weight: 800;
        color: var(--primary);
        line-height: 1;
        margin: 0rem 0;
    }
    .result-card .details {
        color: #4B5563;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Pied de page */
    .footer {
        text-align: center;
        margin-top: 4rem;
        color: #9CA3AF;
        font-size: 0.85rem;
        border-top: 1px solid var(--border-color);
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- CHARGEMENT DU MODÈLE ---
@st.cache_resource
def load_model():
    model_path = '../models/best_model_tuned.joblib'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        st.error("Erreur : Le fichier '../models/best_model_tuned.joblib' est introuvable.")
        return None

model = load_model()

# --- EN-TÊTE avec LOGO MEDIABOX ---
# Assurez-vous d'avoir une image nommée 'mediabox_logo.png' dans le dossier du script.
col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        st.image("mediabox_logo.png", width=100)
    except:
        # Fallback si l'image n'est pas trouvée
        st.markdown("<div style='height:50px; width:50px; background:#F97316;'></div>", unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div class="hero-header">
        <div>
            <h1>Estimateur de loyer</h1>
            <div class="subtitle">Obtenez une estimation du loyer mensuel à Bujumbura en quelques clics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FORMULAIRE PRINCIPAL ---
with st.container():
    st.markdown('<div class="input-section"><h3>Caractéristiques du logement</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        chambres = st.number_input(
            "Nombre de chambres",
            min_value=1,
            max_value=6,
            value=3,
            step=1
        )
        superficie = st.number_input(
            "Superficie (m²)",
            min_value=20.0,
            max_value=350.0,
            value=100.0,
            step=5.0
        )
        age = st.number_input(
            "Âge de la maison (années)",
            min_value=0,
            max_value=40,
            value=10,
            step=1
        )
        distance = st.number_input(
            "Distance route principale (m)",
            min_value=0,
            max_value=300,
            value=100,
            step=5
        )

    with col2:
        quartiers = [
            'Bwiza', 'Buyenzi', 'Cibitoke', 'Gasekebuye', 'Gihosha', 'Jabe',
            'Kamenge', 'Kinama', 'Kinanira', 'Kiriri', 'Musaga', 'Ngagara',
            'Nyakabiga', 'Rohero', 'Autres'
        ]
        quartier = st.selectbox("Quartier", quartiers, help="Sélectionnez le quartier de Bujumbura")

        st.markdown("<hr style='margin: 0.2rem 0; border: 0; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
        st.markdown("**Équipements inclus :**")
        salon = st.checkbox("Salon", value=True)
        sdb = st.checkbox("Salle de bain intérieure", value=True)
        parking = st.checkbox("Parking", value=False)
        meuble = st.checkbox("Meublé", value=False)
        jardin = st.checkbox("Jardin", value=False)
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- BOUTON D'ESTIMATION ---
st.markdown("<br>", unsafe_allow_html=True)
col_btn = st.columns([1])
with col_btn[0]:
    predict_clicked = st.button("Estimer le loyer maintenant", use_container_width=True)

# --- PREDICTION ET RESULTAT ---
if predict_clicked:
    if model is None:
        st.error("Impossible de faire une prédiction car le modèle n'a pas été chargé.")
    else:
        with st.spinner("Analyse en cours..."):
            try:
                confort_score = int(salon) + int(sdb) + int(parking) + int(meuble) + int(jardin)
                chambres_par_superficie = chambres / superficie

                input_data = pd.DataFrame([{
                    'Chambres': chambres,
                    'Superficie_m2': superficie,
                    'DistanceRoute_m': distance,
                    'AgeMaison': age,
                    'Confort_Score': confort_score,
                    'Chambres_par_Superficie': chambres_par_superficie,
                    'Quartier': quartier
                }])

                pred_log = model.predict(input_data)[0]
                loyer_estime = np.expm1(pred_log)

                st.markdown(f"""
                <div class="result-card">
                    <div class="label">Loyer mensuel estimé</div>
                    <div class="price">{loyer_estime:,.0f} BIF</div>
                    <div class="details">
                        {superficie:.0f} m² | {chambres} chambre(s) | {quartier}
                    </div>
                    <div style="margin-top: 0rem; color: #6B7280; font-size:0.9rem; border-top: 1px solid #F3F4F6; padding-top: 1rem;">
                        <small>Estimation basée sur les caractéristiques renseignées</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
                st.info("Vérifiez que les valeurs saisies sont dans les plages d'entraînement du modèle.")

# --- PIED DE PAGE ---
st.markdown("""
<div class="footer">
    <p>&copy; 2026 MEDIABOX Burundi &middot; Estimateur intelligent de loyers à Bujumbura</p>
</div>
""", unsafe_allow_html=True)