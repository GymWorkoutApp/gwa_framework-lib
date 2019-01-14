import json
import pickle
from collections import OrderedDict
from typing import Dict

from flask import request
from flask_restful import Resource
from flask_restful import unpack
from werkzeug.wrappers import Response


class BaseResource(Resource):
    owner = None
    cache = None
    __actions = {
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'put': 'update',
        'delete': 'destroy',
        'retrieve': 'retrieve'
    }

    def dispatch_request(self, *args, **kwargs):
        # Taken from flask
        # noinspection PyUnresolvedReferences
        self.owner = request.owner

        if request.method.lower() == 'get' and (kwargs or args):
            meth = getattr(self, self.__actions['retrieve'])
        else:
            meth = getattr(self, self.__actions[request.method.lower()], None)

        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % self.__actions[request.method.lower()]

        if isinstance(self.method_decorators, Dict):
            decorators = self.method_decorators.get(self.__actions.get(request.method.lower()), [])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)

        if isinstance(resp, Response):  # There may be a better way to test
            return resp

        representations = self.representations or OrderedDict()

        # noinspection PyUnresolvedReferences
        mediatype = request.accept_mimetypes.best_match(representations, default=None)
        if mediatype in representations:
            data, code, headers = unpack(resp)
            resp = representations[mediatype](data, code, headers)
            resp.headers['Content-Type'] = mediatype
            return resp

        return resp

    @staticmethod
    def get_args(key, default=None, type=None):
        return request.args.get(key, default=default, type=type)

    def set_cache(self, name, key, value, expire=60 * 60):
        self.cache.hset(name, key, pickle.dumps(value))
        self.cache.expire(name, expire)

    def get_cache(self, name, key):
        result = self.cache.hget(name, key)
        if result:
            return pickle.loads(result)
        return None
