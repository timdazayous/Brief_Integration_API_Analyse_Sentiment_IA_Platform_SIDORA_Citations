# frontend/pages/3_analyser_sentiment.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Dossier logs + fichier de log
os.makedirs("logs", exist_ok=True)
logger.add("logs/frontend_analyser_sentiment.log", rotation="500 MB", level="INFO")

API_IA_URL   = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_2_PORT', '8080')}/analyse_sentiment/"

st.title("Analyse de texte (anglophone) par Sentiment IA")

text_to_analyse = st.text_area("Saisissez le texte à analyser")

if st.button("Lancez l'analyse IA"):
    if text_to_analyse:
        logger.info(f"Envoi à l'API IA pour analyse : {text_to_analyse}")
        try:
            analyse_resp = requests.post(
                API_IA_URL,
                json={"text": text_to_analyse},
                timeout=5
            )
            logger.info(f"Réponse API IA status={analyse_resp.status_code} body={analyse_resp.text}")

            if analyse_resp.status_code == 200:
                data = analyse_resp.json()
                st.success("Résultat de l'analyse")
                st.json(data)
                logger.success("Connexion à l'api IA reussie et score polarité affiché")
                
                if data['compound'] == 0:
                    st.info('Le score IA sentiment montre une tendance neutre')
                elif data['compound'] > 0:
                    st.info('Le score IA sentiment montre une tendance positive')
                else:
                    st.info('Le score IA sentiment montre une tendance negative')
            else:
                st.error(f"Erreur de l'API IA : {analyse_resp.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(f"Impossible de se connecter à l'API IA {API_IA_URL}")
            logger.exception("Erreur de connexion à l'API IA")
    else:
        st.warning("Veuillez saisir du texte pour le faire analyser et obtenir son score de polarité")
        logger.warning("Pas de texte saisi lors du clic sur button")