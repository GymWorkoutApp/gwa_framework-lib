from functools import wraps

from flask import jsonify, request
from schematics.exceptions import DataError


def validate_schema(schema: 'Model'):
    def validate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                partial = True if request.method.lower() == 'patch' else False
                schema_obj = schema(request.json)
                schema_obj.validate(partial=partial)
                return fn(*args, **kwargs, request_model=schema_obj)
            except DataError as e:
                return jsonify(str(e), 422)

        return wrapper

    return validate
