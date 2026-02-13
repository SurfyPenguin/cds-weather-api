# CDS API Request builder

## A wrapper around Copernicus Climate Data Store API library (cdsapi) to simplify request creation, using builder design pattern.

Making a request with cdsapi library looks like this:

[Reanalysis ERA5 single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview)
```python
import cdsapi

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_dewpoint_temperature",
        "2m_temperature",
        "total_precipitation"
    ],
    "year": ["2024"],
    "month": [
        "05", "06", "07",
        "08"
    ],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15"
    ],
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [40, 60, 0, 100]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
```
While some variables remain constant throughout the process, modifying dates, months and years is not convenient. And requires this particular format:

```python
"day": [
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
],

"year": [
        "2021", "2022", "2023",
        "2024", "2025"
],

"month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
],
```

This project simplifies this request and allows user to make the same request like this:

```python
from WeatherApi import RequestBuilder

variables = [
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_dewpoint_temperature",
    "2m_temperature",
    "total_precipitation"
]

request = (
    RequestBuilder()
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .year(["2024"])
    .month_range(1, 8)
    .day_range(1, 31)
    .time_range(1, 23)
    .area([40, 60, 0, 100])
    .data_format("netcdf")
    .download_format("unarchived")
    .build()
)

request.execute()
```

This project gives access features like:
* Specifying ranges for days, months, years, etc. similar to python `range()` function.
* Builder format for creating request and `build()` method to build it.
* Access to api attributes (code-editor `auto-completion`)
* Validation for attributes, preventing invalid requests.