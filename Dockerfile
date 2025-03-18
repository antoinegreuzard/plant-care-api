# Utiliser une image officielle de Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier uniquement les fichiers nécessaires pour installer les dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet (y compris config/ et api/)
COPY . .

# Vérifier le contenu du dossier pour voir si config/ existe bien
RUN ls -la /app

# Exposer le port 8000
EXPOSE 8000

# Appliquer les migrations avant de démarrer
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
