from it.unito.facets import *


class Facet(object):

    def __init__(self, facet_file):
        self._facet_file = facet_file
        self._load()

    def _load(self):

        with open(self._facet_file, 'r') as reader:
            facet = commentjson.load(reader)

        if 'name' not in facet:
            raise Exception('name not found in facet')
        self._name = facet['name']

        if 'url' not in facet:
            raise Exception('url not found in facet')
        self._url = facet['url']

        if 'folder' not in facet:
            raise Exception('folder not found in facet')
        self._output_folder = facet['folder']

        if 'browser' not in facet:
            raise Exception('browser not found in facet')
        self._browser = facet['browser']

        if 'writer' not in facet:
            raise Exception('writer not in facet')
        self._writer = facet['writer']

        if 'items' not in facet:
            raise Exception('item not in facet')
        self._items = facet['items']

        if 'fields' not in facet:
            raise Exception('fields not in facet')
        self._fields = facet['fields']

    def get_name(self):
        return self._name

    def get_url(self):
        return self._url

    def get_folder(self):
        return self._output_folder

    def get_browser(self):
        return self._browser

    def get_writer(self):
        return self._writer

    def get_items(self):
        return self._items

    def get_fields_name(self):
        return list(self._fields.keys())

    def get_field_parameters(self, field):

        assert isinstance(field, str), 'field parameter is not a string'

        if field not in self._fields:
            raise ValueError('field %s not present in field dictionary')

        return self._fields[field]
