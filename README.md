# Pokémon Data Mining -- PokéAPI

Projet de **Data Mining** réalisé dans le cadre du cursus **ESGI -- 2ème
année**.

Ce projet vise à exploiter les données de l'API publique **PokéAPI**
afin de construire une base de données, analyser les données du Pokédex
et produire des statistiques utiles pour comprendre certaines tendances
stratégiques dans l'univers compétitif Pokémon.

------------------------------------------------------------------------

# Objectifs du projet

-   Exploiter les données de l'API Pokémon pour créer une base
    structurée.
-   Automatiser l'import des données via un script Python.
-   Construire un modèle de données adapté à l'analyse.
-   Produire des statistiques sur les Pokémon, leurs types et leurs
    attaques.
-   Générer des visualisations permettant d'identifier des tendances
    dans le gameplay compétitif.

L'analyse statistique permet notamment d'identifier des tendances utiles
pour la **construction d'équipes en format compétitif (VGC)**.

------------------------------------------------------------------------

# Architecture du projet

TP2/
│
├── README.md
│
├── architecture/
│   └── archi.md                # Description de l'architecture du projet
│
├── database/
│   ├── MCD.pdf                 # Modèle conceptuel de données
│   ├── mld.png                 # Modèle logique de données
│   ├── mld.sql                 # Script SQL du modèle logique
│   ├── poke_db.sql             # Création de la base et des tables
│   ├── simple_requests.sql     # Requêtes SQL de test
│   └── view_creation.sql       # Création des vues analytiques
│
├── docs/
│   └── presentation_canva.pdf  # Présentation du projet
│
├── images/
│   └── docs_pokeapi.png        # Documentation PokéAPI utilisée
│
├── scripts/
│   ├── scrapping/              # Scripts d'extraction depuis l'API
│   │
│   └── view_creation/          # Scripts Python générant les graphiques
│
├── views/
│   ├── avg_power_scatter.png
│   ├── mono_vs_double_type.png
│   ├── move_power_boxplot.png
│   ├── moves_by_type_pie.png
│   ├── moves_par_type.png
│   ├── pokemon_par_generation.png
│   ├── pokemon_par_type.png
│   ├── top_pokemon_moves.png
│   └── type_combinations.png

------------------------------------------------------------------------

# Technologies utilisées

## Base de données

-   MariaDB / MySQL
-   Modélisation relationnelle
-   Vues SQL analytiques

## Backend / Extraction

-   Python
-   requests
-   mysql-connector-python

## Analyse des données

-   Pandas
-   Matplotlib

## Source de données

-   PokéAPI\
    https://pokeapi.co/

------------------------------------------------------------------------

# Modélisation des données

Le modèle de données a été conçu pour ne conserver que les informations
utiles à l'analyse :

Tables principales :

-   pokemon
-   type_ref
-   pokemon_type
-   move
-   use_move
-   generation
-   game

Ces tables permettent de représenter les relations entre Pokémon, leurs
types, leurs attaques et leur génération.

------------------------------------------------------------------------

# Extraction des données

L'import des données est automatisé via un script Python.

Le script effectue les étapes suivantes :

1.  Connexion à l'API PokéAPI
2.  Récupération des données
3.  Transformation des données
4.  Insertion dans la base MariaDB

Exécution du script :

``` bash
./execute_python.bash
```

------------------------------------------------------------------------

# Analyse des données

Les analyses reposent sur des **vues SQL analytiques** qui permettent de
produire rapidement des statistiques.

Exemples :

-   v_pokemon_by_generation
-   v_pokemon_by_type
-   v_moves_by_type
-   v_avg_power_by_type
-   v_move_power_distribution

Ces vues sont ensuite exploitées par Python pour générer des graphiques.

------------------------------------------------------------------------

# Visualisations générées

Les graphiques permettent d'explorer plusieurs aspects du Pokédex.

### Pokémon par génération

Permet d'observer quelles générations ont introduit le plus de nouveaux
Pokémon.

### Pokémon par type

Certains types comme **Water, Normal ou Flying** sont particulièrement
représentés.

### Pokémon possédant le plus d'attaques

Certains Pokémon disposent d'un grand nombre d'attaques, leur donnant
une grande polyvalence stratégique.

### Distribution de la puissance des attaques

La majorité des attaques possède une puissance comprise entre **50 et
100**.

### Puissance moyenne des attaques par type

Certains types comme **Fire, Fairy ou Dragon** possèdent en moyenne des
attaques plus puissantes.

### Répartition des attaques par type

Le type **Normal** possède le plus grand nombre d'attaques.

### Pokémon mono-type vs double-type

Les Pokémon **double-type sont légèrement majoritaires**, ce qui montre
l'importance stratégique des combinaisons de types.

------------------------------------------------------------------------

# Apport pour le jeu compétitif

L'exploitation statistique permet d'identifier plusieurs tendances :

-   Types dominants
-   Potentiel offensif moyen des types
-   Combinaisons de types fréquentes
-   Pokémon possédant un large moveset

Ces informations peuvent aider à comprendre certaines logiques du
**métagame VGC**.

------------------------------------------------------------------------

# Automatisation et pipeline Docker

Afin de rendre le projet reproductible et facilement déployable,
l'architecture peut être intégrée dans un **pipeline complet automatisé
via Docker**.

Le pipeline peut suivre les étapes suivantes :

1.  **Container Base de données**
    -   MariaDB exécuté dans un container Docker
    -   Initialisation automatique des tables via `poke_db.sql`
2.  **Container Extraction**
    -   Container Python exécutant `import_pokeapi_full.py`
    -   Connexion à l'API PokéAPI
    -   Import automatique des données dans la base
3.  **Container Analyse**
    -   Scripts Python exécutant les requêtes SQL
    -   Génération des graphiques avec Pandas et Matplotlib
4.  **Orchestration**
    -   Utilisation de `docker-compose`
    -   Déploiement complet en une seule commande

Exemple :

``` bash
docker-compose up --build
```

Avantages :

-   Environnement reproductible
-   Installation simplifiée
-   Automatisation complète du pipeline
-   Déploiement rapide sur n'importe quelle machine

Cette architecture transforme le projet en **pipeline de data mining
complet**, allant de l'extraction de l'API jusqu'à la génération des
visualisations.

------------------------------------------------------------------------

# Améliorations possibles

-   Ajout des statistiques des Pokémon
-   Analyse des talents (abilities)
-   Analyse des matchups entre types
-   Dashboard interactif (Streamlit / PowerBI)
-   Analyse du métagame réel (Smogon / VGC usage stats)

------------------------------------------------------------------------

# Auteur

Lucas Perez\
ESGI -- Campus Éductive\
Aix-en-Provence
