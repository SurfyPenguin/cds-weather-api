class BuildError(Exception):
    """Raised when building request fails."""

class ClientError(Exception):
    """Raised when no valid client is provided or .cdsapirc file doesn't exist."""

class ValidationError(ValueError):
    """Raised when request parameter is not formed correctly."""

class LatitudeError(ValidationError):
    """Raised when rules of defining latitudes are not followed."""

class LongitudeError(ValidationError):
    """Raised when rules of defining longitudes are not followed."""