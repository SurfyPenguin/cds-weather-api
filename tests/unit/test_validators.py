from CdsApi.exceptions import *
from CdsApi.validators import Validators
import pytest

class TestValidators:

    INVALID_INPUTS = [
        [(), int], # empty tuple
        [[], int], # empty list

        [["10m_u_component_of_wind", 2, 3, 4], int],
        [["10m_u_component_of_wind", 2, 3, 4], float],
        [["10m_u_component_of_wind", 2, 3, 4], str],
        [["10m_u_component_of_wind", 2, 3, 4.0], (int, str)],
        [[1, 2, 3, 4], float],
        [[0.22, 5.89, 3.45, 1.12], int],
    ]

    @pytest.mark.parametrize("data, types", [
        (["10m_u_component_of_wind", "10m_v_component_of_wind"], str), # check string
        ([2021, 2022, 2023], int), # check int
        ([1.4, 5, 9, 4.2], (int, float)), # check multiple types
        (("10m_u_component_of_wind", "10m_v_component_of_wind"), str), # test tuples
    ])
    def test_list_of_type(self, data, types):
        """Test that valid lists and tuples pass without any exception."""
        Validators.list_of_type(data, types=types)

    @pytest.mark.parametrize("data, types", INVALID_INPUTS)
    def test_list_of_type_invalid(self, data, types):
        """Test that exceptions are raised for a set of invalid values."""
        with pytest.raises(ValidationError):
            Validators.list_of_type(data, types)

    @pytest.mark.parametrize("years", [
        [1, 5, 9, 12, 33],
        [33, 35, 12, -1],
        [-1, -4, -6, -9]
    ])
    def test_years(self, years):
        """Test that exceptions are raised for a set of invalid years-list."""
        with pytest.raises(ValidationError):
            Validators.years(years)

    @pytest.mark.parametrize("months", [
        [1, 5, 9, 12, 33],
        [33, 35, 12, -1],
        [-1, -4, -6, -9]
    ])
    def test_months(self, months):
        """Test that exceptions are raised for a set of invalid months-list."""
        with pytest.raises(ValidationError):
            Validators.months(months)

    @pytest.mark.parametrize("days", [
        [1, 5, 9, 12, 33],
        [33, 35, 12, -1],
        [-1, -4, -6, -9]
    ])
    def test_days(self, days):
        """Test that exceptions are raised for a set of invalid days-list."""
        with pytest.raises(ValidationError):
            Validators.days(days)

    @pytest.mark.parametrize("hours", [
        [1, 5, 9, 12, 33],
        [33, 35, 12, -1],
        [-1, -4, -6, -9]
    ])
    def test_hours(self, hours):
        """Test that exceptions are raised for a set of invalid hours-list."""
        with pytest.raises(ValidationError):
            Validators.hours(hours)

    @pytest.mark.parametrize("bbox", [
        [20, 8, 90, 80], # top-edge, lies below bottom-edge
        [60, 80, 40, 20], # left-edge, lies to the right of right-edge
        [-66, 24, -91, 50], # bottom-edge not within (-90, 90)
        [180, 24, -88, 6], # top-edge not within (-90, 90)
        [60, 190, 40, 80], # left-edge not within (-180, 180)
        [60, 90, 40, -190], # right-edge not within (-180, 180)
    ])
    def test_bounding_box(self, bbox):
        """Test that exceptions are raised for a set of invalid BoundingBox tuples."""
        with pytest.raises((ValidationError, LatitudeError, LongitudeError)):
            Validators.bounding_box(bbox)