# Système de Gestion de Lavage Auto

Une application web Django pour la gestion des clients, des souscriptions et des factures pour une entreprise de lavage automobile.

## Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Technologies utilisées](#technologies-utilisées)

## Aperçu

Cette application web permet à une entreprise de lavage automobile de gérer ses clients, de créer des souscriptions (tickets de lavage), de générer des factures et d'analyser les performances commerciales. Elle dispose d'une interface utilisateur intuitive pour les agents et les administrateurs.

## Fonctionnalités

- **Gestion des clients** : Ajout, recherche et consultation des informations clients
- **Gestion des souscriptions** : Création et suivi des tickets de lavage
- **Génération de factures** : Création de factures PDF pour les clients
- **Tableau de bord** : Affichage des statistiques quotidiennes (nouveaux clients, souscriptions)
- **Analytique** : Visualisation des données de lavage par heure et par mois
- **Authentification** : Système de connexion/déconnexion pour les utilisateurs

## Prérequis

- Python 3.8.5 ou supérieur
- Django 5.1.8
- Base de données MySQL ou PostgreSQL
- Autres dépendances listées dans `requirement.txt`

## Installation

1. **Cloner le dépôt**
   ```
   git clone [URL_DU_REPO]
   cd [NOM_DU_DOSSIER]
   ```

2. **Créer un environnement virtuel**
   ```
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Installer les dépendances**
   ```
   pip install -r requirement.txt
   ```

5. **Configurer la base de données**
   - Créer une base de données dans MySQL ou PostgreSQL
   - Configurer les paramètres de connexion dans le fichier de configuration (voir section Configuration)

6. **Appliquer les migrations**
   ```
   python manage.py migrate
   ```

7. **Créer un superutilisateur (administrateur)**
   ```
   python manage.py createsuperuser
   ```

## Configuration

1. **Configuration de la base de données**
   - Ouvrir le fichier `settings.py`
   - Modifier les paramètres de connexion à la base de données:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',  # ou 'django.db.backends.postgresql'
             'NAME': 'nom_de_votre_base_de_donnees',
             'USER': 'votre_utilisateur',
             'PASSWORD': 'votre_mot_de_passe',
             'HOST': 'localhost',
             'PORT': '3306',  # '5432' pour PostgreSQL
         }
     }
     ```

2. **Variables d'environnement (optionnel)**
   - Créer un fichier `.env` à la racine du projet
   - Définir les variables d'environnement sensibles (clés secrètes, identifiants de base de données, etc.)

## Utilisation

1. **Lancer le serveur de développement**
   ```
   python manage.py runserver
   ```

2. **Accéder à l'application**
   - Ouvrir un navigateur web
   - Accéder à l'URL: `http://localhost:8000`

3. **Se connecter à l'application**
   - Utiliser les identifiants du superutilisateur créé précédemment
   - Ou créer un nouvel utilisateur via l'interface d'administration

4. **Fonctionnalités principales**
   - **Ajouter un client**: Cliquer sur "Add Customer" dans le menu latéral
   - **Créer une souscription**: Cliquer sur "Add subscription" dans le menu latéral
   - **Rechercher un client**: Utiliser la barre de recherche sur la page d'accueil
   - **Consulter les analytics**: Cliquer sur "Analytics" dans le menu latéral

## Structure du projet

```
projet/
├── system/                 # Application principale
│   ├── models.py           # Modèles de données
│   ├── views.py            # Vues et logique métier
│   ├── urls.py             # Configuration des URLs
│   └── forms.py            # Formulaires
├── templates/              # Templates HTML
│   ├── base.html           # Template de base
│   ├── home.html           # Page d'accueil
│   ├── login.html          # Page de connexion
│   └── analytics.html      # Page d'analytique
├── static/                 # Fichiers statiques (CSS, JS, images)
├── manage.py               # Script de gestion Django
└── requirement.txt         # Liste des dépendances
```

## Technologies utilisées

- **Backend**:
  - Django 5.1.8 (framework web Python)
  - Django REST Framework (API REST)
  - Celery (tâches asynchrones, si utilisé)

- **Frontend**:
  - Bootstrap (framework CSS)
  - jQuery (bibliothèque JavaScript)
  - Chart.js (visualisation de données)
  - Font Awesome (icônes)

- **Base de données**:
  - MySQL ou PostgreSQL

- **Autres**:
  - FPDF / xhtml2pdf (génération de PDF)
  - Django Crispy Forms (amélioration des formulaires)