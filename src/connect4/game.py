from enum import Enum, auto
import numpy as np
from typing import Self, List
import copy 

NUMBER_OF_ROWS = 6
NUMBER_OF_COLUMNS = 7 
RECQUIRED_ALIGNED_PAWNS_TO_WIN = 4


class Color(Enum):
    EMPTY = 0
    YELLOW = auto()
    RED = auto()

    
class GameState:

    def __init__(self: Self, board: np.ndarray = None, player_turn: Color = None) -> None:
        self.board = board
        self.player_turn = player_turn

    def initialize(self: Self) -> Self:
        self.board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY)
        self.player_turn = Color.YELLOW
        return self

    def switch_player_turn(self: Self) -> Self:
        self.player_turn = Color.RED if self.player_turn == Color.YELLOW else Color.YELLOW
        return self

    def get_position_of_highest_pawn(self: Self, column: int) -> int:
        assert 0 <= column < NUMBER_OF_COLUMNS
        if np.all(self.board[:, column] == Color.EMPTY):
            return NUMBER_OF_ROWS # convention: if no pawn in a column, lowest pawn is "in the ground"
        else:
            return np.where(self.board[:, column] != Color.EMPTY)[0][0]
    
    def play(self: Self, column: int, player_turn: Color) -> Self:
        assert 0 <= column < NUMBER_OF_COLUMNS
        assert player_turn == self.player_turn
        position_of_highest_pawn = self.get_position_of_highest_pawn(column)
        assert 0 < position_of_highest_pawn 
        self.board[position_of_highest_pawn-1][column] = player_turn
        self.switch_player_turn()
        return self
    
    def check_horizontal_victory(self: Self, i: int, j: int, player: Color): #(moving to the right)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if j+k > NUMBER_OF_COLUMNS-1: # reached end of the board 
                return False
            if self.board[i][j+k] != player: # found a different color than player's color
                return False
        return True

    def check_vertical_victory(self: Self, i: int, j: int, player: Color): # (moving to the top)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i-k < 0: # reached end of the board 
                return False
            if self.board[i-k][j] != player: # found a different color than player's color
                return False
        return True

    def check_diagonal_victory(self: Self, i: int, j: int, player: Color): # (moving to the top/right)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i-k > NUMBER_OF_ROWS-1 or j+k > NUMBER_OF_COLUMNS-1: # reached end of the board
                return False
            if self.board[i-k][j+k] != player: # found a different color than player's color
                return False
        return True
    
    def check_victory(self: Self, player: Color) -> Self:
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLUMNS):
                horizontal_victory = self.check_horizontal_victory(i, j, player)
                vertical_victory = self.check_vertical_victory(i, j, player)
                diagonal_victory = self.check_diagonal_victory(i, j, player)
                if horizontal_victory or vertical_victory or diagonal_victory:
                    return True
        return False


class Game:

    def __init__(self: Self, game_states: List[GameState] = []) -> None:
        self.game_states = game_states

    def play(self: Self, column: int, player_turn: Color) -> Self:
        last_game_state = self.game_states[-1]
        assert len(last_game_state) > 1
        last_game_state = copy.deepcopy(last_game_state)
        last_game_state.play(column, player_turn)
        self.game_states.append(last_game_state)
        return self