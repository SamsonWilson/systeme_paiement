# 1. Image de base légère
FROM python:3.9-slim

# 2. Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# 4. Définir le répertoire de travail
WORKDIR /app

# 5. Copier uniquement le fichier requirements.txt
COPY requirements.txt ./

# 6. Mettre à jour pip et installer les dépendances Python
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copier le reste du code de l’application
COPY . .
