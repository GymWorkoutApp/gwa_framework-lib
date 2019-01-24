from gwap_framework.resource.base import BaseResource


class HealthCheckResource(BaseResource):

    def list(self):
        return {
            'status': 'Healthy'
        }
