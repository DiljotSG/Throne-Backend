from .throne_exception import ThroneException


class ThroneUnauthorizedException(ThroneException):
    def __init__(self, message="You do not have permission to do that"):
        super().__init__(message)
