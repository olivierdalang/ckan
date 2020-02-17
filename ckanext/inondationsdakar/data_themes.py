# encoding: utf-8

import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

LIST = [
    u"Cadre institutionnel et réglementaire",
    u"Causes des inondations",
    u"État actuel des inondations",
    u"Solutions génériques",
    u"Projets et plans de développement",
]

def create_themes():
    '''Create themes vocab and tags, if they don't exist already.

    Note that you could also create the vocab and tags using CKAN's API,
    and once they are created you can edit them (e.g. to add and remove
    possible dataset country code values) using the API.

    Voir les vocabulaire : https://127.0.0.1/api/3/action/vocabulary_list
    Supprimer le vocabulaire (/!\ on perd assignation !)

    '''
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'themes'}
        tk.get_action('vocabulary_show')(context, data)
        logging.info("Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        logging.info("Creating vocab 'themes'")
        data = {'name': 'themes'}
        vocab = tk.get_action('vocabulary_create')(context, data)

        for tag in LIST:
            # logging.info(
            #         "Adding tag {0} to vocab 'themes'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def themes():
    '''Return the list of country codes from the country codes vocabulary.'''
    create_themes()
    try:
        themes = tk.get_action('tag_list')(
                data_dict={'vocabulary_id': 'themes'})
        return themes
    except tk.ObjectNotFound:
        return None
