from decimal import Decimal, ROUND_FLOOR
from typing import Optional

from apps.utils.constants import DECIMAL_PLACES


def format_decimal_to_n_places(
    *,
    value: Decimal,
    decimal_places: Optional[int] = None
) -> Decimal:
    """ Format a Decimal object to desired decimal places.
    Args:
        value: A Decimal object.
        decimal_places: An int representing the desired decimal places.
    Returns:
        A Decimal object with the desired decimal places
    """
    if decimal_places is None:
        decimal_places = DECIMAL_PLACES

    if not isinstance(value, Decimal):
        value = Decimal(value)
    assert isinstance(decimal_places, int), (
        'decimal_places must be a int instance'
    )

    decimal_places -= 1
    decimal_places = '.{}1'.format('0' * decimal_places)

    return Decimal(
        value.quantize(Decimal(decimal_places), rounding=ROUND_FLOOR)
    )
