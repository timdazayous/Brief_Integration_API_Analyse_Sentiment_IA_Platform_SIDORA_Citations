import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_ROOT_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '9090')}"
API_IA_URL   = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_2_PORT', '8080')}"

st.title("Lire une citation")

mode = st.radio("Choisissez le mode de recherche :", ("Aléatoire", "Par ID"))

# ---------- MODE ALEATOIRE ----------
if mode == "Aléatoire":
    st.subheader("Citation aléatoire")
    api_url = API_ROOT_URL + "/read/random/"

    if st.button("Obtenir une citation aléatoire"):
        try:
            response = requests.get(api_url, timeout=5)

            if response.status_code == 200:
                result = response.json()
                if result:
                    text = result.get("text", "texte non trouvé")
                    quote_id = result.get("id", "N/A")

                    st.success(f"Citation avec ID {quote_id}")
                    st.info(text)
                    st.balloons()

                    if st.button("Analyser le sentiment de cette citation"):
                        try:
                            analyse_resp = requests.post(
                                API_IA_URL + "/analyse_sentiment/",
                                json={"text": text},
                                timeout=5,
                            )
                            if analyse_resp.status_code == 200:
                                data = analyse_resp.json()
                                st.write("Scores de sentiment :")
                                st.json(data)
                            else:
                                st.error(f"Erreur de l'API IA : {analyse_resp.status_code}")
                        except requests.exceptions.ConnectionError:
                            st.error(f"Impossible de se connecter à l'API IA {API_IA_URL}")
                else:
                    st.warning("Aucune citation disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {api_url}")
            st.warning("Assure-toi que le serveur Uvicorn du backend est bien lancé.")

# ---------- MODE PAR ID ----------
else:
    st.subheader("Citation par ID")
    api_url = API_ROOT_URL + "/read/"

    with st.form("search_by_id"):
        quote_id = st.number_input("Entrez l'ID de la citation :", min_value=1, step=1)
        submitted = st.form_submit_button("Rechercher")

    if submitted:
        try:
            response = requests.get(api_url + str(quote_id), timeout=5)

            if response.status_code == 200:
                result = response.json()
                if result:
                    text = result.get("text", "texte non trouvé")

                    st.success(f"Citation avec ID {quote_id}")
                    st.info(text)
                    st.balloons()

                    if st.button("Analyser le sentiment de cette citation", key="analyse_by_id"):
                        try:
                            analyse_resp = requests.post(
                                API_IA_URL + "/analyse_sentiment/",
                                json={"text": text},
                                timeout=5,
                            )
                            if analyse_resp.status_code == 200:
                                data = analyse_resp.json()
                                st.write("Scores de sentiment :")
                                st.json(data)
                            else:
                                st.error(f"Erreur de l'API IA : {analyse_resp.status_code}")
                        except requests.exceptions.ConnectionError:
                            st.error(f"Impossible de se connecter à l'API IA {API_IA_URL}")
                else:
                    st.warning(f"La citation {quote_id} n'est pas disponible dans la DB")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {api_url}")
            st.warning("Assure-toi que le serveur Uvicorn du backend est bien lancé.")
