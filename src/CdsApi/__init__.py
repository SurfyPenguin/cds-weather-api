from importlib.metadata import version

from .client_config import ClientConfig
from .exceptions import (
    BuildError,
    ClientError,
    LatitudeError,
    LongitudeError,
    ValidationError,
)
from .helpers import CDSFormatter
from .request_builder import RequestBuilder
from .weather_api import WeatherApi

__version__ = version("cds-weather-api")
__author__ = "SurfyPenguin"

__all__ = [
    "CDSFormatter",
    "ClientConfig",
    "RequestBuilder",
    "WeatherApi",
    "BuildError",
    "ClientError",
    "LatitudeError",
    "LongitudeError",
    "ValidationError",
]