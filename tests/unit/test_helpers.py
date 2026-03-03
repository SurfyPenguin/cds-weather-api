from CdsApi.helpers import CDSFormatter
from CdsApi.exceptions import ValidationError
import pytest

# test formatters
class TestHelpers:
    def test_format_to_year_list(self):
        result = CDSFormatter.format_to_year_list([1999, 2012, 2015, 2019, 2024])
        assert result == ["1999", "2012", "2015", "2019", '2024']

    def test_format_to_month_list(self):
        result = CDSFormatter.format_to_month_list([1, 2, 3, 4, 5, 12])
        assert result == ["01", "02", "03", "04", "05", "12"]

    def test_format_to_day_list(self):

        input_days = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
        ]
        output_days = [
            "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"
        ]

        result = CDSFormatter.format_to_day_list(input_days)
        assert result == output_days

    def test_format_to_hour_list(self):
        input_hours = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23
        ]
        output_hours = [
            "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00",
            "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
        ]

        result = CDSFormatter.format_to_hour_list(input_hours)
        assert result == output_hours

    # test range generators
    def test_year_range(self):
        result = CDSFormatter.year_range(start=1999, stop=2024)
        assert result == [
            '1999', '2000',
            '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
            '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020',
            '2021', '2022', '2023', '2024'
        ]

    # month range tests
    def test_month_range_normal(self):
        result = CDSFormatter.month_range(start=1, stop=12)
        assert result == ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    def test_month_range_cyclic(self):
        result = CDSFormatter.month_range(start=6, stop=5)
        assert result == ["06", "07", "08", "09", "10", "11", "12", "01", "02", "03", "04", "05"]

    def test_day_range(self):
        result = CDSFormatter.day_range(start=1, stop=31)
        assert result == [
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
            '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'
        ]

    def test_time_range(self):
        result = CDSFormatter.time_range(start=0, stop=23)
        assert result == [
            '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
            '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
        ]

class TestHelpersExceptions:

    INVALID_YEAR_RANGES = [
        (-1999, 2000), (2000, -2020), # negative values
        (1955, 1940), (2020, 2019), # start > stop
        (1900, 2000), (1930, 1940), # out of year range
        (2020, 2020), # empty list
    ]
    INVALID_DAY_RANGES = [
        (-1, 30), (1, -20), # negative values
        (12, 1), (30, 29), # start > stop
        (0, 12), (1, 33), (33, 55), # out of day range
        (5, 5), # empty list
    ]

    INVALID_MONTH_RANGES = [
        (-1, 9), (1, -9), # negative values
        (0, 12), (9, 22), # out of month range
        (5, 5), # empty list
    ]
    INVALID_TIME_RANGES = [
        (-2, 4), (4, -9), # negative values
        (0, 24), (28, 6), # out of hour range
        (5, 5), # empty list
    ]

    @pytest.mark.parametrize("start, stop", INVALID_YEAR_RANGES)
    def test_year_range_invalid(self, start: int, stop: int):
        with pytest.raises(ValidationError):
            CDSFormatter.year_range(start, stop)

    @pytest.mark.parametrize("start, stop", INVALID_MONTH_RANGES)
    def test_month_range_invalid(self, start: int, stop: int):
        with pytest.raises(ValidationError):
            CDSFormatter.month_range(start, stop)

    @pytest.mark.parametrize("start, stop", INVALID_DAY_RANGES)
    def test_day_range_invalid(self, start: int, stop: int):
        with pytest.raises(ValidationError):
            CDSFormatter.day_range(start, stop)

    @pytest.mark.parametrize("start, stop", INVALID_TIME_RANGES)
    def test_time_range_invalid(self, start: int, stop: int):
        with pytest.raises(ValidationError):
            CDSFormatter.time_range(start, stop)