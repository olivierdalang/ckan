# encoding: utf-8

import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk

from .data_document_types import document_types, create_document_types
from .data_themes import themes, create_themes


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
        return {
            'document_types': document_types,
            'themes': themes,
        }

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
            'document_type': [
                tk.get_validator('ignore_missing'),
                tk.get_converter('convert_to_tags')('document_types'),
            ],
            'theme': [
                tk.get_validator('ignore_missing'),
                tk.get_converter('convert_to_tags')('themes'),
            ],
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
                tk.get_validator('ignore_missing'),
            ],
            'theme': [
                tk.get_converter('convert_from_tags')('themes'),
                tk.get_validator('ignore_missing'),
            ],
        })
        return schema

    def _append_facets(self, facets_dict):
        facets_dict['vocab_themes'] = tk._('Theme')
        facets_dict['vocab_document_types'] = tk._('Document type')
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        return self._append_facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        return self._append_facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type, package_type):
        return self._append_facets(facets_dict)
