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
# update catalog
docker-compose exec ckan bash -c '
  cd /usr/lib/ckan/venv/src/ckan/ && \
  source $CKAN_VENV/bin/activate && \
  python setup.py init_catalog --locale en -w 78
'

# batch rename groupe->projet
docker-compose exec ckan bash -c '
  cd /usr/lib/ckan/venv/src/ckan/ && \
  source $CKAN_VENV/bin/activate && \
  python scripts/batch_update_locale_for_customization.py
'

# compile
docker-compose exec ckan bash -c '
  cd /usr/lib/ckan/venv/src/ckan/ && \
  source $CKAN_VENV/bin/activate && \
  python setup.py compile_catalog --locale fr && \
  python setup.py compile_catalog --locale en
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
    wget https://www.dropbox.com/s/ygyk436m9uo3bxr/ckan.custom?dl=1 -O ckan.custom &&
    psql -U ckan -d postgres -c 'select pg_terminate_backend(pg_stat_activity.pid) from pg_stat_activity where pid <> pg_backend_pid();' &&
    psql -U ckan -d postgres -c 'drop database if exists ckan;' &&
    pg_restore -U ckan -d postgres -c -C /ckan.custom &&
    rm /ckan.custom
"
```

Pour importer les fichiers :

```
docker-compose run --entrypoint="" backup rclone copy -v MYDROPBOX:/99_Backup/ckan/ckan_storage/ /backups/ckan_storage/
# update permissions for ckan user
docker-compose run --entrypoint="" backup chown -R 900 /backups/ckan_storage/
```

## À faire

### Déploiement

- utiliser `uwsgi` (ou autre) à la place de `paster server` (https://github.com/ckan/ckan/issues/4893)
- probablement nécessaire de faire tourner un worker celery (full-text search)
- meilleur gestion de la config production (https://github.com/ckan/ckan/issues/4894)

### Traductions

- quelques traductions importantes manquent (e.g. `Issu de l'abstract du jeu de données`)

### Extensions

- ckanext-extractor : full-text search (pdfs...)
- ckanext-restricted : permettre de restreindre des resources (on voit que metadata)
- ckanext-spatial : classification spatiale

### Notifications

- configurer "enable notification" sur on par défault

### Hacks

- modifier ckanext-ytd-comments pour l'insérer dans le flux d'activité (et donc notifications)

### Guide de publication

- licenses : qu'est-ce qu'on utilise
- visibilité des données

## Notes

### COG (Geotiffs)

Les Geotiffs sont supportés grâce à une modification du plugin geoview.

Créer un COG (dans le OSGeo4W shell):
```
# vérifier la version de GDAL
gdalinfo --version
# si la version est inférieure à 3.1 :
gdal-dev-env
# revérifier, puis lancer la commande suivante en remplaçant FICHIER_ENTREE par le nom du tiff en entrée, et FICHIER_SORTIE par le nom du tiff en sortie
gdal_translate FICHIER_ENTREE.tif FICHIER_SORTIE.tif -of COG -co TILING_SCHEME=GoogleMapsCompatible -co COMPRESS=JPEG
```

Tester le COG (dans le OSGeo4W shell):
```
py3_env
curl https://raw.githubusercontent.com/OSGeo/gdal/master/gdal/swig/python/samples/validate_cloud_optimized_geotiff.py -O validate_cog.py
python validate_cog.py FICHIER_SORTIE.tif
# ça doit écrire `FICHIER_SORTIE is a valid cloud optimized GeoTIFF`
```
