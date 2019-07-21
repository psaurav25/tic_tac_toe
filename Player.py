from abc import abstractmethod

from TicTacToeState import State


class PlayerType:
    NAUGHT = "O"
    CROSS = "X"
    NONE = "NA"

class Player:
    def __init__(self,name:str):
        self.name = name
        self.type = PlayerType.NONE

    @abstractmethod
    def move(self, x, y, board) -> bool:
        pass

    @abstractmethod
    def play(self, board) -> (bool, State):
        pass
