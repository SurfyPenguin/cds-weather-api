import cdsapi
from typing import Self, Callable

class WeatherApi:
    """
    Handles the configuration and execution of data retrieval from the Copernicus Climate Data Store.

    Attributes:
        dataset (str): The name of the ERA5 dataset to query.
        product_type (list[str]): List of product types (e.g., 'reanalysis').
        variables (list[str]): Meteorological variables to download.
        year (list[str]): Target years for data retrieval.
        month (list[str]): Target months in 'MM' format.
        day (list[str]): Target days of the month.
        time (list[str]): Target times in 'HH:MM' format.
        data_format (str): The file format for the output (e.g., 'netcdf').
        download_format (str): Archive or unarchived format specification.
        area (list[int]): Geographical bounding box [North, West, South, East].
    """
    def __init__(self) -> None:
        self.dataset: str = "reanalysis-era5-single-levels"
        self.product_type: list[str] = ["reanalysis"]
        self.variables: list[str] = [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "total_precipitation"
        ]

        self.year: list[str] = ["2025"]
        self.month: list[str] = ["01", "02", "03"]
        self.day: list[str] = [
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

        self.time: list[str] = [
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
        
        self.area: list[int] = [40, 60, 0, 100]

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

    def _validate_list_of_strings(self, data: any, func_ref: Callable):
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

    def dataset(self, dataset: str) -> Self:
        self._request.dataset = dataset
        return self

    def product_type(self, product_type: list[str]) -> Self:
        # validate
        self._validate_list_of_strings(product_type, self.product_type)

        self._request.product_type = product_type
        return self
    
    def variables(self, variables: list[str]) -> Self:
        # validate
        self._validate_list_of_strings(variables, self.variables)

        self._request.variables = variables
        return self
    
    def year(self, years: list[str]) -> Self:
        # validate
        self._validate_list_of_strings(years, self.year)

        self._request.year = years
        return self
    
    def month(self, months: list[str]) -> Self:
        # validate
        self._validate_list_of_strings(months, self.month)

        self._request.month = months
        return self
    
    def day(self, days: list[str]) -> Self:
        # validate
        self._validate_list_of_strings(days, self.day)

        self._request.day = days
        return self
    
    def time(self, time: list[str]) -> Self:
        # validate
        self._validate_list_of_strings(time, self.time)

        self._request.time = time
        return self
    
    def data_format(self, data_format: str) -> Self:
        self._request.data_format = data_format
        return self
    
    def area(self, area: list[int]) -> Self:
        self._request.area = area
        return self
    
    def build(self) -> WeatherApi:
        return self._request
