# UrbaCKAN

Prototype de base de documentation ckan.urbasen.org.

## Installation

(Tiré de https://docs.ckan.org/en/2.8/maintaining/installing/install-from-docker-compose.html)

```
cd contrib/docker

# Configurer
cp .env.template .env
nano .env

# Préparer le stack
docker-compose build
# pip install sur le volume monté (et constater la création de ckan.egg-info):
docker-compose run --entrypoint="" ckan ckan-pip install -e /usr/lib/ckan/venv/src/ckan/

# Lancer le stack
docker-compose up --build -d
```

## Dev

### i18n

```
docker-compose exec ckan bash -c '
  cd /usr/lib/ckan/venv/src/ckan/ && \
  source $CKAN_VENV/bin/activate && \
  python setup.py compile_catalog --use-fuzzy --locale fr
'
```


## Déploiement

Toutes les configuration possibles sont listées dans `contrib/docker/.env`.

Le déploiement se fait via `git push` [à la heroku](https://tridnguyen.com/articles/simple-heroku-like-workflow-with-git-and-docker-compose/).

Il faut que la branche poussée corresponde à la branche courante sur le remote.


### Configuration

Sur le VPS :

```
# installer les dépendances
sudo apt-get update
sudo apt-get install docker.io docker-compose git

# initialiser un repo
git init urbackan
cd urbackan
git checkout -b prod

# configurer le repo
git config receive.denyCurrentBranch updateInstead
ln -s ../../git-deploy.sh ./.git/hooks/post-update
```

Sur votre machine :
```
# ajouter le remote (voir settings sur jelastics)
git remote add prod ssh://14785-1164@gate.jpe.infomaniak.com:3022/root/urbackan

# créer la branche
git checkout -b prod
```

### Déploiement

Pusher la branche vers "prod" :
```
git push MY_REMOTE prod
```

### Restauration

Pour importer des données d'un dump existant, exectuer (compter >60s) :

```
docker exec -it db bash -c "
    apt-get update && apt-get install -y wget &&
    wget https://www.dropbox.com/s/0sou03qbwwiyfia/ckan.custom?dl=1 -O ckan.custom &&
    psql -U ckan -d postgres -c 'select pg_terminate_backend(pg_stat_activity.pid) from pg_stat_activity where pid <> pg_backend_pid();' &&
    psql -U ckan -d postgres -c 'drop database if exists ckan;' &&
    pg_restore -U ckan -d postgres -c -C /ckan.custom &&
    rm /ckan.custom
"
```

Pour importer les fichiers :

```
docker-compose run --entrypoint="" backup rclone copy -v MYDROPBOX:/99_Backup/ckan/ckan_storage/ /backups/ckan_storage/
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
