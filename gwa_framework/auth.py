import json
from typing import Union

import aiohttp
import jwt
import requests
from flask import request, Blueprint

from gwa_framework import asyncio
from gwa_framework.app import GWAApp
from gwa_framework.asyncio import get_loop
from gwa_framework.exceptions.not_authorized import NotAuthorizedException
from gwa_framework.settings import GWAAuthSettings


class GWAAuth(object):
    app = None

    def __init__(self, app: Union[GWAApp, Blueprint]):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        async def call_oauth_token(bearer_token):
            async with aiohttp.ClientSession() as session:
                try:
                    response = await session.post(f'{GWAAuthSettings.INTROSPECT_URL}?token={bearer_token.split("Bearer ")[1]}', "")
                    if response.status == 200:
                        return await response.json()

                    return None

                except asyncio.TimeoutError as e:
                    self.logger.error(f'TimeoutError endpoint: {GWAAuthSettings.INTROSPECT_URL}')
                    raise e
                except Exception as e:
                    self.logger.error(f'error post endpoint: {GWAAuthSettings.INTROSPECT_URL} {str(e)}')
                    raise e

        def authenticate():
            if 'Authorization' in request.headers:
                bearer_token = request.headers.get("Authorization", default=None)
                if bearer_token:
                    resp = get_loop().run_until_complete(call_oauth_token())

                    if resp.status_code == 200:
                        token = resp.content.decode()
                        token = json.loads(token)
                        decoded = jwt.decode(token['access_token'], GWAAuthSettings.TOKEN_KEY,
                                             algorithms=['HS512'])
                        request.owner = decoded
                        return
            raise NotAuthorizedException('You are not authorized for this request.')

        if isinstance(app, GWAApp):
            app.before_request_funcs.setdefault(None, []).append(authenticate)
        elif isinstance(app, Blueprint):
            app.before_request(authenticate)
