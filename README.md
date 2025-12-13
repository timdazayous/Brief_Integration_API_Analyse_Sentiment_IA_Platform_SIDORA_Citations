#### Installation des bibliothèques
`pip install fastapi uvicorn loguru streamlit requests python-dotenv sqlalchemy pytest httpx`

Un mini programme complet:
* **frontend** (streamlit)
  * **pages**
* **backend**:
  * **modules** (contenir nos propres modules)
  * **data** (nos csv)

#### Architecture du projet
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

#### Fonctions de l'application
* Affichage d'une interface graphique Streamlit composée de plusieurs pages:
  * ℹ️ Un accueil permettant de ping l'API de gestion des citations
  * 📝 Une page inserer permettant d'ajouter une nouvelle citation à la base de données
  * 📃 Une page afficher permettant d'afficher toutes les citations de la base de données
  * 🔎 Une page rechercher permettant la recherche aléatoire ou par id d'une citation et d'analyser le score de polarité de cette derniere par API Sentiment IA (anglophone)
  * 📈 Une page analyse de sentiment permettant de saisir un texte et d'en connaitre le score de polarité avec l'API Sentiment IA (angolophone)


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
