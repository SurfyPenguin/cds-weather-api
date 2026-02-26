class ClientError(Exception):
    """Raised when no valid client is provided or .cdsapirc file doesn't exist."""

class ValidationError(Exception):
    """Raised when request parameters are out of range or malformed"""

class LatitudeError(ValidationError):
    """Raised when rules of defining latitudes are not followed."""

class LongitudeError(ValidationError):
    """Raised when rules of defining longitudes are not followed."""