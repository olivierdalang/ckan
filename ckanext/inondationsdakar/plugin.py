# encoding: utf-8

import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


def create_document_types():
    '''Create document_types vocab and tags, if they don't exist already.

    Note that you could also create the vocab and tags using CKAN's API,
    and once they are created you can edit them (e.g. to add and remove
    possible dataset country code values) using the API.

    Voir les vocabulaire : https://127.0.0.1/api/3/action/vocabulary_list
    Supprimer le vocabulaire (/!\ on perd assignation !)

    '''
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'document_types'}
        tk.get_action('vocabulary_show')(context, data)
        logging.info("Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        # logging.info("Creating vocab 'document_types'")
        data = {'name': 'document_types'}
        vocab = tk.get_action('vocabulary_create')(context, data)

        # doc_types = [
        #     "Plan de développement",
        #     "Texte réglementaire",
        #     "Loi",
        #     "Article de presse",
        #     "Rapport d'activités",
        #     "Rapport final",
        #     "Document diagnostic",
        #     "Donnée météorologique",
        #     "Donnée démographique",
        #     "Donnée technique",
        #     "Donnée spatiale",
        #     "Carte",
        #     "Thèse ou mémoire",
        #     "Autre",
        # ]
        doc_types = [
            u"projet de développement",
            u"texte réglementaire et lois",
            u"article de presse",
            u"rapport de projet",
            u"diagnostic",
            u"données brutes",
            u"carte",
            u"thèse ou mémoire",
            u"guide",
            u"autre",
        ]

        for tag in doc_types:
            # logging.info(
            #         "Adding tag {0} to vocab 'document_types'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def document_types():
    '''Return the list of country codes from the country codes vocabulary.'''
    create_document_types()
    try:
        document_types = tk.get_action('tag_list')(
                data_dict={'vocabulary_id': 'document_types'})
        return document_types
    except tk.ObjectNotFound:
        return None


class InondationsDakarPlugin(plugins.SingletonPlugin,
        tk.DefaultDatasetForm):
    '''An example IDatasetForm CKAN plugin.

    Uses a tag vocabulary to add a custom metadata field to datasets.

    '''
    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)
    plugins.implements(plugins.IFacets, inherit=False)


    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')

    def get_helpers(self):
        return {'document_types': document_types}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        # Add our custom document_type metadata field to the schema.
        schema.update({
                'document_type': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')('document_types')]
                })
        return schema

    def create_package_schema(self):
        schema = super(InondationsDakarPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(InondationsDakarPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(InondationsDakarPlugin, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        # Add our custom document_type metadata field to the schema.
        schema.update({
            'document_type': [
                tk.get_converter('convert_from_tags')('document_types'),
                tk.get_validator('ignore_missing')]
            })
        return schema


    def dataset_facets(self, facets_dict, package_type):

        facets_dict['document_type'] = tk._('Document type')

        # Return the updated facet dict.
        return facets_dict
