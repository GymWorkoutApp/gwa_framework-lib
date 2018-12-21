from enum import Enum


class PubSubOperation(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
