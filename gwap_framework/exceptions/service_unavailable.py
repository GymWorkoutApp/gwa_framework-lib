import gwap_framework.exceptions.base


class ServiceUnavailableException(gwap_framework.exceptions.base.BaseException):
    """
        ServiceUnavailableException are dispatch when requests is not completed by any reason
    """
