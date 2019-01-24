from typing import Union

import aiohttp
import jwt
from flask import request, Blueprint

from gwap_framework.app import GwapApp
from gwap_framework.asyncio import get_loop
from gwap_framework.exceptions.not_authorized import NotAuthorizedException
from gwap_framework.exceptions.service_unavailable import ServiceUnavailableException
from gwap_framework.settings import GwapAuthSettings


class GwapAuth:
    """
        GwapAuth is a middleware which guarantees every requests to endpoints are authenticated.
    """
    app = None
    logger = None

    def __init__(self, app: Union[GwapApp, Blueprint], logger):
        if app:
            self.init_app(app, logger)

    def init_app(self, app, logger) -> None:
        """

        :param app: GwapApp
        :return: None
        """
        self.app = app
        self.logger = logger

        async def call_oauth_token(bearer_token):
            async with aiohttp.ClientSession() as session:
                try:
                    response = await session.get(
                        f'{GwapAuthSettings.INTROSPECT_URL}?token={bearer_token.split("Bearer ")[1]}')
                    if response.status == 200:
                        return await response.json()

                    return None

                except TimeoutError as exception:
                    self.logger.error(f'TimeoutError endpoint: {GwapAuthSettings.INTROSPECT_URL}')
                    raise exception
                except aiohttp.ClientConnectorError as exception:
                    self.logger.error(f'ClientConnectorError service unavailable: {GwapAuthSettings.INTROSPECT_URL}')
                    raise ServiceUnavailableException(exception)
                except Exception as exception:
                    self.logger.error(f'Error post endpoint: {GwapAuthSettings.INTROSPECT_URL} {str(exception)}')
                    raise exception

        def authenticate():
            if 'Authorization' in request.headers:
                bearer_token = request.headers.get("Authorization", default=None)
                if bearer_token:
                    token = get_loop().run_until_complete(call_oauth_token(bearer_token))

                    if token:
                        decoded = jwt.decode(token['access_token'], GwapAuthSettings.TOKEN_KEY,
                                             algorithms=['HS512'])
                        request.owner = decoded
                        return
            raise NotAuthorizedException('You are not authorized for this request.')

        if isinstance(app, GwapApp):
            app.before_request_funcs.setdefault(None, []).append(authenticate)
        elif isinstance(app, Blueprint):
            app.before_request(authenticate)
