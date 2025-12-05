# backend/main.py
from fastapi import FastAPI
import uvicorn
import os 
from dotenv import load_dotenv 

load_dotenv()

API_ROOT_URL =  f"http://127.0.0.1:{os.getenv('FASTAPI_PORT', '8080')}"
                                    

# def timer_decorator(function):
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         result = function(*args, **kwargs)
#         end = time.perf_counter()
#         print(f"La fonction {function.__name__} a été exécutée en : {end - start: .5f} secondes")
#         return result
#     return wrapper

# --- Configuration ---
app = FastAPI(title="API")

# --- Routes API ---
# http://www.google.com/fr route fr
# http://www.google.com/en route en 
# http://www.google.com/ route principale

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@app.get("/citation")
def read_citation():
    return {"auteur": "Cyril", "citation": "Caractéristique qui, pour tout ensemble, fini ou infini, permet de définir une notion équivalente au nombre d'éléments à travers la mise en place d'une bijection entre ensembles."}

@app.get("/fr")
def read_root_fr():
    return {"Bonjour": "Monde", "status": "API est ok"}


if __name__ == "__main__":
    # 1 - on récupère le port de l'API
    try:
        print("Hello")
        port = os.getenv('FAST_API_PORT')
        url = os.getenv('API_BASE_URL')
        port = int(port)
        print(port)
    except ValueError:
        print("ERREUR")
        port = 8080

    # 2 - On lance uvicorn
    uvicorn.run(
        "main:app", 
        host = url,
        port = port, 
        reload = True
    )