import cdsapi
from typing import Self, Callable
from exceptions import *

type ParameterList = list[str]
"""
Representation for list which contains string parameters.

Example:

    product_type = ['reanalysis']
    day = ["01", "02", "03", ..., "12"]
    month = ["01", "02", ..., "30"]
"""

type BoundingBox = list[int | float]
"""
Represents a geographical area as a list of four coordinates.

Format:

    [North, West, South, East]

Example:

    [90, -120, -90, 180]
"""

class WeatherApi:
    """
    Handles the configuration and execution of data retrieval from the Copernicus Climate Data Store.

    Attributes:
        dataset (str): The name of the ERA5 dataset to query.
        product_type (ParameterList): List of product types (e.g., 'reanalysis').
        variables (ParameterList): Meteorological variables to download.
        year (ParameterList): Target years for data retrieval.
        month (ParameterList): Target months in 'MM' format.
        day (ParameterList): Target days of the month.
        time (ParameterList): Target times in 'HH:MM' format.
        data_format (str): The file format for the output (e.g., 'netcdf').
        download_format (str): Archive or unarchived format specification.
        area (BoundingBox): Geographical bounding box [North, West, South, East].
    """
    def __init__(self) -> None:
        self.dataset: str = "reanalysis-era5-single-levels"
        self.product_type: ParameterList = ["reanalysis"]
        self.variables: ParameterList = [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "total_precipitation"
        ]

        self.year: ParameterList = ["2025"]
        self.month: ParameterList = ["01", "02", "03"]
        self.day: ParameterList = [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"
        ]

        self.time: ParameterList = [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ]

        self.data_format: str = "netcdf"
        self.download_format: str = "unarchived"
        
        self.area: BoundingBox = [40, 60, 0, 100]

    def execute(self) -> None:
        dataset = self.dataset
        request = {"product_type": self.product_type,
            "variable": self.variables,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "time": self.time,
            "data_format": self.data_format,
            "download_format": self.download_format,
            "area": self.area
        }

        client = cdsapi.Client()
        client.retrieve(dataset, request).download()  

class RequestBuilder():
    """
    A builder class to construct WeatherApi configuration.
    """
    def __init__(self) -> None:
        self._request: WeatherApi = WeatherApi()

    def _validate_list_of_strings(self, data: any, func_ref: Callable) -> None:
        """Validation for list-of-string fields.

        Args:
            data (any): The input value to validate.
            func_ref (Callable): The calling method used to generate context-aware error messages. 

        Raises:
            ValueError: If "data" is not a list or contains non-string elements.
        """
        name = func_ref.__name__
        if (
            not isinstance(data, list) or
            not all(isinstance(item, str) for item in data)
        ):
            raise ValueError(f"'{name}' must be a list of strings")
        
    def _validate_list_of_numbers(self, data: any):
        """Validation for list of int/float fields.

        Args:
            data (any): The input value to validate.

        Raises:
            ValueError: Raised when data is a list or does not contain integer/float values.
        """
        if (
            not isinstance(data, list) or
            not all(isinstance(item, (int, float)) for item in data)
        ):
            raise ValueError("'area' must contain list of north, west, south and east coordinates as integer or float")

    def dataset(self, dataset: str) -> Self:
        self._request.dataset = dataset
        return self

    def product_type(self, product_type: ParameterList) -> Self:
        # validate
        self._validate_list_of_strings(product_type, self.product_type)

        self._request.product_type = product_type
        return self
    
    def variables(self, variables: ParameterList) -> Self:
        # validate
        self._validate_list_of_strings(variables, self.variables)

        self._request.variables = variables
        return self
    
    def year(self, years: ParameterList) -> Self:
        # validate
        self._validate_list_of_strings(years, self.year)

        self._request.year = years
        return self
    
    def month(self, months: ParameterList) -> Self:
        # validate
        self._validate_list_of_strings(months, self.month)

        self._request.month = months
        return self
    
    def day(self, days: ParameterList) -> Self:
        # validate
        self._validate_list_of_strings(days, self.day)

        self._request.day = days
        return self
    
    def time(self, time: ParameterList) -> Self:
        # validate
        self._validate_list_of_strings(time, self.time)

        self._request.time = time
        return self
    
    def data_format(self, data_format: str) -> Self:
        self._request.data_format = data_format
        return self
    
    def area(self, area: BoundingBox) -> Self:
        """Sets the geographical bounding box for the ERA5 data request.

        Args:
            area (BoundingBox): Coordinates of bounding area in the format [N, W, S, E].

        Raises:
            ValidationError: Raised when provided BoundingBox doesn't have 4 values
            LatitudeError: Raised for invalid latitudes
            ValidationError: Raised for invalid longitudes
        """

        # validate type
        self._validate_list_of_numbers(area)

        # validate length
        if len(area) != 4:
            raise ValidationError("BoundingBox must have exactly 4 values: [N, W, S, E]")
        
        n, w, s, e = area

        # Latitude checks
        if not (-90 <= s <= n <= 90):
            raise LatitudeError(f"North ({n}) must be >= South ({s}) and both within [-90, 90]")
        
        # Longitude checks
        if not (-180 <= w <= e <= 180):
            raise LongitudeError(f"East ({e}) must be >= West ({w}) and both within [-180, 180]")

        self._request.area = area
        return self
    
    def build(self) -> WeatherApi:
        return self._request
