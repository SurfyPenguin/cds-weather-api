from datetime import datetime
from exceptions import ValidationError

FIRST_MONTH: int = 1
LAST_MONTH: int = 12

ERA5_START_YEAR: int = 1939 # datasets in CDS are available from 1939 
ERA5_CURRENT_YEAR: int = datetime.now().year # maximum year would be current year

FIRST_DAY: int = 1
LAST_DAY: int = 31 # 30 or 31, managed by cdsapi

EN_DASH = "–" # proper typography for ranges

class CDSFormatter:

    @staticmethod
    def year_range(start: int, stop: int) -> list[str]:
        """Creates a range of valid years using start and stop (inclusive) values.

        This method is helpful for defining year ranges and prevents the need for passing numeric-strings manually.
        Using this method for large ranges might increase the request size significantly, especially when variables 
        are too many, therefore request gets rejected.

        Args:
            start (int): The starting year of the sequence.
            stop (int): The ending year of the sequence (inclusive).

        Raises:
            ValidationError: Raised when start value is greater than stop value.
            ValidationError: Raised when provided start or stop value is negative.
            ValidationError: Raised when start or stop values are not in the years for which datasets are available in CDS.

        Returns:
            list[str]: A list of years in numeric-string.
        """
        # validate
        if start > stop:
            raise ValidationError(f"Start year ({start}) can't be greater than stop year ({stop}).")

        if start < 0 or stop < 0:
            raise ValidationError("Years can't be negative or zero.")
        
        # CDS datasets start from the year 1939
        if not (ERA5_START_YEAR <= start <= stop <= ERA5_CURRENT_YEAR):
            raise ValidationError(f"Years must be between {ERA5_START_YEAR}{EN_DASH}{ERA5_CURRENT_YEAR}.")
        
        return [str(year) for year in range(start, stop + 1)]

    @staticmethod
    def month_range(start: int, stop: int) -> list[str]:
        """Creates a range of valid months using start and stop (inclusive) values.

        This method is helpful for defining range of months (in the format required by CDS api).
        Months are cyclic i.e. values like (9, 4) will return a list of months from September
        to April.

        Args:
            start (int): The starting month of the sequence (1 for Jan, 2 for Feb, ...).
            stop (int): The ending month of the sequence (inclusive).

        Raises:
            ValidationError: Raised when provided start or stop value is negative.
            ValidationError: Raised when provided start or stop value is greater than 12.

        Returns:
            list[str]: A list of months in numeric-string.
        """
        # validate
        if start <= 0 or stop <= 0:
            raise ValidationError("Months can't be negative or zero.")
        
        # max value for month is 12
        if start > LAST_MONTH or stop > LAST_MONTH:
            raise ValidationError(f"Months must be between {FIRST_MONTH}{EN_DASH}{LAST_MONTH}.")

        if start <= stop:
            months = list(range(start, stop + 1))
        else:
            # allow months to cycle
            months = list(range(start, 13)) + list(range(1, stop + 1))
        
        return [f"{month:02d}" for month in months]
    
    @staticmethod
    def day_range(start: int, stop: int) -> list[str]:
        """Creates a range of valid days using start and stop (inclusive) values.

        This method is helpful for defining range of days (in the format required by CDS api).

        Args:
            start (int): The starting day of the sequence.
            stop (int): The ending day of the sequence.

        Raises:
            ValidationError: Raised when start value is greater than stop value.
            ValidationError: Raised when provided start or stop value is negative.
            ValidationError: Raised when start or stop values are not between valid month range (1–31).

        Returns:
            list[str]: A list of days in numeric-string.
        """
        # validate
        if start > stop:
            raise ValidationError(f"Start day ({start}) can't be greater than stop day ({stop}).")

        if start <= 0 or stop <= 0:
            raise ValidationError("Days can't be negative or zero.")
        
        # last day is 31
        if start > LAST_DAY or stop > LAST_DAY:
            raise ValidationError(f"Days must be between {FIRST_DAY}{EN_DASH}{LAST_DAY}.")
        
        return [f"{day:02d}" for day in range(start, stop + 1)]
