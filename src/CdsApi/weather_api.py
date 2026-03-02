from __future__ import annotations
import cdsapi
from .client_config import ClientConfig
from .exceptions import *
from .helpers import CDSFormatter as fmt
from .helpers import (
    ERA5_CURRENT_YEAR, ERA5_START_YEAR,
    FIRST_MONTH, LAST_MONTH,
    FIRST_DAY, LAST_DAY,
    FIRST_HOUR, LAST_HOUR,
    EN_DASH,
)
import os
from .types import ParameterList, BoundingBox
from typing import Union
from .validators import Validators as validate

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
        # client config
        self.client: cdsapi.Client = None

        # required defaults
        self.data_format: str = "netcdf"
        self.download_format: str = "unarchived"
        
        # dataset info
        self.dataset: str = None
        self.product_type: ParameterList = ["reanalysis"]
        self.variables: ParameterList = None

        # duration
        self.year: ParameterList = None
        self.month: ParameterList = None
        self.day: ParameterList = None
        self.time: ParameterList = None
        
        # area
        self.area: BoundingBox = None
        self.target: str = None

        # optional values
        self.optional = {"area"}

    def get_request_dict(self) -> dict[str, Union[str, ParameterList, BoundingBox]]:
        request = {
            "product_type": self.product_type,
            "variable": self.variables,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "time": self.time,
            "data_format": self.data_format,
            "download_format": self.download_format,
            "area": self.area
        }
        return request

    def execute(self) -> None:
        dataset = self.dataset
        request = self.get_request_dict()

        # filter all None values / clean request
        filtered = {key: value for key, value in request.items() if value is not None}

        client = self.client or ClientConfig.config()
        client.retrieve(dataset, filtered).download(self.target)

class RequestBuilder():
    """
    A builder class to construct WeatherApi configuration.
    """
    def __init__(self) -> None:
        self._request: WeatherApi = WeatherApi()

    def client(self, client: cdsapi.Client) -> RequestBuilder:
        """Set client/configuration for request.

        Client/configuration object can be instantiated using cdsapi.Client. 

        Args:
            client (cdsapi.Client): cdsapi.Client instance.

        Raises:
            ValidationError: When provided 'client' value is not an instance of `cdsapi.Client()`
        """
        # validate
        if not isinstance(client, cdsapi.Client):
            raise ValidationError("'client' must be an instance of cdsapi.Client")
        
        self._request.client = client
        return self

    def dataset(self, dataset: str) -> RequestBuilder:
        """Dataset for making request.

        For a list of valid datasets visit https://cds.climate.copernicus.eu/datasets

        Args:
            dataset (str): Name of dataset.
        """        
        self._request.dataset = dataset
        return self

    def product_type(self, *product_type: ParameterList) -> RequestBuilder:
        """The statistical nature of the data, such as hourly analysis, reanalysis, etc.

        Args:
            product_type (ParameterList): Product type such as reanalysis, hourly analysis, etc.
        """        
        # validate
        validate.list_of_type(product_type, types=str)

        self._request.product_type = list(product_type)
        return self
    
    def variables(self, variables: ParameterList) -> RequestBuilder:
        """Key variables which are considered for request.

        Different datasets may have different variables.

        Args:
            variables (ParameterList): Variables in string-list.
        """
        # validate
        validate.list_of_type(variables, types=str)

        self._request.variables = variables
        return self
    
    def year(self, *years: int) -> RequestBuilder:
        """Sets target year(s) for data retrieval.

        Provide specific year values in integer format to set those years for request.

        The years must be between 1939–Current.
        """
        # validate
        validate.list_of_type(years, types=int)

        # for valid years
        if not all(year in range(ERA5_START_YEAR, ERA5_CURRENT_YEAR + 1) for year in years):
            raise ValidationError(f"Years must be between {ERA5_START_YEAR}{EN_DASH}{ERA5_CURRENT_YEAR}")

        self._request.year = fmt.format_to_year_list(years)
        return self
    
    def year_range(self, start: int, stop: int = ERA5_CURRENT_YEAR) -> RequestBuilder:
        """Specify starting and ending year values to set years in that range.
        
        For specific year values, it is highly recommended to use `RequestBuilder.year()`
        method.

        Args:
            start (int): Starting year value.
            stop (int, optional): Ending year value (inclusive). Defaults to `ERA5_CURRENT_YEAR`.
        """
        # to get year range in list[str]
        self._request.year = fmt.year_range(start, stop)
        return self
    
    def month(self, *months: int) -> RequestBuilder:
        """Sets target month(s) for data retrieval.

        Provide specific month values in integer format to set those months for request.

        The months must be between 1–12.
        """
        # validate
        validate.list_of_type(months, types=int)

        # for valid months
        if not all(month in range(FIRST_MONTH, LAST_MONTH + 1) for month in months):
            raise ValidationError(f"Months must be between {FIRST_MONTH}{EN_DASH}{LAST_MONTH}")

        self._request.month = fmt.format_to_month_list(months)
        return self
    
    def month_range(self, start: int, stop: int) -> RequestBuilder:
        """Specify starting and ending month values to set months in that range.

        Months are cyclic so starting (`start`) month doesn't need to be less than ending (`stop`) month.
        Use `RequestBuilder.month()` method to set specific values of month.

        Args:
            start (int): Starting month value (1–12).
            stop (int): Ending month value (1–12, inclusive).
        """
        # to get month range in list[str]
        self._request.month = fmt.month_range(start, stop)
        return self

    
    def day(self, *days: int) -> RequestBuilder:
        """Sets target days(s) for data retrieval.

        Provide specific day values in integer format to set those months for request.

        The days must be between 1–31.
        """
        # validate
        validate.list_of_type(days, types=int)

        # for valid days
        if not all(day in range(FIRST_DAY, LAST_DAY + 1) for day in days):
            raise ValidationError(f"Days must be between {FIRST_DAY}{EN_DASH}{LAST_DAY}")

        self._request.day = fmt.format_to_day_list(days)
        return self
    
    def day_range(self, start: int, stop: int) -> RequestBuilder:
        """Specify starting and ending day values to set days in that range.

        For specific day values, it is highly recommended to use `RequestBuilder.day()` method.

        Args:
            start (int): Starting day value (1–12).
            stop (int): Ending day value (1–12, inclusive).
        """
        # to get day range in list[str]
        self._request.day = fmt.day_range(start, stop)
        return self
    
    def time(self, *hours) -> RequestBuilder:
        """Sets the target hours for data retrieval.

        This method accepts a list of timestamps in 24-hour format. It ensures that each entry follows the "HH:MM" convention
        """
        # validate
        validate.list_of_type(hours, types=int)

        # for valid hours
        if not all(hour in range(FIRST_HOUR, LAST_HOUR + 1) for hour in hours):
            raise ValidationError(f"Hours must be between {FIRST_HOUR}{EN_DASH}{LAST_HOUR}")

        self._request.time = fmt.format_to_hour_list(hours)
        return self
    
    def time_range(self, start: int, stop: int) -> RequestBuilder:
        """Specify starting and ending time values to set hours in that range.

        Hours are cyclic so starting (`start`) time doesn't need to be less than ending (`stop`) time.
        Use `RequestBuilder.time()` method to set specific values of time in HH:MM format.

        Args:
            start (int): Starting time value (0–23).
            stop (int): Ending time value (0–23, inclusive).
        """
        # to get time range in list[str]
        self._request.time = fmt.time_range(start, stop)
        return self
    
    def data_format(self, data_format: str) -> RequestBuilder:
        """Sets the data-format in which the dataset would be requested from CDS

        This method can take two parameters "netcdf" and "grib"

        Args:
            data_format (str): Takes preferred data-format 

        Raises:
            ValidationError: When provided data_format is not allowed/available.
        """
        allowed = ["netcdf", "grib"]
        
        # clean
        data_format = data_format.strip().lower()

        # validate
        if data_format.lower().strip() not in allowed:
            raise ValidationError(f"Invalid data_format {data_format}. Data format must be one of {allowed}.")

        self._request.data_format = data_format
        return self
    
    def download_format(self, download_format: str) -> RequestBuilder:
        """Sets the download-format in which the dataset would be requested from CDS

        This method can take two parameters "unarchived" and "zip"

        Args:
            data_format (str): Takes preferred download-format

        Raises:
            ValidationError: When provided download-format is not allowed/available.
        """
        allowed = ["unarchived", "zip"]

        # clean
        download_format = download_format.strip().lower()

        # validate
        if download_format.lower().strip() not in allowed:
            raise ValidationError(f"Invalid download_format {download_format}. Download format must be one of {allowed}.")
        
        self._request.download_format = download_format
        return self
    
    def area(self, area: BoundingBox) -> RequestBuilder:
        """Sets the geographical bounding box for the ERA5 data request.

        Args:
            area (BoundingBox): Coordinates of bounding area in the format [N, W, S, E].

        Raises:
            ValidationError: Raised when provided BoundingBox doesn't have 4 values
            LatitudeError: Raised for invalid latitudes
            ValidationError: Raised for invalid longitudes
        """

        # validate type
        validate.list_of_type(area, types=(int, float))

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
    
    def target(self, file_name: Union[str , os.PathLike], dir: os.PathLike = os.getcwd()) -> RequestBuilder:
        """Downloads data-set in current-working directory

        Args:
            file_name (str): Name of file.
            dir (str, optional): Target directory. Defaults to os.getcwd().
        """

        target = os.path.join(dir, file_name)
        self._request.target = target

        return self
    
    def build(self) -> WeatherApi:
        """Builds and returns the request

        The request object can be executed using `request.execute()`.

        Raises:
            BuildError: When 'dataset' attribute is not set.
            BuildError: When required attributes are not set.

        Returns:
            WeatherApi: Built request.
        """
        optional = self._request.optional
        request_dict = self._request.get_request_dict()

        # validate non api payload parameters
        if self._request.dataset is None:
            raise BuildError("Required field 'dataset' is not set.")
        
        # validate api payload parameters
        for key, value in request_dict.items():
            if key not in optional and value is None:
                raise BuildError(f"Required field '{key}' is not set.")
                      
        return self._request
