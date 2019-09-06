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

## Déploiement

Toutes les configuration possibles sont listées dans `contrib/docker/.env`.

Le déploiement se fait via `git push` [à la heroku](https://tridnguyen.com/articles/simple-heroku-like-workflow-with-git-and-docker-compose/).

Il faut que la branche poussée corresponde à la branche courante sur le remote.


### Configuration

Sur le VPS :

```
# installer les dépendances
sudo apt-get update

## install docker
wget https://download.docker.com/linux/ubuntu/dists/xenial/pool/stable/amd64/docker-ce_18.06.1~ce~3-0~ubuntu_amd64.deb
sudo dpkg -i docker-ce_18.06.1~ce~3-0~ubuntu_amd64.deb
rm docker-ce_18.06.1~ce~3-0~ubuntu_amd64.deb
sudo usermod -aG docker $USER

## installer docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0-rc2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

## installer git
sudo apt-get install git

# initialiser un repo
git init urbackan
cd urbackan
git checkout -b prod

# configurer le repo
git config receive.denyCurrentBranch updateInstead
touch ./.git/hooks/post-update
chmod +x ./.git/hooks/post-update
```

Créer le script dans `nano ./.git/hooks/post-update`:
```
#!/usr/bin/env bash
set -e

for REF in "$@"
do
    echo "----- POST-UPDATE SCRIPT -----"

    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    PUSHED_BRANCH=$(git rev-parse --symbolic --abbrev-ref $REF)

    echo "current branch is : $CURRENT_BRANCH"
    echo "you pushed : $PUSHED_BRANCH"

    if [ "$CURRENT_BRANCH" != "$PUSHED_BRANCH" ]; then
        echo "- NOT DEPLOYING -"
    else
        echo "- !!! DEPLOYING !!! -"
        cd ../contrib/docker
        docker-compose -f docker-compose.yml up --build -d --remove-orphans
    fi
done
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
