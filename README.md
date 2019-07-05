# UrbaCKAN

Prototype de base de documentation ckan.urbasen.org.

## Installation

(Tiré de https://docs.ckan.org/en/2.8/maintaining/installing/install-from-docker-compose.html)

```
cd contrib/docker

# Configurer
cp .env.template .env
nano .env

# Lancer le stack
docker-compose up --build -d

# Configurer CKAN
docker-compose exec ckan vim /etc/ckan/production.ini
docker-compose restart ckan
```

## À faire

### Déploiement

- backups
- utiliser `uwsgi` (ou autre) à la place de `paster server` (https://github.com/ckan/ckan/issues/4893)
- probablement nécessaire de faire tourner un worker celery (full-text search)
- meilleur gestion de la config production (https://github.com/ckan/ckan/issues/4894)

### Customization

- home page (image, couleurs...)

### Traductions

- quelques traductions importantes manquent (e.g. `Issu de l'abstract du jeu de données`)

### Extensions

- ckanext-extractor : full-text search (pdfs...)
- ckanext-pdfview : PDF preview

### Guide de publication

- licenses : qu'est-ce qu'on utilise
- visibilité des données
