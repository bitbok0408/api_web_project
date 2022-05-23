import collections
import re


class Cleaner:

    def __init__(self):
        self._storage = collections.deque()

    @property
    def storage(self):
        return self._storage

    @property
    def storage_copy(self):
        return list(self._storage)

    def add(self, url_name, response):
        rid_list = self.take_rid_list_from_response(url_name, response)
        for i in rid_list:
            self._storage.appendleft((url_name, i))

    def take_rid_list_from_response(self, url_name, response):
        response = response.json()
        params_list = self.identification(url_name)
        rid_list = [response[i] for i in params_list if i in response.keys() if isinstance(response[i], str)]
        return rid_list

    def remove(self, url_name, rid):
        url_with_rid = (url_name, rid)
        while url_with_rid in self._storage:
            self._storage.remove(url_with_rid)

    @staticmethod
    def identification(url):
        idents_list = []
        ident = re.search(r'/(?P<name>[\w-]+)$', url).group('name')
        if "-" in ident:
            ident = ident.split('-')[0] + ident.split('-')[1].capitalize()
        idents_list.append(ident + "Id")
        if ident.endswith('s'):
            idents_list.append(ident[:-1] + "Id")
        return idents_list
