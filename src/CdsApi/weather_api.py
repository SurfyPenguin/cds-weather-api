from __future__ import annotations
import cdsapi
from .client_config import ClientConfig
from .types import ParameterList, BoundingBox
from typing import Union

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
