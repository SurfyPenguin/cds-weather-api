from typing import Union
from .exceptions import ValidationError

class Validators:

    @staticmethod
    def list_of_type(data: any, types: Union[type, tuple[type, ...]]) -> None:
        """Validation for list of provided type(s)

        Checks if all the elements in a list are of the provided type(s) or not.

        Args:
            data (any): Data to be validated.
            types (type | tuple[type, ...]): Type(s) to be checked.

        Raises:
            ValidationError: If any type mismatch is found.
        """
        # using all() with empty list would return "True"
        # explicit check for empty list/tuple
        if not data:
            raise ValidationError("Provided list/typle can't be empty.")

        if not isinstance(data, (list, tuple)):
            raise ValidationError(f"Provided data must be 'list' or 'tuple'.")
        
        if not all(isinstance(item, types) for item in data):
            raise ValidationError(f"The list/tuple must conatain these types only: {types}")
