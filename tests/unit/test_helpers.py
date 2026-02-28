from CdsApi.helpers import CDSFormatter

# test formatters
def test_format_to_year_list():
    result = CDSFormatter.format_to_year_list([1999, 2012, 2015, 2019, 2024])
    assert result == ["1999", "2012", "2015", "2019", '2024']

def test_format_to_month_list():
    result = CDSFormatter.format_to_month_list([1, 2, 3, 4, 5, 12])
    assert result == ["01", "02", "03", "04", "05", "12"]

def test_format_to_day_list():

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

def test_format_to_hour_list():
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