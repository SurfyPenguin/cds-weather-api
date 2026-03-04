from CdsApi.validators import Validators
import pytest

class TestValidators:
    @pytest.mark.parametrize("data, types", [
        (["10m_u_component_of_wind", "10m_v_component_of_wind"], str), # check string
        ([2021, 2022, 2023], int), # check int
        ([1.4, 5, 9, 4.2], (int, float)), # check multiple types
        (("10m_u_component_of_wind", "10m_v_component_of_wind"), str), # test tuples
    ])
    def test_list_of_type(self, data, types):
        """Test that valid lists and tuples pass without any exception."""
        Validators.list_of_type(data, types=types)