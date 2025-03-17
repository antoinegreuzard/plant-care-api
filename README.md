# 🚀 Plant Care API

Une API Django pour gérer un catalogue personnalisé de plantes avec des fonctionnalités avancées comme un calendrier d'entretien automatisé et un journal de suivi visuel.

---

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

4. **Créer un superutilisateur (optionnel)**
   ```sh
   python manage.py createsuperuser
   ```

5. **Lancer le serveur**
   ```sh
   python manage.py runserver
   ```

L'API est accessible sur `http://127.0.0.1:8000/api/`.

---

## 📡 Endpoints de l'API

### 🌿 Gestion des plantes

| Méthode  | Endpoint            | Description                     |
|----------|---------------------|---------------------------------|
| `GET`    | `/api/plants/`      | Récupérer toutes les plantes    |
| `POST`   | `/api/plants/`      | Ajouter une nouvelle plante     |
| `GET`    | `/api/plants/{id}/` | Récupérer une plante spécifique |
| `PUT`    | `/api/plants/{id}/` | Modifier une plante existante   |
| `DELETE` | `/api/plants/{id}/` | Supprimer une plante            |

### 📷 Suivi visuel des plantes

| Méthode | Endpoint                         | Description                       |
|---------|----------------------------------|-----------------------------------|
| `POST`  | `/api/plants/{id}/upload-photo/` | Ajouter une photo à une plante    |
| `GET`   | `/api/plants/{id}/photos/`       | Récupérer les photos d’une plante |

### 🔔 Rappels et notifications d'entretien

| Méthode | Endpoint                      | Description                           |
|---------|-------------------------------|---------------------------------------|
| `GET`   | `/api/plants/{id}/reminders/` | Récupérer les prochains entretiens    |
| `POST`  | `/api/plants/send-reminders/` | Envoyer des rappels par email (Admin) |

### 📝 Conseils d’entretien personnalisés

| Méthode | Endpoint                   | Description                        |
|---------|----------------------------|------------------------------------|
| `GET`   | `/api/plants/{id}/advice/` | Obtenir des conseils personnalisés |

---

## ⚙️ Test avec Docker

1. **Construire et lancer le conteneur**
   ```sh
   docker-compose up --build
   ```

2. **Tester avec `curl`**
   ```sh
   curl -X GET http://127.0.0.1:8000/api/plants/
   ```

---

## 🛠 CI/CD avec GitHub Actions

Ce projet utilise **GitHub Actions** pour automatiser :

- L’installation des dépendances
- La qualité du code avec `flake8`
- Les tests unitaires Django avec une base PostgreSQL

---

## 📜 Licence

Ce projet est sous licence **MIT**. 📝
