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
from .weather_api import WeatherApi

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
            start (int): Starting day value (1–31).
            stop (int): Ending day value (1–31, inclusive).
        """
        # to get day range in list[str]
        self._request.day = fmt.day_range(start, stop)
        return self
    
    def time(self, *hours: int) -> RequestBuilder:
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
        if data_format not in allowed:
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
        if download_format not in allowed:
            raise ValidationError(f"Invalid download_format {download_format}. Download format must be one of {allowed}.")
        
        self._request.download_format = download_format
        return self
    
    def area(self, area: BoundingBox) -> RequestBuilder:
        """Sets the geographical bounding box for the ERA5 data request.

        Args:
            area (BoundingBox): Coordinates of bounding area in the format [N, W, S, E].

        Raises:
            ValidationError: BoundingBox doesn't have 4 values.
            LatitudeError: South is greater than north, or values are outside [-90, 90].
            LongitudeError: West or East is outside [-180, 180].
        """
        # validate type
        validate.list_of_type(area, types=(int, float))
        validate.bounding_box(area)

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

        Returns:
            WeatherApi: Built request.

        Raises:
            BuildError: When `dataset` parameter is not set.
            BuildError: When non-optional parameters are not set.
        """
        validate.build_request_parameters(self._request)
        return self._request
