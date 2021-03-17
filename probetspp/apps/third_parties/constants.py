from os import getenv


USE_CHROMELESS = bool(int(getenv('USE_CHROMELESS', '0')))
