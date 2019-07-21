
import numpy as np
from Player import PlayerType, Player
from itertools import permutations

from TicTacToeState import State

from Utils import board_display


class BoardFieldCurrentValue:
    EMPTY = 0
    NAUGHT = 1
    CROSS = 2


class Board:

    def __init__(self, dim):
        self.BOARD_DIM = dim
        self.BOARD_SIZE = self.BOARD_DIM * self.BOARD_DIM
        self.currentBoardFields = np.zeros(self.BOARD_SIZE)
        self.naught_pos = []
        self.cross_pos = []

        self.currentBoardFields.fill(0)

    def play(self, player1: Player , player2: Player):
        self.naught_player = player1
        self.cross_player = player2

        self.naught_player.type = PlayerType.NAUGHT
        self.cross_player.type = PlayerType.CROSS

        x,y = 0,0
        isLegal, state = self.naught_player.play(self)
        board_display(self)
        nextPlayer = self.cross_player
        # print('state ', state)
        while(state == State.IN_PROGRESS):
            # print('calling play for next player ', nextPlayer.name, state)
            isLegal, state = nextPlayer.play(self)
            if( not isLegal):
                print('Invalid Pos, please try again')
                continue
            board_display(self)
            if(nextPlayer == self.naught_player):
                nextPlayer = self.cross_player
            else:
                nextPlayer = self.naught_player

            if state is State.CROSS_WIN:
                print(self.cross_player.name,' Won ')
            else:
                print(self.naught_player.name,' Won')

            if state is State.DRAW:
                print('It\'s a Draw')




    def coord_2d_to_1d(self, x: int, y: int) -> int:
        return self.BOARD_DIM * y + x

    def coord_1d_to_2d(self, pos: int) -> (int, int):
        x =  pos % self.BOARD_DIM
        y = (pos - x)/self.BOARD_DIM
        return x, y

    def getCurrSum(self, type: PlayerType):
        if type == PlayerType.CROSS:
            return np.sum(self.cross_pos)
        else:
            return np.sum(self.naught_pos)

    def board_contains(self, arr, win_arr) -> bool:

        for t in permutations(arr, self.BOARD_DIM):
            val = np.array_equal(win_arr, t)
            if(val):
                return True

        return False



    def check(self, arr):
        # print('check ',arr)
        for pos in arr:
            x,y = self.coord_1d_to_2d(pos)
            if self.isLeft(x,y)  :
                # print('left ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = (i + pos)
                    temp = np.append(temp, val)
                # print(' temp ',temp)
                ret = self.board_contains(arr, temp)
                if(ret):
                    return True
            if self.isRight(x,y) :
                # print('right ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = ( pos - i)
                    temp = np.append(temp, val)
                # print(' temp ', temp)
                ret = self.board_contains(arr, temp)
                if (ret):
                    return True
            if self.isTop(x,y) :
                # print('top ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = (pos + i * self.BOARD_DIM )
                    temp = np.append(temp, val)

                # print(' temp ', temp)
                ret = self.board_contains(  arr, temp)
                if (ret):
                    return True
            if self.isBottom(x,y) :
                # print('bottom ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = (pos - i * self.BOARD_DIM)
                    temp = np.append(temp, val)

                # print(' temp ', temp)
                ret = self.board_contains(arr, temp)
                if (ret):
                    return True


            # diagonal
            if self.isBottomLeftDiagonal(x, y):
                # print('bottomLeftDiagonal ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = (pos - i * (self.BOARD_DIM - 1))
                    temp = np.append(temp, val)

                # print(' temp ', temp)
                ret = self.board_contains(arr, temp)
                if (ret):
                    return True

            if self.isTopRightDiagonal(x, y):
                # print('topRightDiagonal ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = (pos + i * (self.BOARD_DIM - 1))
                    temp = np.append(temp, val)

                # print(' temp ', temp)
                ret = self.board_contains(arr, temp)
                if (ret):
                    return True

            if self.isBottomRightDiagonal(x, y):
                # print('BottomRightDiagonal ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = (pos - i * (self.BOARD_DIM + 1))
                    temp = np.append(temp, val)

                # print(' temp ', temp)
                ret = self.board_contains(arr, temp)
                if (ret):
                    return True

            if self.isTopLeftDiagonal(x, y):
                # print('TopLeftDiagonal ',x,y)
                temp = []
                for i in range(self.BOARD_DIM):
                    val = (pos + i * (self.BOARD_DIM + 1))
                    temp = np.append(temp, val)

                # print(' temp ', temp)
                ret = self.board_contains(arr, temp)
                if (ret):
                    return True

        return False


    def isLeft(self, x, y):
        if x == 0:
            return True
        return False

    def isRight(self, x, y):
        if x == self.BOARD_DIM - 1:
            return True
        return False

    def isTop(self, x, y):
        if y == 0:
            return True
        return False

    def isBottom(self, x, y):
        if y == self.BOARD_DIM - 1:
            return True
        return False

    def isBottomLeftDiagonal(self, x, y ):
        return self.isLeft(x,y) and self.isBottom(x,y)

    def isTopRightDiagonal(self, x, y):
        return self.isTop(x,y) and self.isRight(x,y)

    def isBottomRightDiagonal(self, x, y):
        return self.isRight(x,y) and self.isBottom(x,y)

    def isTopLeftDiagonal(self, x, y):
        return self.isLeft(x,y) and self.isTop(x,y)



    def check_win(self, type: PlayerType) -> bool:

        if(type == PlayerType.NAUGHT):
            return self.check(self.naught_pos)
        else:
            return self.check(self.cross_pos)





    def tohtml(self) -> str:
        data = self.state_to_char_list()
        html = '<table border="1"><tr>{}</tr></table>'.format('</tr><tr>'
            .join('<td>{}</td>'.format('</td><td>'
                                       .join(str(val) for val in row)) for row in data)
        )
        return html

    def state_to_char_list(self):
        res = []

        for i in range(self.BOARD_DIM):
            line = []
            for j in range(self.BOARD_DIM):
                line.append(self.state_to_char(i * self.BOARD_DIM + j))
            res.append(line)

        return res

    def state_to_char(self, pos: int):
        retval = '<pre> </pre>' #for empty html space

        if(self.currentBoardFields[pos] == BoardFieldCurrentValue.NAUGHT):
            retval = 'O'
        elif(self.currentBoardFields[pos] == BoardFieldCurrentValue.CROSS):
            retval = 'X'

        return retval

    def moveXY(self, x: int, y: int, type: PlayerType) -> (bool, State):
        pos = self.coord_2d_to_1d(x,y)
        return self.move(pos, type)

    def move(self, pos: int, type: PlayerType) -> (bool, State):
        state = State.IN_PROGRESS
        valid = False
        # print('pos ',pos)
        if(self.currentBoardFields[pos] != BoardFieldCurrentValue.EMPTY):
            return valid, state

        if(type == PlayerType.NAUGHT):
            self.naught_pos = np.append(self.naught_pos, pos)
            self.currentBoardFields[pos] = BoardFieldCurrentValue.NAUGHT
        else:
            self.cross_pos = np.append(self.cross_pos, pos)
            self.currentBoardFields[pos] = BoardFieldCurrentValue.CROSS
        # print('naught_pos ',self.naught_pos, ' cross_pos ', self.cross_pos)
        if( self.check_win(type)):
            if(type == BoardFieldCurrentValue.NAUGHT):
                state = State.NAUGHT_WIN
            else:
                state = State.CROSS_WIN
            # print('',type,' won')

        if(np.count_nonzero(self.currentBoardFields) == self.BOARD_SIZE):
            state = State.DRAW
            # print('DRAW')

        valid = True

        return valid, state




