import pathlib
from enum import Enum


_main_path = pathlib.Path().absolute()

TABLE_TENNIS_TODAY_URL = 'https://www.flashscore.co/tenis-de-mesa/'
FOLDER_PATH_FLASH_DATA = f'{_main_path}/info_pages/flash/'
FILE_PATH_DATA_SET = f'{_main_path}/datasets/%Y%m%d.csv'
FILENAME_FORMAT_FLASH_DATA = '%d%m%Y.html'


class TableTennisStatus(Enum):
    FINISHED = 'Finalizado'
    CANCELED = 'Anulado'
    IN_LIVE = 'Set'
    ABANDONMENT = 'Abandono'


class GenderLeague(Enum):
    MALE = 'MASCULINO'
    FEMALE = 'FEMENINO'
