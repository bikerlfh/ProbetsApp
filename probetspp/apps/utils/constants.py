from os import getenv
import pathlib
import platform


_main_path = pathlib.Path().absolute()

DECIMAL_PLACES = int(getenv('DECIMAL_PLACES', 2))
DELIMITER_CSV = getenv('DELIMITER_CSV', ';')

DRIVER_PATH = f'{_main_path}/probetspp/web_drivers' \
              f'/{platform.system()}/chromedriver'
