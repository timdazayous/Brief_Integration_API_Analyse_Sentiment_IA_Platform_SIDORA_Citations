# frontend/pages/2_Rechercher.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Dossier logs + fichier de log
os.makedirs("logs", exist_ok=True)
logger.add("logs/frontend_sentiment.log", rotation="500 MB", level="INFO")

API_ROOT_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '9090')}"
API_IA_URL   = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_2_PORT', '8080')}/analyse_sentiment/"

st.title("Lire une citation")

# État pour garder la dernière citation affichée
if "current_text" not in st.session_state:
    st.session_state.current_text = None
if "current_id" not in st.session_state:
    st.session_state.current_id = None

mode = st.radio("Choisissez le mode de recherche:",
                ("Aléatoire", "Par ID "))

# ---------- MODE ALÉATOIRE ----------
if mode == "Aléatoire":
    st.subheader("Citation Aléatoire")
    API_URL = API_ROOT_URL + "/read/random/"

    if st.button("Obtenir une citation aléatoire:"):
        logger.info(f"Demande de citation aléatoire à {API_URL}")
        try:
            response = requests.get(API_URL, timeout=5)
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Réponse backend random: {result}")

                if result:
                    st.session_state.current_id = result.get('id', 'N/A')
                    st.session_state.current_text = result.get('text', 'text non trouvé')

                    st.success(f"Citation avec ID {st.session_state.current_id}")
                    st.info(st.session_state.current_text)
                    st.balloons()
                else:
                    st.warning("Aucune citation disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")
                logger.error(f"Erreur backend random {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
            logger.exception("Erreur de connexion au backend random")

# ---------- MODE PAR ID ----------
else:
    st.subheader("Citation par ID")
    API_URL = API_ROOT_URL + "/read/"

    with st.form("search_by_id"):
        quote_id = st.number_input("Entrez l'ID de la citation:",
                                   min_value=1, step=1)
        submitted = st.form_submit_button("Rechercher")

    if submitted:
        logger.info(f"Demande de citation ID={quote_id} à {API_URL}")
        try:
            response = requests.get(API_URL + str(quote_id), timeout=5)
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Réponse backend ID {quote_id}: {result}")

                if result:
                    st.session_state.current_id = quote_id
                    st.session_state.current_text = result.get('text', 'text non trouvé')

                    st.success(f"Citation avec ID {quote_id}")
                    st.info(st.session_state.current_text)
                    st.balloons()
                else:
                    st.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")
                logger.error(f"Erreur backend ID {quote_id} {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
            logger.exception("Erreur de connexion au backend par ID")

# ---------- BOUTON D'ANALYSE SENTIMENT IA ----------
st.markdown("---")
st.subheader("Analyse de sentiment IA")

if st.session_state.current_text:
    # st.info(f"Citation acutelle (ID {st.session_state.current_id}) :")
    st.write(st.session_state.current_text)
else:
    st.warning("Aucune citation sélectionnée pour l'instant.")

if st.button("Analyser le sentiment de la citation affichée"):
    if not st.session_state.current_text:
        st.error("Aucune citation n'est affichée. Veuillez d'abord en rechercher une.")
        logger.warning("Bouton d'analyse cliqué sans citation courante")
    else:
        logger.info(f"Envoi à l'API IA pour analyse: ID={st.session_state.current_id}")
        try:
            analyse_resp = requests.post(
                API_IA_URL,
                json={"text": st.session_state.current_text},
                timeout=5,
            )
            logger.info(f"Réponse API IA status={analyse_resp.status_code} body={analyse_resp.text}")

            if analyse_resp.status_code == 200:
                data = analyse_resp.json()
                st.success("Résultats de l'analyse IA :")
                st.json(data)

                if data['compound'] == 0:
                    st.info('Le score IA sentiment montre une tendance neutre')
                elif data['compound'] > 0:
                    st.info('Le score IA sentiment montre une tendance positive')
                else:
                    st.info('Le score IA sentiment montre une tendance negative')
                    
            else:
                st.error(f"Erreur de l'API IA : {analyse_resp.status_code}")
                st.write("Réponse brute :", analyse_resp.text)
        except requests.exceptions.ConnectionError:
            st.error(f"Impossible de se connecter à l'API IA {API_IA_URL}")
            logger.exception("Erreur de connexion à l'API IA")
