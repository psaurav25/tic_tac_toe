from Player import Player
from TicTacToeState import State


class HumanPlayer(Player):

    def move(self, x, y, board) -> bool:
        board.moveXY(x,y, self.type)


    def play(self, board) -> (bool, State):
        read = True
        while read:
            try:
                x,y = input('Enter co-ordinates for \''+self.type+"\' : ").split()
                read = False
            except KeyboardInterrupt as ke:
                read = False
            except Exception as e:
                print('Invalid format, please input again :: ',e)


        x = int(x)
        y = int(y)
        # print('x,y ', x,y)
        return board.moveXY(x,y,self.type)