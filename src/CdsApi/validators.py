from .exceptions import *
from .helpers import (
    EN_DASH,
    ERA5_START_YEAR, ERA5_CURRENT_YEAR,
    FIRST_MONTH, LAST_MONTH,
    FIRST_DAY, LAST_DAY,
    FIRST_HOUR, LAST_HOUR,
)
from .types import BoundingBox
from typing import Union
from .weather_api import WeatherApi

class Validators:

    @staticmethod
    def list_of_type(data: any, types: Union[type, tuple[type, ...]]) -> None:
        """Validation for list of provided type(s).

        Checks if all the elements in a list are of the provided type(s) or not.

        Args:
            data (any): Data to be validated.
            types (type | tuple[type, ...]): Type(s) to be checked.

        Raises:
            ValidationError: Provided list/tuple is empty.
            ValidationError: Provided data is not list/tuple.
            ValidationError: If any type mismatch is found.
        """
        # using all() with empty list would return "True"
        # explicit check for empty list/tuple
        if not data:
            raise ValidationError("Provided list/tuple can't be empty.")

        if not isinstance(data, (list, tuple)):
            raise ValidationError(f"Provided data must be 'list' or 'tuple'.")
        
        if not all(isinstance(item, types) for item in data):
            raise ValidationError(f"The list/tuple must contain these types only: {types}")
        
    @staticmethod
    def years(years: list[int]) -> None:
        """Validation for list of provided years.

        Args:
            years (list[int]): List of years to be validated.

        Raises:
            ValidationError: When provided years are not in the years for which datasets are available in CDS.
        """
        if not all(year in range(ERA5_START_YEAR, ERA5_CURRENT_YEAR + 1) for year in years):
            raise ValidationError(f"Years must be between {ERA5_START_YEAR}{EN_DASH}{ERA5_CURRENT_YEAR}")
        
    @staticmethod
    def months(months: list[int]) -> None:
        """Validation for list of provided months.

        Args:
            months (list[int]): List of months to be validated.

        Raises:
            ValidationError: When provided months are not in 1–12 range.
        """
        if not all(month in range(FIRST_MONTH, LAST_MONTH + 1) for month in months):
            raise ValidationError(f"Months must be between {FIRST_MONTH}{EN_DASH}{LAST_MONTH}")

        
    @staticmethod
    def days(days: list[int]) -> None:
        """Validation for list of provided days.

        Args:
            days (list[int]): List of days to be validated.

        Raises:
            ValidationError: When provided days are not in 1–31 range.
        """
        if not all(day in range(FIRST_DAY, LAST_DAY + 1) for day in days):
            raise ValidationError(f"Days must be between {FIRST_DAY}{EN_DASH}{LAST_DAY}")
        
    @staticmethod
    def hours(hours: list[int]) -> None:
        """Validation for list of provided hours.

        Args:
            hours (list[int]): List of hours to be validated.

        Raises:
            ValidationError: When provided hours are not in 00:00–23:00 range.
        """
        if not all(hour in range(FIRST_HOUR, LAST_HOUR + 1) for hour in hours):
            raise ValidationError(f"Hours must be between {FIRST_HOUR}{EN_DASH}{LAST_HOUR}")

    @staticmethod
    def data_format(data_format: str) -> None:
        """Validation for dataset format.

        Checks if provided data format is allowed.

        Allowed:

            ["netcdf", "grib"]

        Args:
            data_format (str): Dataset format.

        Raises:
            ValidationError: When provided format is invalid.
        """
        allowed = ["netcdf", "grib"]

        # clean
        data_format = data_format.strip().lower()

        # validate
        if data_format not in allowed:
            raise ValidationError(f"Invalid download_format {data_format}. Download format must be one of {allowed}.")

    @staticmethod
    def download_format(download_format: str) -> None:
        """Validation for download format.

        Checks if provided data format is allowed.

        Allowed:

            ["unarchived", "zip"]

        Args:
            download_format (str): Download format.

        Raises:
            ValidationError: When provided format is invalid.
        """
        allowed = ["unarchived", "zip"]

        # clean
        download_format = download_format.strip().lower()

        # validate
        if download_format not in allowed:
            raise ValidationError(f"Invalid download_format {download_format}. Download format must be one of {allowed}.")
        
    @staticmethod
    def bounding_box(area: BoundingBox) -> None:
        """Validates `BoundingBox` coordinates.

        Args:
            area (BoundingBox): Coordinates in [N, W, S, E] format.

        Raises:
            ValidationError: BoundingBox doesn't have 4 values.
            LatitudeError: South is greater than north, or values are outside [-90, 90].
            LongitudeError: West or East is outside [-180, 180].
        """
        # validate length
        if len(area) != 4:
            raise ValidationError("BoundingBox must have exactly 4 values: [N, W, S, E]")
        
        n, w, s, e = area

        # Latitude checks
        if not (-90 <= s <= n <= 90):
            raise LatitudeError(f"North ({n}) must be >= South ({s}) and both within [-90, 90]")
        
        # Longitude checks
        if not (-180 <= w <= 180):
            raise LongitudeError(f"West ({w}) must be within [-180, 180]")
        
        if not (-180 <= e <= 180):
            raise LongitudeError(f"East ({e}) must be within [-180, 180]")
        
    @staticmethod
    def build_request_parameters(request: WeatherApi) -> None:
        """Validation for request parameters in a particular `WeatherApi` request instance.

        Validates api payload parameters for not-set (None) values.
 
        Args:
            request (WeatherApi): `WeatherApi` request instance.

        Raises:
            BuildError: When `dataset` parameter is not set.
            BuildError: When non-optional parameters are not set.
        """
        request_dict = request.get_request_dict()

        # validate non api payload parameters
        if request.dataset is None:
            raise BuildError("Required field 'dataset' is not set.")
        
        # validate api payload parameters
        for key, value in request_dict.items():
            if key not in request.optional and value is None:
                raise BuildError(f"Required field '{key}' is not set.")
