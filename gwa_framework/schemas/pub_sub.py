from schematics.contrib.enum_type import EnumType
from schematics.types import ModelType

from gwa_framework.schemas.base import BaseSchema
from gwa_framework.utils.enums import PubSubOperation


class PubSubMessage(BaseSchema):
    message = ModelType(model_spec=BaseSchema, required=True, serialized_name='message')
    operation = EnumType(required=True, serialized_name='operation', choices=[e.value for e in PubSubOperation])
