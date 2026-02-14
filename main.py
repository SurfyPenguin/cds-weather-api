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
    .area([40, 60, 0, 100])
    .time_range(0, 12)
    .data_format("netcdf")
    .download_format("unarchived")
    .build()
)

request.execute()