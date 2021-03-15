from os import getenv


DIR = 'tmp'
SUBDIR = 'probetspp'

DECIMAL_PLACES = int(getenv('DECIMAL_PLACES', 2))
DELIMITER_CSV = getenv('DELIMITER_CSV', ';')

BUCKET_FILES = getenv('BUCKET_FILES')

ENVIRONMENT = getenv('ENVIRONMENT', 'alpha')
