# KENGAN - Plateforme de Duels pour Otakus

![Logo KENGAN](static/img/logo-placeholder.svg)

KENGAN est une plateforme de duels en ligne permettant aux fans d'animes et de mangas de s'affronter dans des quiz de connaissances sur leurs œuvres préférées. Mettez vos connaissances à l'épreuve, montez en niveau, et gagnez des récompenses !

## Table des matières

- [Architecture du Projet](#architecture-du-projet)
- [Prérequis](#prérequis)
- [Installation et Configuration](#installation-et-configuration)
  - [Préparation (Linux/macOS et Windows)](#préparation-linuxmacos-et-windows)
  - [Backend (Django)](#backend-django)
    - [Linux/macOS](#backend---linuxmacos)
    - [Windows](#backend---windows)
  - [Frontend (Vue.js)](#frontend-vuejs)
    - [Linux/macOS et Windows](#frontend---linuxmacos-et-windows)
- [Démarrage des Serveurs](#démarrage-des-serveurs)
  - [Backend](#démarrage-backend)
    - [Linux/macOS](#backend-démarrage---linuxmacos)
    - [Windows](#backend-démarrage---windows)
  - [Frontend](#démarrage-frontend)
- [Accès aux Interfaces](#accès-aux-interfaces)
- [Structure du Projet](#structure-du-projet)
- [Développement](#développement)
- [Résolution des Problèmes](#résolution-des-problèmes)

## Architecture du Projet

Le projet KENGAN est composé de deux parties principales :

- **Backend** : API REST développée avec Django et Django REST Framework, avec PostgreSQL comme base de données et Django Channels pour les WebSockets.
- **Frontend** : Application web développée avec Vue.js, TypeScript, et Tailwind CSS.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

### Linux/macOS

- **Python 3.8+** (`python3 --version` pour vérifier)
- **Node.js 16+** et **npm** (`node --version` et `npm --version` pour vérifier)
- **PostgreSQL 12+** (`psql --version` pour vérifier)
- **Redis** (`redis-cli --version` pour vérifier)
- **Git** (`git --version` pour vérifier)

### Windows

- **Python 3.8+** (vérifier dans PowerShell avec `python --version`)
- **Node.js 16+** et **npm** (vérifier dans PowerShell avec `node --version` et `npm --version`)
- **PostgreSQL 12+** (installer via [le site officiel](https://www.postgresql.org/download/windows/))
- **Redis** (via [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install) ou [Redis Windows](https://github.com/tporadowski/redis/releases))
- **Git** (vérifier dans PowerShell avec `git --version`)

## Installation et Configuration

### Préparation (Linux/macOS et Windows)

#### 1. Cloner les Dépôts

```bash
# Cloner le backend
git clone https://github.com/votre-organisation/kengan-backend.git

# Cloner le frontend
git clone https://github.com/votre-organisation/kengan-frontend.git
```

### Backend (Django)

#### Backend - Linux/macOS

#### 1. Configuration de PostgreSQL

Assurez-vous que PostgreSQL est installé et en cours d'exécution :

```bash
# Installer PostgreSQL (si nécessaire)
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS avec Homebrew
brew install postgresql
brew services start postgresql

# Vérifier le statut
sudo service postgresql status  # Ubuntu/Debian
brew services list | grep postgres  # macOS

# Démarrer si nécessaire
sudo service postgresql start  # Ubuntu/Debian
brew services start postgresql  # macOS
```

#### 2. Configuration de Redis

```bash
# Installer Redis (si nécessaire)
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS avec Homebrew
brew install redis

# Vérifier le statut
sudo service redis-server status  # Ubuntu/Debian
brew services list | grep redis  # macOS

# Démarrer si nécessaire
sudo service redis-server start  # Ubuntu/Debian
brew services start redis  # macOS
```

#### 3. Configuration de l'environnement Django

```bash
# Naviguer vers le répertoire du backend
cd kengan-backend

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer l'utilisateur et la base de données PostgreSQL
sudo -u postgres psql -c "CREATE USER kengan_user WITH PASSWORD 'kengan_password';"
sudo -u postgres psql -c "CREATE DATABASE kengan_db WITH OWNER kengan_user;"
sudo -u postgres psql -c "ALTER USER kengan_user CREATEDB;"

# Exécuter les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur (si non créé par le script)
python manage.py createsuperuser
# ou utiliser admin@kengan.com / admin123 si déjà créé
```

#### Backend - Windows

#### 1. Configuration de PostgreSQL

Assurez-vous que PostgreSQL est installé via [le site officiel](https://www.postgresql.org/download/windows/)

```powershell
# Ouvrir PowerShell en tant qu'administrateur

# Si vous avez installé PostgreSQL avec le chemin par défaut, ajoutez-le au PATH (une seule fois)
$env:Path += ";C:\Program Files\PostgreSQL\14\bin"  # Ajustez le numéro de version selon votre installation

# Connectez-vous à PostgreSQL en tant qu'utilisateur postgres
# Entrez le mot de passe défini lors de l'installation quand demandé
psql -U postgres

# Dans l'invite de commande PostgreSQL, exécutez :
CREATE USER kengan_user WITH PASSWORD 'kengan_password';
CREATE DATABASE kengan_db WITH OWNER kengan_user;
ALTER USER kengan_user CREATEDB;
\q  # Quitter psql
```

#### 2. Configuration de Redis

Options pour Windows :

**Option 1 : via WSL (recommandé)**
```powershell
# Installer WSL si non installé
wsl --install

# Dans votre distribution Linux WSL
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

**Option 2 : Redis pour Windows**
Téléchargez la dernière version depuis [Redis Windows](https://github.com/tporadowski/redis/releases)
```powershell
# Après l'installation, démarrez Redis
Start-Process "C:\Program Files\Redis\redis-server.exe"
```

#### 3. Configuration de l'environnement Django

```powershell
# Naviguer vers le répertoire du backend
cd kengan-backend

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env s'il n'existe pas
if (-not(Test-Path -Path ".env" -PathType Leaf)) {
    @"
DEBUG=True
SECRET_KEY=votre_clé_secrète_longue_et_aléatoire
DATABASE_URL=postgresql://kengan_user:kengan_password@localhost:5432/kengan_db
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://localhost:5173
"@ | Out-File -FilePath ".env" -Encoding utf8
}

# Exécuter les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur (si non créé par le script)
python manage.py createsuperuser
# ou utiliser admin@kengan.com / admin123 si déjà créé
```

### Frontend (Vue.js)

#### Frontend - Linux/macOS et Windows

Les commandes sont identiques pour Linux/macOS et Windows :

```bash
# Naviguer vers le répertoire du frontend
cd kengan-frontend

# Installer les dépendances
npm install

# Créer un fichier .env.local
echo "VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws" > .env.local  # Linux/macOS

# Sur Windows (PowerShell)
# @"
# VITE_API_URL=http://localhost:8000/api
# VITE_WS_URL=ws://localhost:8000/ws
# "@ | Out-File -FilePath ".env.local" -Encoding utf8  # Windows PowerShell
```

## Démarrage des Serveurs

### Démarrage Backend

#### Backend Démarrage - Linux/macOS

```bash
# Naviguer vers le répertoire du backend
cd kengan-backend

# Activer l'environnement virtuel
source venv/bin/activate

# Démarrer le serveur Django
python manage.py runserver
```

#### Backend Démarrage - Windows

```powershell
# Naviguer vers le répertoire du backend
cd kengan-backend

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Démarrer le serveur Django
python manage.py runserver
```

### Démarrage Frontend

Les commandes sont identiques pour Linux/macOS et Windows :

```bash
# Naviguer vers le répertoire du frontend
cd kengan-frontend

# Démarrer le serveur de développement
npm run dev
```

## Accès aux Interfaces

Une fois les serveurs démarrés, vous pouvez accéder aux interfaces suivantes :

### Backend

- **Admin Django** : http://localhost:8000/admin/
  - Utilisateur : `admin@kengan.com`
  - Mot de passe : `admin123` (à changer en production !)
- **Documentation API** : http://localhost:8000/swagger/
- **Documentation API Alternative** : http://localhost:8000/redoc/

### Frontend

- **Application Web** : http://localhost:5173/

## Structure du Projet

### Backend

Le backend est organisé selon l'architecture suivante :

```
kengan-backend/
│
├── apps/                           # Applications Django
│   ├── accounts/                   # Authentification et profils utilisateurs
│   ├── duels/                      # Logique des duels
│   ├── questions/                  # Gestion des questions et catégories
│   ├── wallet/                     # Portefeuille virtuel
│   ├── community/                  # Fonctionnalités sociales
│   ├── ranking/                    # Systèmes de classement
│   ├── notifications/              # Gestion des notifications
│   ├── admin_dashboard/            # Tableau de bord administratif
│   └── core/                       # Fonctionnalités de base
│
├── config/                         # Configuration du projet Django
│   ├── settings/                   # Paramètres Django
│   │   ├── base.py                 # Paramètres communs
│   │   ├── development.py          # Paramètres de développement
│   │   ├── production.py           # Paramètres de production
│   │   └── test.py                 # Paramètres de test
│   ├── urls.py                     # URLs principales
│   ├── wsgi.py                     # Configuration WSGI
│   └── asgi.py                     # Configuration ASGI pour WebSockets
│
├── websockets/                     # Configuration des WebSockets
├── templates/                      # Templates Django (principalement pour emails)
├── static/                         # Fichiers statiques
├── media/                          # Médias téléchargés
├── utils/                          # Utilitaires partagés
├── manage.py                       # Script de gestion Django
├── requirements.txt                # Dépendances Python
└── .env                            # Variables d'environnement
```

### Frontend

Le frontend est organisé selon l'architecture suivante :

```
kengan-frontend/
│
├── public/                           # Fichiers statiques accessibles directement
│
├── src/
│   ├── assets/                       # Ressources compilées par le bundler
│   ├── components/                   # Composants réutilisables
│   │   ├── admin/                    # Composants pour l'espace admin
│   │   ├── ui/                       # Composants UI de base
│   │   ├── landing/                  # Composants landing page
│   │   ├── auth/                     # Composants authentification
│   │   ├── dashboard/                # Composants tableau de bord utilisateur
│   │   ├── profile/                  # Composants profil utilisateur
│   │   ├── wallet/                   # Composants portefeuille
│   │   ├── duel/                     # Composants de duel
│   │   ├── ranking/                  # Composants classement
│   │   ├── community/                # Composants communauté
│   │   └── demo/                     # Composants mode démo
│   │
│   ├── composables/                  # Logique réutilisable (composition API)
│   ├── config/                       # Configuration constantes
│   ├── layouts/                      # Mise en page
│   ├── mock-data/                    # Données mockées dev
│   ├── pages/                        # Pages/vues
│   ├── router/                       # Configuration routeur
│   ├── services/                     # Services API
│   ├── socket/                       # Gestion WebSockets
│   ├── store/                        # Stores Pinia
│   ├── styles/                       # Styles
│   ├── types/                        # Définitions TypeScript
│   ├── utils/                        # Utilitaires
│   │
│   ├── App.vue                       # Composant racine
│   ├── main.ts                       # Point d'entrée JS
│   └── vite-env.d.ts                 # Déclarations types pour Vite
│
├── .env                              # Variables d'environnement
├── .env.development                  # Variables dev
├── .env.production                   # Variables prod
├── index.html                        # Page HTML racine
├── package.json                      # Dépendances et scripts
├── tsconfig.json                     # Config TypeScript
├── vite.config.ts                    # Config Vite
├── tailwind.config.js                # Config Tailwind CSS
└── postcss.config.js                 # Config PostCSS
```

## Développement

### Workflow Git

1. Créez une branche pour chaque nouvelle fonctionnalité ou correction de bug
2. Faites des commits réguliers avec des messages clairs
3. Ouvrez une Pull Request pour la revue de code avant de merger

### Conventions de Code

- **Backend** : Suivez les conventions PEP 8 pour Python
- **Frontend** : Utilisez ESLint et Prettier avec la configuration du projet

### Tests

#### Linux/macOS

```bash
# Tests Backend
cd kengan-backend
source venv/bin/activate
python manage.py test

# Tests Frontend
cd kengan-frontend
npm test
```

#### Windows

```powershell
# Tests Backend
cd kengan-backend
.\venv\Scripts\Activate.ps1
python manage.py test

# Tests Frontend
cd kengan-frontend
npm test
```

## Résolution des Problèmes

### Problèmes PostgreSQL

#### Linux/macOS

Si vous rencontrez des erreurs de connexion à PostgreSQL :

1. Vérifiez le statut du service : `sudo service postgresql status` (Ubuntu/Debian) ou `brew services list | grep postgres` (macOS)
2. Redémarrez si nécessaire : `sudo service postgresql restart` (Ubuntu/Debian) ou `brew services restart postgresql` (macOS)
3. Vérifiez les logs : `sudo tail -f /var/log/postgresql/postgresql-*.log` (Ubuntu/Debian) ou `tail -f /usr/local/var/log/postgres.log` (macOS)

#### Windows

1. Vérifiez que le service PostgreSQL est en cours d'exécution dans les services Windows (`services.msc`)
2. Vérifiez les identifiants dans le fichier `.env`
3. Testez la connexion avec `psql -U kengan_user -d kengan_db`

### Problèmes avec les WebSockets

#### Linux/macOS

1. Vérifiez le statut de Redis : `sudo service redis-server status` (Ubuntu/Debian) ou `brew services list | grep redis` (macOS)
2. Redémarrez si nécessaire : `sudo service redis-server restart` (Ubuntu/Debian) ou `brew services restart redis` (macOS)
3. Testez Redis avec `redis-cli ping` (doit répondre "PONG")

#### Windows

1. Si vous utilisez WSL, vérifiez que Redis est en cours d'exécution dans WSL : `wsl -d Ubuntu sudo service redis-server status`
2. Si vous utilisez Redis pour Windows, vérifiez que le processus est en cours d'exécution
3. Testez Redis avec `redis-cli ping` ou `wsl redis-cli ping` (si WSL)

### Problèmes Frontend

Les solutions sont similaires pour Linux/macOS et Windows :

1. Vérifiez que Node.js et npm sont correctement installés et à jour
2. Nettoyez le cache de npm avec `npm cache clean --force`
3. Supprimez le dossier `node_modules` et réinstallez avec `npm install`

### Problèmes d'environnement virtuel Python

#### Linux/macOS

Si vous avez des problèmes avec l'environnement virtuel :

```bash
# Supprimer et recréer l'environnement virtuel
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows

```powershell
# Supprimer et recréer l'environnement virtuel
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Ressources Supplémentaires

- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation Django REST Framework](https://www.django-rest-framework.org/)
- [Documentation Vue.js](https://vuejs.org/guide/introduction.html)
- [Documentation TypeScript](https://www.typescriptlang.org/docs/)
- [Documentation Tailwind CSS](https://tailwindcss.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)

---

Pour toute question ou problème, contactez l'équipe de développement.
