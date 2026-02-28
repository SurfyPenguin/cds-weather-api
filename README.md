<center><h1>CDS API Request builder</h1></center>

## A wrapper around Copernicus Climate Data Store API library (cdsapi) to simplify request creation, using builder design pattern.

## Project Structure
```bash
cds-weather-api/
├── LICENSE
├── pyproject.toml
├── README.md
├── src
│   ├── CdsApi
│   │   ├── client_config.py
│   │   ├── exceptions.py
│   │   ├── helpers.py
│   │   ├── __init__.py
│   │   └── weather_api.py
│   └── examples
│       └── example.py
└── uv.lock
```
## Introduction

Normal way to make request in [cdsapi](https://pypi.org/project/cdsapi/):

*Dataset*: [Reanalysis ERA5 single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview)
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
Throughout the request one has to follow the same boiler-plate, especially with __years__, __months__, __days__ and __hours__.

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
## Issues with cdsapi 
* Can't provide months in integer:
```python
"month": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] # this will work
"month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # this will not work
"month": ["1", "2", "3", "4", "5", ...] # this will not work 
``` 
__There is no validation__ for these values and cdsapi will send requests like these to CDS easily but __no month__ would be actually selected in the request form.

It is fine with months as it has only 12 possible values. But with attributes like __days__ it becomes inconvenient especially when we want to request data-set for whole month, Its hard to imagine typing all that format for months or years.

* No way to provide ranges:

There is no way to provide ranges such as 1–12 (months), 1–15 (days) and 2000–2020 (years) and 2–3 as hours. (Side note: Yes, we used en dash)

With hours the parameters should be strictly in `HH:MM` format where `MM` is mostly `00`.
```python
"time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
] # no comments
```

# Using the script
We tried to organize request attributes, using builder-pattern which uses method-chaining to enable fluent interface.

## Getting API Credentials
Here is how to setup the CDS Api key: \
If you do not have an account yet, login/register to [CDS](https://cds.climate.copernicus.eu/).

Get api __url__ & __key__ from account settings.
* For linux: Save your credentials to the file `$HOME/.cdsapirc`
* For windows: Save your credentials to the file `%USERPROFILE%\.cdsapirc` or `C:\Users\YourUsername\.cdsapirc`
```
url: https://cds.climate.copernicus.eu/api
key: <PERSONAL-ACCESS-TOKEN>
```
Alternatively, create an `.env` file and setup config/client using `ClientConfig` class.

## Constructing request
1. Constructing request requires `RequestBuilder` class from `CdsApi` module.
```python
from CdsApi import RequestBuilder
```
2. Define required 'variables' in a variable for ease.
```python
variables = [
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "2m_dewpoint_temperature",
    "2m_temperature",
    "total_precipitation"
]
```
3. Define the request with `RequestBuilder()`
```python
request = RequestBuilder()
```
4. Try to access methods and use the ones required like this:
```python
# normal way
request = RequestBuilder() \
    .dataset("reanalysis-era5-single-levels") \
    .product_type(["reanalysis"]) \
    .variables(variables) \
    .build() \

# cleaner format to do the same thing
request = (
    RequestBuilder()
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .build() # build() to return constructed request
)
```
5. Your request needs some time-interval as well, here are the methods:
```python
request = (
    RequestBuilder()
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .year_range(2000, 2020) # all years from 2000–2020 (2020 included)
    .month_range(1, 12) # all months (12 included)
    .day_range(1, 31) # all days (31st included)
    .time_range(0, 23) # all hours (23:00 included)
    .build() # finally build request
)
```
* What if we want to set months for winter or consider night hours?

Its taken care of! months and hours are cyclic:
```python
request = (
    RequestBuilder()
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .year_range(2000, 2020)
    .month_range(9, 4) # sets Sep, Oct, Nov, Dec, Jan, Feb, Mar, April (winter season)
    .day_range(1, 31)
    .time_range(22, 3) # sets 22:00, 23:00, 00:00, 01:00, 02:00, 03:00
    .build()
)
```
__Note:__ Years and days are not cyclic for obvious reasons. Doing so will result in `ValidationError`.

* What if we want only specific years, months, days or hours?

That can be mentioned using the following methods:
```python
request = (
    RequestBuilder()
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .year(2024) # obvious
    .month(1, 3, 5) # Jan, Mar, May
    .day(1, 22, 31)
    .time(19, 20, 1, 3) # 19:00, 20:00, 01:00, 03:00
    .build()
)
```
6. Finally set `data format` and `download format`.
```python
request = (
    RequestBuilder()
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .year(2024)
    .month_range(1, 8)
    .day_range(1, 31)
    .time_range(0, 12)
    .data_format("netcdf") # netcdf or grib
    .download_format("unarchived") # zip or unarchived
    .build() # build and get WeatherApi object
)
```
7. Make request using `request.execute()`.
```python
request = (
    RequestBuilder()
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .year(2024)
    .month_range(1, 8)
    .day_range(1, 31)
    .time_range(0, 12)
    .data_format("netcdf") # netcdf or grib
    .download_format("unarchived") # zip or unarchived
    .build() # build and get WeatherApi object
)

request.execute() # make request
```

8. Difference:
* With cdsapi:
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
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
```

* With our cdsapi wrapper:
```python
from CdsApi import RequestBuilder

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
    .year(2024)
    .month_range(1, 8)
    .day_range(1, 31)
    .time_range(0, 12)
    .data_format("netcdf")
    .download_format("unarchived")
    .build()
)

request.execute()
```
Its easily configurable!

## Creating Configs
"Configs" or Clients are basically extension of already available `cdsapi.Client` class in cdsapi. The wrapper class `ClientConfig` is more helpful for developers and IDEs than it is for a normal user, as it provides type-checking and few validations before the final request is returned by `RequestBuilder`.

* Creating a config:
```python
from CdsApi import ClientConfig as client
url = <api url> # not recommended to store api credentials directly
key = <api key> # just for representation

config = client.config(url=url, key=key)
```
Usually API key and url is stored in `.env` file:
```python
from CdsApi import ClientConfig as client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.environ.get("API_URL")
key = os.environ.get("API_KEY")

config = client.config(url=url, key=key)
```
Again, you can __skip these steps__ by creating `.cdsapirc` file. 

* Using configs in `RequestBuilder`:
```python
from CdsApi import ClientConfig as client
from CdsApi import RequestBuilder
... # api key & url retrieval

config = client.config(url=url, key=key)

variables = [
    ... # variables
]

request = (
    RequestBuilder()
    .client(config) # pass the config/client
    .dataset("reanalysis-era5-single-levels")
    .product_type(["reanalysis"])
    .variables(variables)
    .year(2024)
    .month_range(1, 8)
    .day_range(1, 31)
    .time_range(0, 12)
    .data_format("netcdf")
    .download_format("unarchived")
    .build()
)

request.execute()
```
A config with explicit API __credentials will override__ the credentials in `.cdsapi` for that specific request.

* Multiple configs:
Not that important but we can create multiple configs for multiple api credentials or for debugging.
```python
from CdsApi import ClientConfig as client

# multiple keys
api_key_1 = client.config(url=url, key=key_1)
api_key_2 = client.config(url=url, key=key_2)

# multiple profiles
debug_config = client.config(debug=True, retry_max=10)
quiet_config = client.config(quiet=True, sleep_max=20) # avoid announcements in terminal

# combined
combined_config = client.config(
    quiet=True,
    timeout=240,
    wait_until_complete=False,
    retry_max=20,
    sleep_max=120,
)
```
At the end of the day, This method only returns an instance of `cdsapi.Client()`, so you are free to use whichever method you want, and pass that config to `RequestBuilder` and it will still work.

## Installation & Updates

### Using git
Use the following command to get latest Release:
```bash
pip install git+https://github.com/SurfyPenguin/cds-weather-api.git

# using uv
uv add git+https://github.com/SurfyPenguin/cds-weather-api.git
```

### Installing wheels
1. Download latest wheels from [Releases](https://github.com/SurfyPenguin/cds-weather-api/releases/latest)
2. Install it in your environment:
```bash
pip install cds_weather_api-1.0.0-py3-none-any.whl

# or with uv
uv pip install cds_weather_api-1.0.0-py3-none-any.whl
```

### Update to latest version
Update to new release
```bash
pip install --upgrade git+https://github.com/SurfyPenguin/cds-weather-api.git

# or with uv
uv add git+https://github.com/SurfyPenguin/cds-weather-api.git
```
# Development & Testing
Project uses [uv standalone](https://docs.astral.sh/uv/getting-started/installation/) for management.

All the tests are based on `pytest` & `pytest-mock`, and very few unit tests are present for now.

## Getting started
* Clone repository
```bash
git clone https://github.com/SurfyPenguin/cds-weather-api.git
```
* Install dependencies
```bash
uv sync
```
## Testing
* Install `CdsApi` as editable package
```bash
uv pip install -e .
```
Doing so allows us to perform tests using `pytest`.
* Run tests
```bash
uv run pytest

# verbose
uv run pytest -v
```

# License
This project is licensed under the MIT License.
