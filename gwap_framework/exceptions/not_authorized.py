import gwap_framework.exceptions.base


class NotAuthorizedException(gwap_framework.exceptions.base.BaseException):
    """
        NotAuthorizedException are dispatch when requests is not authenticated
    """
