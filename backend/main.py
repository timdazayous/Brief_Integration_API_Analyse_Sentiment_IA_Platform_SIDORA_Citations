# backend/main.py
from fastapi import FastAPI, HTTPException
import uvicorn
import os
import sys 
import pandas as pd
from dotenv import load_dotenv 
from pydantic import BaseModel, Field

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.modules.db_tools import read_db, write_db, initialize_db
from typing import List, Annotated

import random
load_dotenv()

# modèles pydantic
class QuoteRequest(BaseModel):
    """
    Modele de données pour créer une nouvelle citation

    Attributs
    ---------
    text : str
        Contenu textuel de la citation à enregistrer.
        Doit  contenir au moins un caractère
    """
    text : str = Field(min_length=1, description="donnez un texte pour la citation")

class QuoteResponse(BaseModel):
    """
    Modèle de réponse représentatn une citation enregistrée

    Attributs
    ---------
    id : int
        Identifiant unique de la citation dans la base.
    text : str
        Contenu textuel de la citation
    """
    id : int
    text : str

# creation si besoin de la base de données
initialize_db()

# --- Configuration ---
app = FastAPI(title="API")

@app.get("/")
def read_root():
    """
    Route test de l'API

    Retourne un message indiquant que l'API fonctionne
    utile pour vérifier rapidement l'êtat du service
    """
    return {"Hello": "World", "status": "API is running"}

@app.post("/insert/", response_model= QuoteResponse)
def insert_quote(quote : QuoteRequest):
    """
    Insère une nouvelle citation dans la base de données

    Etapes
    ------
    1. Lit la base de données existante pour récupérer les citaitons déjà enregistrées
    2. Calcule un nouvel identifiant unique pour la citation à partir de l'index courant
    3. Enregisttre le texte de la citation dasn la base de données via write_db
    4. Retourne l'identifiant et le texte de la citaiton insérée

    Paramètres
    ----------
    quote : QuoteRequest
        Objet contenant le texste de la nouvelle citation

    Retour
    ------
    QuoteResponse
        Citation nouvellement créée avec son id
    """

    # 1. trouver le dernier id dans le csv
    df = read_db()

    # 2. donne un id a ma citation
    if df.empty :
        new_id = 1
    elif df.index.max() <= 0 :
        new_id = 1
    else :
        new_id = 1 + df.index.max()

    # sauvegarde dans la DB
    write_db([{"text": quote.text}])
    # 3.1 créer la nouvelle ligne
    # objet = {"text": [quote.text]}
    # new_row = pd.DataFrame(objet, index = [new_id])

    # 3.2 enregistrer le fichier csv
    # df = pd.concat([df, new_row])
    # write_db(df)

    # 4. pour la confirmation je vais envoyer à l'application
    # la citation avec son id
    return {"id":new_id, "text":quote.text}

@app.get("/read/", response_model=List[QuoteResponse])
def read_all_quotes():
    """
    Renvoie la liste complète de toutes les citations enregistrées dans la base de données

    Lit la base de données, et retourne un df contenant chaque citation sous forme de dictionnaire compatbile avec le modèle QuoteResponse
    """
    df = read_db()
    return df.reset_index().rename(columns={'id':'id','text':'text'}).to_dict('records')


@app.get("/read/{id}", response_model=QuoteResponse)
def read_specific_quotes(id : int):
    """
    Renvoie une citation spécifique à partir de son identifiant.

    Paramètres
    ----------
    id : int
        Identifiant de la citation recherchée.

    Comportement
    ------------
    - Si l'identifiant existe dans l'index du DataFrame, la citation correspondante est renvoyée.
    - Si aucune citation ne correspond à cet identifiant, une erreur HTTP 404 est levée.
    """
    # il me faut toutes les citations pour les connaitres
    df = read_db()
    # filtre par l'id concerné
    if id not in df.index:
        raise HTTPException(status_code=404, detail=f"Citation avec ID {id} non trouvée")
    quote_data = df.loc[id].to_dict()
    quote_data['id'] = id
    # retourne les résultats
    return quote_data

@app.get("/read/random/", response_model=QuoteResponse)
def read_random_quotes():
    """
    Renvoie une citation aléatoire parmi celles enregistrées.

    Comportement
    ------------
    - Si la base de données est vide, renvoie une erreur HTTP 404.
    - Sinon, choisit un identifiant au hasard dans l'index du DataFrame
      et renvoie la citation correspondante.
    """
    # il me faut toutes les citations pour les connaitres
    df = read_db()
    # filtre par l'id concerné  
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Citation avec aléatoire non trouvée")
    
    random_id = random.choice(df.index)
    quote_data = df.loc[random_id].to_dict()
    quote_data['id'] = random_id
    # retourne les résultats
    return quote_data

if __name__ == "__main__":
    """
    Point d'entrée de l'application lorsqu'elle est lancée en script.

    Lit la configuration d'hôte et de port dans les variables d'environnement :
    - API_BASE_URL : adresse d'écoute de l'API (par défaut '127.0.0.1')
    - FAST_API_PORT : port d'écoute (par défaut 8000)

    En cas de problème de conversion du port en entier, un port par défaut (8080)
    est utilisé. L'application FastAPI est ensuite démarrée avec Uvicorn
    en mode reload pour le développement.
    """
    url = "127.0.0.1"
    try:
        print("Hello")
        url = os.getenv("API_BASE_URL", "127.0.0.1")
        port_str = os.getenv("FAST_API_PORT", "8000")
        port = int(port_str)
        print(port)
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "backend.main:app",  # import string
        host=url,
        port=port,
        reload=True,
    )