# Gestion des tâches

Application web de gestion de tâches développée avec Django (Python).

## Architecture

L'application est organisée autour de 3 modèles principaux :

- **User** : utilisateur avec email comme identifiant, peut faire partie d'une équipe, créer ou recevoir des tâches
- **Team** : une équipe avec un nom, des membres et un créateur. Les membres peuvent rejoindre ou quitter librement
- **Task** : chaque tâche a un titre, une description, un statut, et peut être privée. Elle peut être assignée à des utilisateurs ou des équipes. Les sous-tâches sont aussi supportées

Des formulaires permettent l'inscription avec choix ou création d'équipe, et la création de tâches avec assignation. Les vues sont protégées avec `@login_required`.

## Installation

```bash
# Créer et activer l'environnement virtuel
python3 -m venv tp-env
source tp-env/bin/activate

# Installer Django
python -m pip install Django

# Appliquer les migrations
python3 manage.py makemigrations tasks
python3 manage.py migrate

# Lancer le serveur
python3 manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000 dans le navigateur.

## Fonctionnement

- À l'arrivée sur le site, vous pouvez vous connecter ou vous inscrire
- Après l'inscription, vous êtes connecté automatiquement
- On conseille de tester avec deux comptes (ex: Chrome + Edge) pour tester les tâches privées
- Une tâche **privée** est visible uniquement par son créateur
- Une tâche **publique** est visible par tous les utilisateurs et équipes assignés
- Une étoile identifie les tâches que vous avez créées dans la liste

## Technologies

- Python / Django
- SQLite
- HTML / CSS
