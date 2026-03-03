from CdsApi.weather_api import RequestBuilder

class TestRequestBuilder:
    
    def test_builder_minimal(self):
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
            .product_type("reanalysis")
            .variables(variables)
            .year(2024)
            .month_range(1, 8)
            .day_range(1, 8)
            .time_range(0, 12)
            .area((40, 60, 0, 100))
            .data_format("netcdf")
            .download_format("unarchived")
            .build()
        )
        d = request.get_request_dict()
        assert getattr(request, "dataset", None) == "reanalysis-era5-single-levels"

        assert d["product_type"] == ["reanalysis"]
        assert d["variable"] == variables
        assert d["year"] == ["2024"]
        assert d["month"] == ["01", "02", "03", "04", "05", "06", "07", "08"]
        assert d["day"] == ["01", "02", "03", "04", "05", "06", "07", "08"]
        assert d["time"] == ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00"]
        assert d["area"] == (40, 60, 0, 100)
        assert d["data_format"] == "netcdf"
        assert d["download_format"] == "unarchived"