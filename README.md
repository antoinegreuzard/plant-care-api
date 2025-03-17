# 🚀 Plant Care API

Une API Django pour gérer des ressources avec Django REST Framework.

## 📦 Installation

1. **Cloner le projet**
   ```sh
   git clone https://github.com/antoinegreuzard/plant-care-api
   cd plant-care-api
   ```

2. **Créer un environnement virtuel et installer les dépendances**
   ```sh
   python -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurer la base de données**
   ```sh
   python manage.py migrate
   ```

4. **Lancer le serveur**
   ```sh
   python manage.py runserver
   ```

L'API est accessible sur `http://127.0.0.1:8000/api/`.

---

## 📡 Endpoints de l'API

| Méthode  | Endpoint           | Description                  |
|----------|--------------------|------------------------------|
| `GET`    | `/api/items/`      | Récupérer tous les items     |
| `POST`   | `/api/items/`      | Créer un item                |
| `GET`    | `/api/items/{id}/` | Récupérer un item spécifique |
| `PUT`    | `/api/items/{id}/` | Modifier un item             |
| `DELETE` | `/api/items/{id}/` | Supprimer un item            |

---

## ⚙️ Test avec Docker

1. **Construire et lancer le conteneur**
   ```sh
   docker-compose up --build
   ```

2. **Tester avec `curl`**
   ```sh
   curl -X GET http://127.0.0.1:8000/api/items/
   ```

---

## 🛠 CI/CD avec GitHub Actions

Ce projet utilise GitHub Actions pour vérifier automatiquement :

- L’installation des dépendances
- La qualité du code avec `flake8`
- Les tests unitaires Django avec une base PostgreSQL

---

## 📜 Licence

Ce projet est sous licence MIT. 📝
