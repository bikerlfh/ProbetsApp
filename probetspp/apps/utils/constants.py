from os import getenv


DECIMAL_PLACES = int(getenv('DECIMAL_PLACES', 2))
DELIMITER_CSV = getenv('DELIMITER_CSV', ';')
