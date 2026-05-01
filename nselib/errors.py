from enum import Enum


class ErrorCodeEnum(Enum):
    """Error codes for NSElib"""

    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    API_ERROR = "API_ERROR"
    CALENDAR_NOT_FOUND = "CALENDAR_NOT_FOUND"
    DATA_NOT_FOUND = "DATA_NOT_FOUND"
    INVALID_INDEX_CATEGORY = "INVALID_INDEX_CATEGORY"
    INVALID_INDEX = "INVALID_INDEX"
    DERIVATIVE_INSTRUMENT_NOT_FOUND = "DERIVATIVE_INSTRUMENT_NOT_FOUND"


class NSEException(Exception):
    """Base class for all NSElib exceptions"""

    error_code: ErrorCodeEnum = ErrorCodeEnum.UNKNOWN_ERROR

    def __init__(
        self,
        message: str,
        error_code: ErrorCodeEnum = ErrorCodeEnum.UNKNOWN_ERROR,
    ):
        super().__init__(message)
        self.error_code: ErrorCodeEnum = error_code
        self.message: str = message


class NSEApiError(NSEException):
    """Exception raised when NSE API returns an error"""

    def __init__(self, message):
        super(NSEApiError, self).__init__(message, ErrorCodeEnum.API_ERROR)


class CalenderNotFound(NSEException):
    """Exception raised when a calendar is not found"""

    def __init__(self, message):
        super(CalenderNotFound, self).__init__(
            message, ErrorCodeEnum.CALENDAR_NOT_FOUND
        )


class DerivativeInstrumentNotFoundError(NSEException):
    """Exception raised when derivative instrument is not found"""

    def __init__(self, message):
        super(DerivativeInstrumentNotFoundError, self).__init__(
            message, ErrorCodeEnum.DERIVATIVE_INSTRUMENT_NOT_FOUND
        )


class NSEdataNotFound(NSEException):
    """Exception raised when data is not found"""

    def __init__(self, message):
        super(NSEdataNotFound, self).__init__(message, ErrorCodeEnum.DATA_NOT_FOUND)


class InvalidIndexCategoryError(NSEException):
    """Exception raised when category is not found"""

    def __init__(self, message):
        super(InvalidIndexCategoryError, self).__init__(
            message, ErrorCodeEnum.INVALID_INDEX_CATEGORY
        )


class InvalidIndexError(NSEException):
    """Exception raised when index is invalid"""

    def __init__(self, message):
        super(InvalidIndexError, self).__init__(message, ErrorCodeEnum.INVALID_INDEX)


class IndexDataNotFound(NSEException):
    """Exception raised when index data is not found"""

    def __init__(self, message):
        super(IndexDataNotFound, self).__init__(message, ErrorCodeEnum.DATA_NOT_FOUND)
