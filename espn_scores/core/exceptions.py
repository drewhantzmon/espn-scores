"""Custom exceptions for ESPN Scores package."""


class ESPNScoresException(Exception):
    """Base exception for all ESPN Scores errors."""
    pass


class APIException(ESPNScoresException):
    """Exception raised when ESPN API returns an error."""
    
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        super().__init__(message)


class InvalidDateException(ESPNScoresException):
    """Exception raised when an invalid date is provided."""
    pass


class InvalidWeekException(ESPNScoresException):
    """Exception raised when an invalid week number is provided."""
    pass
