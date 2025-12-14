#### ✔️ Installation des bibliothèques
`pip install fastapi uvicorn loguru streamlit requests python-dotenv sqlalchemy pytest httpx`

ou 

`pip install -r requirements.txt`

Un mini programme complet:
* **frontend** (streamlit)
  * **pages**
* **backend**:
  * **modules** (contenir nos propres modules)
  * **data** (nos csv/DB)

#### 📍 Architecture du projet
```
mon_projet(FAST_API_INITIATION)/
├── backend
│   ├── modules
│   |   ├── db_tools.py
│   │   └── df_tools.py
│   ├── data
|   |   ├──quotes_db.sqlite
│   │   └── quotes_db.csv
│   └── main.py
├── frontend
│   ├── app.py
│   └── pages
│       ├── 0_insérer.py
│       ├── 1_Afficher.py
│       ├── 2_Rechercher.py
|       └── 3_analyser_sentiment.py
├── API_IA
|   └── sentiment_api.py
├── tests
│   ├── test_api_ia_sentiment.py
│   ├── test_initiation.py
│   ├── test_backend_api.py
│   └── test_backend_orm.py
├── DEV
│   ├── quotes_db.csv
│   ├── dev.ipynb
│   └── dev.py
├── README.md
├── pytest.ini
├── .env
├── .venv
├── requirements.txt
└── .gitignore
```

#### 🔎 Fonctions de l'application
* Affichage d'une interface graphique Streamlit composée de plusieurs pages:
  * ℹ️ Un accueil permettant de ping l'API de gestion des citations
  * 📝 Une page inserer permettant d'ajouter une nouvelle citation à la base de données
  * 📃 Une page afficher permettant d'afficher toutes les citations de la base de données
  * 🔎 Une page rechercher permettant la recherche aléatoire ou par id d'une citation et d'analyser le score de polarité de cette derniere par API Sentiment IA (anglophone)
  * 📈 Une page analyse de sentiment permettant de saisir un texte et d'en connaitre le score de polarité avec l'API Sentiment IA (angolophone)

#### 💹 Comment fonctionne l'application
* 1️⃣ Une api pour la gestion de la base de données des citations ajout, lecture
* 2️⃣ Une api IA pour l'analyse de sentiment (model NLTK VADER)
* 3️⃣ Une interface utilisateur Streamlit contenant diverses pages pour utiliser les fonctions des deux API 

Uvicorn permet de connecter les deux API avec l'interface (localhost à l'ip 127.0.0.1)
Une base de données SQL pour le stockage des citations

#### ☑️ Mise en place de procedure de test, de gestion d'exception, d'erreur, et journalisation
* Dossier `tests` contenant les divers test sur les fonctions des deux API 
* Mise en place de bloc try except pour gerer les erreurs et exceptions liées au fonctionnement de l'application (erreur de saisie, de connexion avec les api, etc.)
* Dossier `logs` contenant la journalisation du fonctionnement de l'API IA sentiment dans son ensemble

#### 💻 Lancement de l'application
* 1️⃣ Terminale 1 Lancement de l'API de gestion des citations: `py backend\main.py`
* 2️⃣ Terminale 2 Lancement de l'API d'analyse de sentiment IA: `py API_IA\sentiment_api.py`
* 3️⃣ Terminale 3 Lancement de l'interface Streamlit: `streamlit run frontend\app.py`

#### L'ancienne base de données "quotes_db.csv"
Colonnes:
- `id`
- `text`

#### Ma base de données actuelle "quotes_db.sqlite"
Colonnes:
- `id`
- `text`
- 
#### Commande pour lancer le serveur uvicorn

`uvicorn chemin.nom:app --reload --log-level debug`

#### Commandes pour le terminale pour faire un GET

- `Powershell` : `Invoke-WebRequest -Method GET "http://127.0.0.1:8000/citation"`

- `MAC Linux` : `CURL -X GET "http://127.0.0.1:8000/citation"`

#### Commande pour streamlit

`streamlit run frontend.\app.py`
