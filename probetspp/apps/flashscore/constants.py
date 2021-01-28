from enum import Enum
import pathlib

TABLE_TENNIS_TODAY_URL = 'https://www.flashscore.co/tenis-de-mesa/'


FOLDER_PATH_FLASH_DATA = f'{pathlib.Path().absolute()}/info_pages/flash/'
FILENAME_FORMAT_FLASH_DATA = '%d%m%Y.html'


class TableTennisStatus(Enum):
    FINISHED = 'Finalizado'
    CANCELED = 'Anulado'
    IN_LIVE = 'Set'
    ABANDONMENT = 'Abandono'


class GenderLeague(Enum):
    MALE = 'MASCULINO'
    FEMALE = 'FEMENINO'
