import requests
from flask import request

from gwa_framework.app import GWAApp
from gwa_framework.exceptions.not_authorized import NotAuthorizedException
from gwa_framework.settings import GWAAuthSettings


class GWAAuth(object):
    app = None

    def __init__(self, app: 'GWAApp', **kwargs):
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        self.app = app;

        def authenticate():
            if 'Authorization' in request.headers:
                bearer_token = request.headers.get("Authorization", default=None)
                if bearer_token:
                    response = requests.post(f'{GWAAuthSettings.INTROSPECT_URL}?token={bearer_token.split("Bearer ")[1]}')
                    if response.status_code == 200:
                        token = response.content.decode()
                        return
            raise NotAuthorizedException('You are not authorized for this request.')

        app.before_request_funcs.setdefault(None, []).append(authenticate)
