from os import getenv

import pathlib


_main_path = pathlib.Path().absolute()
DIR = 'tmp'
SUBDIR = 'probetspp'

DECIMAL_PLACES = int(getenv('DECIMAL_PLACES', 2))
DELIMITER_CSV = getenv('DELIMITER_CSV', ';')

BUCKET_FILES = getenv('BUCKET_FILES')
