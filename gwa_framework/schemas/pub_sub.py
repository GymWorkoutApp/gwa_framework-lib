from schematics.types import StringType, ModelType

from gwa_framework.schemas.base import BaseSchema


class PubSubMessage(BaseSchema):
    message = ModelType(model_spec=BaseSchema, required=True, serialized_name='message')
    operation = StringType(required=True, serialized_name='operation')

