ParameterList = list[str]
"""
Representation for list which contains string parameters.

Example:

    product_type = ['reanalysis']
    day = ["01", "02", "03", ..., "12"]
    month = ["01", "02", ..., "30"]
"""

BoundingBox = tuple[float, float, float, float]
"""
Represents a geographical area as a list of four coordinates.

Format:

    (North, West, South, East)

Example:

    (90, -120, -90, 180)
"""