from typing import Union
from .exceptions import BuildError, ValidationError
from .weather_api import WeatherApi

class Validators:

    @staticmethod
    def list_of_type(data: any, types: Union[type, tuple[type, ...]]) -> None:
        """Validation for list of provided type(s)

        Checks if all the elements in a list are of the provided type(s) or not.

        Args:
            data (any): Data to be validated.
            types (type | tuple[type, ...]): Type(s) to be checked.

        Raises:
            ValidationError: Provided list/tuple is empty.
            ValidationError: Provided data is not list/tuple.
            ValidationError: If any type mismatch is found.
        """
        # using all() with empty list would return "True"
        # explicit check for empty list/tuple
        if not data:
            raise ValidationError("Provided list/tuple can't be empty.")

        if not isinstance(data, (list, tuple)):
            raise ValidationError(f"Provided data must be 'list' or 'tuple'.")
        
        if not all(isinstance(item, types) for item in data):
            raise ValidationError(f"The list/tuple must contain these types only: {types}")
        
    @staticmethod
    def build_request_parameters(request: WeatherApi) -> None:
        """Validation for request parameters in a particular `WeatherApi` request instance.

        Validates api payload parameters for not-set (None) values.
 
        Args:
            request (WeatherApi): `WeatherApi` request instance.

        Raises:
            BuildError: When `dataset` parameter is not set.
            BuildError: When non-optional parameters are not set.
        """
        request_dict = request.get_request_dict()

        # validate non api payload parameters
        if request.dataset is None:
            raise BuildError("Required field 'dataset' is not set.")
        
        # validate api payload parameters
        for key, value in request_dict.items():
            if key not in request.optional and value is None:
                raise BuildError(f"Required field '{key}' is not set.")
