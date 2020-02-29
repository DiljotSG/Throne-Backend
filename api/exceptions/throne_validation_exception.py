from .throne_exception import ThroneException


class ThroneValidationException(ThroneException):
    def __init__(self, message="Provided data is invalid"):
        super().__init__(message)
