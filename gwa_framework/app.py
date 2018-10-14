import os

from decouple import config
from flask import Flask


class GWAApp(Flask):

    def __init__(self, import_name,  **kwargs):
        os.environ['FLASK_ENV'] = config('ENV')
        os.environ['FLASK_DEBUG'] = config('DEBUG')
        super(GWAApp, self).__init__(import_name, **kwargs)
