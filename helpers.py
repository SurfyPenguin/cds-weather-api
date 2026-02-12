from datetime import datetime
from exceptions import ValidationError

FIRST_MONTH: int = 1
LAST_MONTH: int = 12

ERA5_START_YEAR: int = 1939 # datasets in CDS are available from 1939 
ERA5_CURRENT_YEAR: int = datetime.now().year # maximum year would be current year

EN_DASH = "–" # proper typography for ranges

class CDSFormatter:

    @staticmethod
    def year_range(start: int, stop: int):
        # validate
        if start > stop:
            raise ValidationError(f"Start year ({start}) can't be greater than stop ({stop}) year")

        if start < 0 or stop < 0:
            raise ValidationError("Years can't be negative or zero.")
        
        # CDS datasets start from the year 1939
        if not (ERA5_START_YEAR <= start <= stop <= ERA5_CURRENT_YEAR):
            raise ValidationError(f"Years must be between {ERA5_START_YEAR}{EN_DASH}{ERA5_CURRENT_YEAR}.")
        
        return [str(year) for year in range(start, stop + 1)]

    @staticmethod
    def month_range(start: int, stop: int) -> list[str]:
        # validate
        if start <= 0 or stop <= 0:
            raise ValidationError("Months can't be negative or zero.")
        
        # max value for month is 12
        if start > LAST_MONTH or stop > LAST_MONTH:
            raise ValidationError(f"Months must be between {FIRST_MONTH}{EN_DASH}{LAST_MONTH}")

        if start <= stop:
            months = list(range(start, stop + 1))
        else:
            # allow months to cycle
            months = list(range(start, 13)) + list(range(1, stop + 1))
        
        return [str(month).zfill(2) for month in months]
