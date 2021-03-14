from os import getenv
import pathlib
from enum import Enum


FILES_PATH = getenv('FILES_PATH', pathlib.Path().absolute())

TABLE_TENNIS_TODAY_URL = 'https://www.flashscore.co/tenis-de-mesa/'
FOLDER_PATH_FLASH_DATA = f'{FILES_PATH}/info_pages/flash/'
FILE_PATH_DATA_SET = f'{FILES_PATH}/datasets/%Y%m%d.csv'
FILENAME_FORMAT_FLASH_DATA = '%Y%m%d.html'


class TableTennisStatus(Enum):
    FINISHED = 'Finalizado'
    CANCELED = 'Anulado'
    IN_LIVE = 'Set'
    ABANDONMENT = 'Abandono'
    DISCONTINUED = 'Suspendido'
    FOR_LOST = 'Por perdido'
    POSTPONED = 'Aplazado'


class GenderLeague(Enum):
    MALE = 'MASCULINO'
    FEMALE = 'FEMENINO'
