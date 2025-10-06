# Fichier : Dockerfile

# 1. Utiliser une image "slim" qui est plus légère
FROM python:3.9-slim

# 2. Définir des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Mettre à jour apt et installer les dépendances système nécessaires
# (build-essential et default-libmysqlclient-dev sont souvent requis pour mysqlclient)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    # Nettoyer le cache apt pour réduire la taille de l'image
    && rm -rf /var/lib/apt/lists/*

# 4. Définir le répertoire de travail
WORKDIR /app

# 5. Copier UNIQUEMENT le fichier des dépendances
# C'est la clé de l'optimisation ! Si ce fichier ne change pas, Docker n'exécutera pas l'étape suivante.
COPY requirements.txt .

# 6. Installer les dépendances Python
RUN pip install -r requirements.txt

# 7. Copier tout le reste de votre projet
COPY . .