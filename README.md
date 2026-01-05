# tourism-france-dashboard
# 🏖️ Tourisme International en France - Dashboard d'Analyse

**Projet de Data Science - ESIEE Paris**

Dashboard interactif d'analyse du tourisme international en France basé sur des données Open Data. Ce projet permet de visualiser les flux touristiques, leur origine géographique et leur impact économique pour éclairer les décideurs publics et les acteurs du secteur touristique.

---

## 📋 Table des matières

- [User Guide](#-user-guide)
- [Data](#-data)
- [Developer Guide](#-developer-guide)
- [Rapport d'Analyse](#-rapport-danalyse)
- [Copyright](#-copyright)

---

##  User Guide

### Prérequis

- **Python 3.8+** installé sur votre machine
- **pip** pour la gestion des packages Python
- **Navigateur web** moderne (Chrome, Firefox, Edge, Safari)

### Installation

#### 1. Cloner le dépôt

```bash
git clone https://github.com/PapabassirouDiop/tourism-france-dashboard.git
cd tourism-france-dashboard
```

#### 2. Créer un environnement virtuel (recommandé)

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### Préparation des données

Avant le premier lancement, nettoyez les données brutes :

```bash
python src/utils/clean_data.py
```

Cette étape :
- Lit les fichiers CSV du dossier `data/raw/`
- Supprime les doublons
- Convertit les colonnes numériques
- Sauvegarde les données nettoyées dans `data/cleaned/`

### Lancement du dashboard

```bash
python app.py
```

Le dashboard sera accessible à l'adresse : **http://localhost:8050**

### Utilisation du dashboard

#### Navigation

Le dashboard comporte **4 pages principales** accessibles via les onglets en haut :

1. **🏠 Accueil** : Vue d'ensemble et contexte du projet
2. **🗺️ Régions** : Cartes interactives des flux touristiques
3. **🌍 International** : Analyse détaillée par pays
4. **💼 Économie** : Impact économique et retombées

#### Fonctionnalités interactives

**Filtres disponibles :**
- **Période temporelle** : Sélectionnez date de début et date de fin
- **Région d'origine** : Filtrez par continent/région du monde
- **Année** : Filtrez par année spécifique
- **Indicateurs** : Choisissez entre touristes, nuitées ou durée de séjour

**Interactions avec les graphiques :**
- **Survol** : Passez la souris sur les éléments pour voir les détails
- **Zoom** : Utilisez la molette ou les boutons +/- sur les cartes
- **Déplacement** : Cliquez-glissez pour déplacer les cartes
- **Sélection multiple** : Utilisez les dropdowns pour comparer plusieurs pays/régions
- **Export** : Téléchargez les données filtrées en CSV (bouton disponible dans certaines sections)

#### Arrêt du dashboard

Pour arrêter le serveur, appuyez sur `Ctrl+C` dans le terminal.

---

## 📊 Data

### Source des données

**Type** : Données Open Data publiques  
**Source** : Statistiques officielles de fréquentation touristique en France  
**Période couverte** : 2024-2025  
**Licence** : Données publiques librement réutilisables  

### Structure des données

Le projet utilise **3 fichiers CSV** :

#### 1. `frequentation_mensuelle.csv`
Fréquentation touristique agrégée par mois

| Colonne | Type | Description |
|---------|------|-------------|
| Mois | Date | Mois de la fréquentation (format YYYY-MM-DD) |
| Nombre de touristes | Integer | Nombre total de touristes (en milliers) |
| Nombre de croisièristes | Integer | Nombre de croisiéristes (en milliers) |
| Nuitées touristiques | Integer | Nombre total de nuitées (en milliers) |
| Durée de séjour moyenne | Float | Durée moyenne de séjour (en jours) |

#### 2. `frequentation_region.csv`
Fréquentation détaillée par région d'origine et pays

| Colonne | Type | Description |
|---------|------|-------------|
| Mois | Date | Mois de la fréquentation |
| Region | String | Région du monde (Europe, Asie, Amérique du Nord, etc.) |
| Pays | String | Pays d'origine des touristes |
| Nombre de touristes | Integer | Nombre de touristes de ce pays (en milliers) |
| Nombre de croisièristes | Integer | Nombre de croisiéristes (en milliers) |
| Nuitées touristiques | Integer | Nombre de nuitées générées (en milliers) |
| Durée de séjour moyenne | Float | Durée moyenne de séjour (en jours) |

#### 3. `frequentation_hoteliere.csv`
Fréquentation hôtelière avec codes ISO3

| Colonne | Type | Description |
|---------|------|-------------|
| Année | Integer | Année de référence |
| Region | String | Région du monde |
| Pays | String | Pays d'origine |
| ISO3 | String | Code ISO3 du pays (pour cartographie) |
| Nombre de touristes | Integer | Nombre de touristes (en milliers) |
| Nombre de croisièristes | Integer | Nombre de croisiéristes (en milliers) |
| Nuitées touristiques | Integer | Nombre de nuitées (en milliers) |
| Durée de séjour moyenne | Float | Durée moyenne de séjour (en jours) |

### Traitement des données

**Pipeline de nettoyage** (`src/utils/clean_data.py`) :
1. Lecture des fichiers CSV bruts
2. Suppression des doublons
3. Conversion des colonnes numériques (remplacement virgule → point)
4. Gestion des valeurs manquantes
5. Sauvegarde des données nettoyées

**Chargement des données** (`src/utils/load_cleaned_data.py`) :
- Lecture des fichiers nettoyés
- Vérification de la cohérence des colonnes
- Retour d'un dictionnaire avec les 3 DataFrames

### Indicateurs calculés

- **Intensité économique** : Nuitées totales / Nombre de touristes
- **Volume total** : Somme des arrivées sur la période
- **Durée moyenne pondérée** : Moyenne des durées de séjour

---

##  Developer Guide

### Architecture du code

```
tourism-france-dashboard/
├── app.py                          # Point d'entrée principal de l'application
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation
│
├── data/
│   ├── raw/                        # Données brutes (non versionnées si volumineuses)
│   │   ├── frequentation_mensuelle.csv
│   │   ├── frequentation_region.csv
│   │   └── frequentation_hoteliere.csv
│   └── cleaned/                    # Données nettoyées (générées automatiquement)
│       ├── frequentation_mensuelle_cleaned.csv
│       ├── frequentation_region_cleaned.csv
│       └── frequentation_hoteliere_cleaned.csv
│
└── src/
    ├── layouts/                    # Layouts des pages du dashboard
    │   ├── __init__.py
    │   ├── home_layout.py          # Page d'accueil
    │   ├── regional_layout.py      # Page Régions avec cartes
    │   ├── international_layout.py # Page International
    │   └── economic_layout.py      # Page Économie
    │
    └── utils/                      # Utilitaires
        ├── clean_data.py           # Script de nettoyage des données
        └── load_cleaned_data.py    # Chargement des données nettoyées
```

### Technologies utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.8+ | Langage de programmation |
| Dash | 2.14.0 | Framework web pour dashboards |
| Plotly | 5.18.0 | Visualisations interactives |
| Pandas | 2.1.4 | Manipulation de données |
| Dash Bootstrap Components | 1.5.0 | Composants UI stylisés |

### Structure de l'application Dash

#### `app.py` - Application principale

```python
# Initialisation de l'application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout principal avec navigation par onglets
app.layout = dbc.Container([...])

# Callback principal pour la navigation
@app.callback(Output('page-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    # Rendu de la page selon l'onglet sélectionné
    ...
```

#### Layouts - Pages individuelles

Chaque page suit cette structure :

```python
def create_layout(df_dict):
    """
    Crée le layout de la page
    
    Args:
        df_dict (dict): Dictionnaire contenant les DataFrames
        
    Returns:
        dbc.Container: Layout Dash de la page
    """
    # Construction du layout avec composants Dash
    layout = dbc.Container([...])
    return layout

def register_callbacks(app, df_dict):
    """
    Enregistre les callbacks pour l'interactivité
    
    Args:
        app: Instance de l'application Dash
        df_dict (dict): Dictionnaire des DataFrames
    """
    @app.callback(...)
    def update_chart(...):
        # Logique de mise à jour des graphiques
        ...
```

### Ajouter une nouvelle page

#### Étape 1 : Créer le fichier layout

Créez `src/layouts/nouvelle_page_layout.py` :

```python
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def create_layout(df_dict):
    """Crée le layout de la nouvelle page"""
    
    df = df_dict["frequentation_region"]  # Choisir le DataFrame
    
    layout = dbc.Container([
        html.H2("Titre de la nouvelle page"),
        
        # Ajouter vos composants (graphiques, filtres, etc.)
        dcc.Graph(id='mon-graphique'),
        
        # Ajouter des filtres
        dcc.Dropdown(id='mon-filtre', options=[...])
    ])
    
    return layout

def register_callbacks(app, df_dict):
    """Enregistre les callbacks"""
    
    @app.callback(
        Output('mon-graphique', 'figure'),
        Input('mon-filtre', 'value')
    )
    def update_graph(filtre_value):
        # Logique de mise à jour
        df = df_dict["frequentation_region"]
        
        # Filtrer les données
        df_filtered = df[df['Region'] == filtre_value]
        
        # Créer le graphique
        fig = px.bar(df_filtered, x='Pays', y='Nombre de touristes')
        
        return fig
```

#### Étape 2 : Importer dans `app.py`

```python
# Ajouter l'import
from src.layouts import nouvelle_page_layout

# Ajouter l'onglet dans le layout
dcc.Tab(label='🆕 Nouvelle Page', value='nouvelle_page')

# Ajouter le cas dans le callback de navigation
elif tab == 'nouvelle_page':
    return nouvelle_page_layout.create_layout(df_dict)

# Enregistrer les callbacks
nouvelle_page_layout.register_callbacks(app, df_dict)
```

### Ajouter un nouveau graphique

#### Dans le layout :

```python
# Ajouter le composant Graph
dcc.Graph(id='nouveau-graphique')
```

#### Dans les callbacks :

```python
@app.callback(
    Output('nouveau-graphique', 'figure'),
    Input('filtre-existant', 'value')
)
def update_nouveau_graphique(filtre_value):
    # Récupérer les données
    df = df_dict["frequentation_region"]
    
    # Filtrer si nécessaire
    df_filtered = df[df['Region'] == filtre_value]
    
    # Créer le graphique Plotly
    fig = px.scatter(
        df_filtered,
        x='Nombre de touristes',
        y='Durée de séjour moyenne',
        color='Pays',
        size='Nuitées touristiques',
        title="Mon nouveau graphique"
    )
    
    return fig
```

### Types de graphiques disponibles (Plotly Express)

```python
# Histogramme
px.bar(df, x='colonne_x', y='colonne_y')

# Courbe temporelle
px.line(df, x='Mois', y='Nombre de touristes', color='Region')

# Scatter plot
px.scatter(df, x='col_x', y='col_y', size='col_size', color='col_color')

# Carte choroplèthe
px.choropleth(df, locations='ISO3', color='indicateur')

# Carte avec marqueurs
px.scatter_geo(df, lat='lat', lon='lon', size='valeur', color='categorie')

# Graphique circulaire
px.pie(df, values='valeurs', names='categories')

# Boîte à moustaches
px.box(df, x='categorie', y='valeur')
```

### Bonnes pratiques

1. **Nommage des IDs** : Utilisez des préfixes par page (`regional-`, `intl-`, `eco-`)
2. **Documentation** : Ajoutez des docstrings à toutes les fonctions
3. **Gestion des erreurs** : Utilisez `try-except` pour les opérations critiques
4. **Performance** : Utilisez `@app.callback` avec `prevent_initial_call=True` si nécessaire
5. **Lisibilité** : Gardez les callbacks courts et focalisés sur une tâche

### Debugging

Pour activer le mode debug :

```python
# Dans app.py
app.run_server(debug=True)
```

Le mode debug permet :
- Rechargement automatique lors des modifications
- Messages d'erreur détaillés
- Interface de débogage interactive

---

## 📈 Rapport d'Analyse

### Contexte et objectif

Ce dashboard répond à un enjeu d'**intérêt public** : optimiser l'attractivité touristique de la France en comprenant les flux de touristes internationaux, leur origine géographique et leur impact économique.

Les **questions principales** éclairées par cette analyse sont :
1. D'où viennent les touristes qui visitent la France ?
2. Quelle est l'évolution temporelle de ces flux ?
3. Quel est l'impact économique réel par marché ?
4. Quelles stratégies adopter pour maximiser les retombées ?

### Principales conclusions

#### 1. 🌍 Géographie des flux touristiques

**Constat** :
- L'**Europe** domine largement avec plus de 60% des arrivées internationales
- L'**Amérique du Nord** (USA, Canada) représente le 2ème marché avec ~15% des flux
- L'**Asie** est en croissance mais reste sous-représentée (~10%)

**Insight stratégique** :
> **Opportunité** : L'Asie (Chine, Inde, Japon) représente un potentiel de croissance majeur. Malgré leur population importante, ces pays génèrent relativement peu de touristes vers la France. Une campagne marketing ciblée pourrait significativement augmenter les flux.

#### 2. 📊 Impact économique par marché

**Intensité économique** (ratio nuitées/touriste) :

| Marché | Intensité | Interprétation |
|--------|-----------|----------------|
| Australie, Brésil, Japon | >15 nuitées/touriste | 🟢 Très rentables - longue durée |
| Europe de l'Ouest | 8-12 nuitées/touriste | 🟡 Bon équilibre volume/durée |
| USA, Chine | 5-8 nuitées/touriste | 🟠 Fort volume mais séjours courts |

**Insight stratégique** :
> **Action prioritaire** : Les touristes américains et chinois représentent un volume élevé mais des séjours courts. Créer des **packages multi-destinations** (Paris + Provence + Côte d'Azur) pourrait allonger leur durée de séjour de 30-40%, générant des millions de nuitées supplémentaires.

#### 3. ⏱️ Saisonnalité et tendances temporelles

**Observations** :
- **Pics de fréquentation** : Juillet-Août (saison estivale)
- **Creux** : Novembre-Février (hors fêtes de fin d'année)
- **Tendance 2024-2025** : Croissance de +8% par rapport à l'année précédente

**Insight stratégique** :
> **Recommandation** : Développer une stratégie **hors-saison** avec des tarifs attractifs et des événements culturels en automne/hiver. Cela permettrait de lisser les flux, réduire la pression sur les infrastructures en été, et maximiser l'occupation annuelle.

#### 4. 🎯 Segmentation des marchés (Matrice Volume vs Durée)

**Quadrant 1 - Haute priorité** (Volume élevé + Longue durée) :
- Allemagne, Royaume-Uni, Benelux
- **Action** : Fidéliser ces marchés matures avec des programmes de fidélité

**Quadrant 2 - Développer** (Faible volume + Longue durée) :
- Australie, Brésil, Japon
- **Action** : Investir en marketing pour augmenter le volume tout en conservant la durée

**Quadrant 3 - Optimiser** (Volume élevé + Courte durée) :
- USA, Chine
- **Action** : Allonger les séjours avec des packages attractifs

**Quadrant 4 - Basse priorité** (Faible volume + Courte durée) :
- Marchés émergents
- **Action** : Surveiller l'évolution mais pas d'investissement majeur immédiat

### Recommandations stratégiques

#### Pour Atout France (marketing)

1. **Budget marketing** : Prioriser Chine et Inde (marchés émergents à fort potentiel)
2. **Campagnes ciblées** : 
   - USA/Chine → Packages multi-destinations
   - Japon/Australie → Expériences premium longue durée
3. **Partenariats** : Nouer des accords avec compagnies aériennes asiatiques

#### Pour les collectivités territoriales

1. **Infrastructures** : Renforcer signalétique multilingue (chinois, japonais)
2. **Transports** : Liaisons aéroportuaires vers marchés prioritaires
3. **Services publics** : Anticiper les pics estivaux avec effectifs renforcés

#### Pour les acteurs économiques (hôtellerie, restauration)

1. **Adaptation de l'offre** :
   - Petits-déjeuners adaptés aux clientèles asiatiques
   - Services en mandarin/japonais dans les zones touristiques
2. **Stratégie tarifaire** : Promotions hors-saison pour attirer volume
3. **Formation** : Personnel formé aux codes culturels des marchés clés

### Méthodologie d'analyse

- **Données** : 1 993 lignes × 7 colonnes (fréquentation régionale)
- **Période** : 18 mois (2024-2025)
- **Méthodes** : Agrégations, calculs d'intensité économique, segmentation par quadrants
- **Outils** : Python (Pandas), Plotly pour visualisations interactives

---

## 📜 Copyright

### Déclaration d'originalité

Je déclare sur l'honneur que le code fourni a été produit par moi-même, **à l'exception des éléments suivants** :

#### Frameworks et bibliothèques utilisés

- **Dash** (Plotly) : Framework Python pour dashboards web - Licence MIT
  - Documentation : https://dash.plotly.com/
  - Utilisation : Structure de l'application, callbacks, composants

- **Plotly** : Bibliothèque de visualisation interactive - Licence MIT
  - Documentation : https://plotly.com/python/
  - Utilisation : Graphiques interactifs (choroplèthes, scatter, bar, line)

- **Pandas** : Bibliothèque de manipulation de données - Licence BSD
  - Documentation : https://pandas.pydata.org/
  - Utilisation : Traitement et agrégation des données

- **Dash Bootstrap Components** : Composants UI pour Dash - Licence MIT
  - Documentation : https://dash-bootstrap-components.opensource.faculty.ai/
  - Utilisation : Layout responsive et composants stylisés

#### Mapping des codes ISO3

Le dictionnaire de mapping pays → codes ISO3 (`iso3_mapping` dans `regional_layout.py` et `international_layout.py`) utilise des codes standards définis par la norme ISO 3166-1 alpha-3.

Source : Organisation internationale de normalisation (ISO)

#### Coordonnées géographiques des régions

Les coordonnées approximatives des centres géographiques des régions du monde (`coords_regions` dans `regional_layout.py`) sont basées sur des valeurs géographiques standards.

#### Inspiration pour la structure

L'architecture modulaire du code (séparation layouts/callbacks) s'inspire des bonnes pratiques recommandées dans la documentation officielle de Dash :
- https://dash.plotly.com/urls
- https://dash.plotly.com/sharing-data-between-callbacks

### Tout le reste du code est original

- Architecture spécifique du dashboard
- Logique métier et agrégations de données
- Callbacks et interactions personnalisées
- Choix de visualisations et design
- Analyses et insights du rapport

**Date** : [""]  
**Auteur** : Papa Bassirou Diop  
**Promotion** : ESIEE Paris - 2025/2026
---

## 📧 Contact

Pour toute question concernant ce projet :
- **Email** : [papabassirou.diop@edu.esiee.fr]
- **GitHub** : [https://github.com/PapabassirouDiop]

---

**🎓 Projet réalisé dans le cadre du cours de EPIGEP-FI-3-S1-UPM-Python-visualisation-données - ESIEE Paris**
