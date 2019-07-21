from enum import Enum

class State(Enum):
    IN_PROGRESS = 0
    DRAW = 1
    NAUGHT_WIN = 2
    CROSS_WIN = 3