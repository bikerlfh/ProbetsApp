from os import getenv
import pathlib
import platform


_main_path = pathlib.Path().absolute()
DIR = 'tmp'
SUBDIR = 'probetspp'

DECIMAL_PLACES = int(getenv('DECIMAL_PLACES', 2))
DELIMITER_CSV = getenv('DELIMITER_CSV', ';')

DRIVER_PATH = getenv(
    'DRIVER_PATH',
    '/usr/bin/chromedriver'
)


BUCKET_FILES = getenv('BUCKET_FILES')
