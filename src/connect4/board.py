from enum import Enum, auto
import numpy as np
from typing import Self

NUMBER_OF_ROWS = 6
NUMBER_OF_COLUMNS = 7 
RECQUIRED_ALIGNED_PAWNS_TO_WIN = 4


class Color(Enum):
    RED = auto()
    YELLOW = auto()
    EMPTY = auto()

class Game:

    def __init__(self: Self, board: np.array, player_turn: Color) -> Self:
        self.board = board
        self.player_turn = player_turn

    @staticmethod
    def initialize_board() -> Self:
        return Game(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW)
    
    def switch_player_turn(self: Self) -> Self:
        match self.player_turn :
            case Color.YELLOW:
                self.player_turn = Color.RED
            case Color.RED:
                self.player_turn = Color.YELLOW
            case _:
                raise ValueError()
        return self
    
    def get_position_of_highest_pawn(self: Self, column: int) -> int:
        assert 0 <= column < NUMBER_OF_COLUMNS
        return np.where(self.board[:, column] != Color.EMPTY)[0][0]
    
    def play(self: Self, column: int, player_color: Color) -> Self:
        assert 0 <= column < NUMBER_OF_COLUMNS
        assert player_color == self.player_turn
        position_of_highest_pawn = self.get_position_of_highest_pawn(column)
        assert 0 < position_of_highest_pawn 
        self.board[position_of_highest_pawn-1][column] = player_color
        self.switch_player_turn()
        return self
    
    def check_horizontal_victory(self: Self, i: int, j: int, player_color):
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if j+k > NUMBER_OF_COLUMNS-1: # reached end of the board
                return False
            if self.board[i][j+k] != player_color: # found a different color than player's color
                return False
        return True

    def check_vertical_victory(self: Self, i: int, j: int, player_color):
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i+k > NUMBER_OF_ROWS-1: # reached end of the board
                return False
            if self.board[i+k][j] != player_color: # found a different color than player's color
                return False
        return True

    def check_diagonal_victory(self: Self, i: int, j: int, player_color):
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i+k > NUMBER_OF_ROWS-1 or j+k > NUMBER_OF_COLUMNS-1: # reached end of the board
                return False
            if self.board[i+k][j+k] != player_color: # found a different color than player's color
                return False
        return True
    
    def check_victory(self: Self, player_color: Color) -> Self:
        assert player_color in {Color.RED, Color.YELLOW}
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLUMNS):
                horizontal_victory = self.check_horizontal_victory(i, j)
                vertical_victory = self.check_vertical_victory(i, j)
                diagonal_victory = self.check_diagonal_victory(i, j)
                if horizontal_victory or vertical_victory or diagonal_victory:
                    return True
        return False



        