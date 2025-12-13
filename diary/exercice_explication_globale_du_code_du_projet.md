## Exercice: Expliquer le fonctionnement du projet

#### Conception du projet
* création d'un dossier de travail
* création des fichiers 
  * .venv (environnement virtuel)
  * .env (les variables d'environnement)
  * la procédure d'installation
    * README.md (la procédured'installation)
    * requirements.txt (pour l'import des bibliothèques)
  * .gitignore (pour le versionnage)
* separation de l'architecture
  * dossiers:
    * FAST_API_INITIATION: contient toute l'application
    * backend: conteint la logique data (DB)
    * API_IA: contient la logique IA (sentiment IA)
  * architecture en couche
    * separation des modules 
    * separation des modèles
    * separation des données
### Abstraction 1
#### Logique / étapes
**Application**
* importation des bibliothèques 
* chargement dfes variables d'environnement
* créations des pages:
  * accueil:
    * bouton ping de l'API type `hello world`
    * transaction GET avec la route `'/`
  * insérer:
    * formulaire pour l'insertion des données
    * transaction POST avec la route `'/insert/`
    * gestion des exceptions
  * read(_all):
    * bouton pour l'affichage de toute les données
    * affichage df de la base de donées
    * transaction GET avec la route `/read/`
    * gestion des exceptions
  * read(_id):
    * selectbox pour la selection d'un id 
    * affichage de la donnée recherché
    * transaction GET avec la route `/read/id`
    * gestion des exceptions
  * read(_random):
    * bouton pour l'affichage d'une donnée aléatoire de la base de données
    * affichage la donnée aléatoire
    * transaction GET avec la route `/read/random/`
    * gestion des exceptions
  * analyse_sentiment(_quote):
    * bouton analyser la citation
    * transaction POST avec la route `/analyse_sentiment/`
    * affichage de l'analyse
    * gestion des exceptions
  * analyse_sentiment(_texte_saisi):
    * formulaire pour la saisie d'une donnée
    * bouton pour l'analyse de la donnée par IA sentiment
    * transaction POST avec la route `/analyse_sentiment/`
    * affichage de l'analyse
    * gestion des exceptions

**API backend**
* importation des bibliothèques
* chargement des variables d'environnement
* définition des modèles pydantique
* initialisation de la base de données
  * création de la base de données si elle n'existe pas 
* création de l'API
* définition des routes
  * route principale - get 
    * hello world
  * route insert - post 
    * vérifie les données, voir choisir un index
    * conversion en df
    * écriture en base de données
    * retourne une info sous info de dictionnaire
  * route read - get
    * lecture de la base de données complète
    * retourne un df
  * route read/id - get
    * **lecture de la base de données complète**
    * filtre une id dans le df
    * retourne un df
  * route logique pour lancer l'API

**API IA SENTIMENT**
* importation des bibliothèques
* chargement des variables d'environnement
* définition du modèle pydantique
* initialisation de Vader 
* création de l'API
* création du dossier logs si besoin
* ajout de logs 
* définition de la route analyse_sentiment - post
  * calcul du score de poularité d'un texte (anglophone)
  * retourne un json de l'analyse
* définition de la route logique pour lancer l'API IA


### Abstraction 2

dans l'idéal une application
1. conception
2. developpement/ recherche(notebook)
   * execution de chaque bloc du code dans un notebook et dans le dossier dev (clone du projet principale ou on peut faire des test plus facilement sans impacter la DB du projet principale etc) avant de les integrer dans le code principal pour comprendre et verifier le bon focntionnement avant de tester plus serieusement avec des tests pytest (pour la partie backend et API_IA)
   * test de l'interface graphique streamlit
   * test de la bonne connexion entre les differentes api et streamlit
   * recherche dans la doc ou autre projet plus ou moins similaire ou verification par llm 
3. production(code et test)
   * tout ce qu'il ya au dessus
4. surveillance (monitoring)
   
**Application**
* setup / préparation de l'application

* créations des pages:
  * accueil:
    * bouton ping de l'API type `hello world`
    * transaction GET avec la route `'/`
  * insérer:
    * formulaire pour l'insertion des données
    * transaction POST avec la route `'/insert/`
    * gestion des exceptions
  * read(_all):
    * bouton pour l'affichage de toute les données
    * affichage df de la base de donées
    * transaction GET avec la route `/read/`
    * gestion des exceptions
  * read(_id):
    * selectbox pour la selection d'un id 
    * affichage de la donnée recherché
    * transaction GET avec la route `/read/id`
    * gestion des exceptions
  * read(_random):
    * bouton pour l'affichage d'une donnée aléatoire de la base de données
    * affichage la donnée aléatoire
    * transaction GET avec la route `/read/random/`
    * gestion des exceptions
  * analyse_sentiment(_quote):
    * bouton analyser la citation
    * transaction POST avec la route `/analyse_sentiment/`
    * affichage de l'analyse
    * gestion des exceptions
  * analyse_sentiment(_texte_saisi):
    * formulaire pour la saisie d'une donnée
    * bouton pour l'analyse de la donnée par IA sentiment
    * transaction POST avec la route `/analyse_sentiment/`
    * affichage de l'analyse
    * gestion des exceptions