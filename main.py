from WeatherApi import RequestBuilder

request = (
    RequestBuilder()
    .year(["2024"])
    .month(["05", "06", "07", "08"])
    .build()
)

request.execute()