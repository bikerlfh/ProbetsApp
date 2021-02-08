from enum import IntEnum


class GameStatus(IntEnum):
    DEFAULT = -1
    SCHEDULED = 1
    IN_LIVE = 2
    FINISHED = 3
    CANCELED = 4
    ABANDONMENT = 5
    DISCONTINUED = 6
    POSTPONED = 7
