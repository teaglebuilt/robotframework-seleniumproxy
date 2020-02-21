from collections import OrderedDict
from collections.abc import Mapping, MutableMapping


class InspectRequestMixin:

    @property
    def requests(self):
        return [Request(r, self.client) for r in self.client.get_requests()]


class Request:

    def __init__(self, data, client):
        self.data = data
        self.client = client
        self.method = data['method']
        self.path = data['path']
        self.headers = data['headers']

    def body(self):
        if self.data.get('body') is None:
            self.data['body'] = self.client.get_request_body(self.data['id'])
        return self.data['body']

    def __repr__(self):
        return 'Request({})'.format(self._data)

    def __str__(self):
        return self.path


class Response:

    def __init__(self, request, data, client):
        self.request_id = request_id
        self.data = data
        self.client = client
        self.headers = data['headers']
        self.status_code = data['status_code']

    @property
    def body(self):
        if self.data.get('body') is None:
            self.data['body'] = self._client.get_response_body(
                self.request_id)
        return self.data['body']

    def __repr__(self):
        return "Response('{}', {})".format(self._request_id, self._data)

    def __str__(self):
        return '{} {}'.format(self.status_code, self.reason)


class CaseInsensitiveDict(MutableMapping):

    def __init__(self, data=None, **kwargs):
        self.store = OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        self.store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self.store[key.lower()][1]

    def __delitem__(self, key):
        del self.store[key.lower()]

    def copy(self):
        return CaseInsensitiveDict(self.store.values())

    def __repr__(self):
        return str(dict(self.items()))
