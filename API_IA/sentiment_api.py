# API_IA/sentiment_api.py
from nltk.sentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel
from pydantic import Field, BaseModel
from loguru import logger
import os
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# modèle pydantic
class QuoteIAnalyse(BaseModel):
    text : str = Field(min_length=1, description="donnez un texte pour la citation")

# initialisation de Vader
sia = SentimentIntensityAnalyzer()

app = FastAPI(title="API IA Sentiment")

#création du dossier logs si besoin
os.makedirs("logs", exist_ok=True)

logger.add("logs/sentiment_api.log", rotation="500 MB", level="INFO")


@app.post("/analyse_sentiment/")
async def analyse_sentiment(quote: QuoteIAnalyse):
    """" 
    Recoit un texte (anglophone pour une analyse correcte) et renvoie un score de sentiment par IA

    Paramètres
    ----------
    quote : QuoteIAnalyse
        Objet contenant le texte à analyser 
    
    Retourne une dictionnaire contenant l'analyse de sentiment par IA
    """
    logger.info(f"Analyse du texte: {quote.text}")
    try:
        sentiment = sia.polarity_scores(quote.text)
        logger.info(f"Resultats IA: {sentiment}")

        return {
            "neg": sentiment["neg"],
            "neu": sentiment["neu"],
            "pos": sentiment["pos"],
            "compound": sentiment["compound"]
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse IA: {e}")

if __name__ == "__main__":
    import subprocess
    import sys

    
    cmd = [
        sys.executable,               # python du venv
        "-m", "uvicorn",
        "API_IA.sentiment_api:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload",
    ]
    subprocess.run(cmd)
