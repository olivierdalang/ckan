#!/usr/bin/env bash
set -e

echo "----- POST-UPDATE SCRIPT -----"

for REF in "$@"
do

    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    PUSHED_BRANCH=$(git rev-parse --symbolic --abbrev-ref $REF)

    echo "current branch is : $CURRENT_BRANCH"
    echo "you pushed : $PUSHED_BRANCH"

    if [ "$CURRENT_BRANCH" != "$PUSHED_BRANCH" ]; then
        echo "- NOT DEPLOYING -"
    else
        echo "- !!! DEPLOYING !!! -"
        cd ../contrib/docker/
        docker-compose -f docker-compose.yml up --build -d --remove-orphans
    fi
done
