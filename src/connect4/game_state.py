from enum import Enum, auto
import numpy as np
from typing import Self, List
import copy 
import random

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
    
    def play(self: Self, column: int) -> Self:
        assert 0 <= column < NUMBER_OF_COLUMNS
        position_of_highest_pawn = self.get_position_of_highest_pawn(column)
        assert 0 < position_of_highest_pawn 
        self.board[position_of_highest_pawn-1][column] = self.player_turn
        self.switch_player_turn()
        return self
    
    def check_horizontal_victory(self: Self, i: int, j: int, player: Color) -> bool: #(moving to the right)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if j+k > NUMBER_OF_COLUMNS-1: # reached end of the board 
                return False
            if self.board[i][j+k] != player: # found a different color than player's color
                return False
        return True

    def check_vertical_victory(self: Self, i: int, j: int, player: Color) -> bool: # (moving to the top)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i-k < 0: # reached end of the board 
                return False
            if self.board[i-k][j] != player: # found a different color than player's color
                return False
        return True

    def check_diagonal_victory(self: Self, i: int, j: int, player: Color) -> bool: # (moving to the top/right)
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
    
    def check_if_victory_is_possible(self: Self, player: Color) -> bool:
        for player_to_test in {Color.YELLOW, Color.RED}:
            assert not self.check_victory(player_to_test) # no player is supposed to have won already
        for column in range(NUMBER_OF_COLUMNS):   
            game_state_copy = copy.deepcopy(self)
            game_state_copy.play(column)
            if game_state_copy.check_victory(player):
                return True
        return False
    
    def is_a_deadly_move(self: Self, column: int) -> bool:
        potential_winner_player = self.player_turn
        game_state_copy = copy.deepcopy(self)
        game_state_copy.play(column)
        for column in range(NUMBER_OF_COLUMNS):
            new_game_state_copy = copy.deepcopy(game_state_copy)
            new_game_state_copy.play(column)
            if not new_game_state_copy.check_if_victory_is_possible(potential_winner_player):
                return False
        return True
    
    def check_if_exists_a_deadly_move(self: Self) -> bool:
        for column in range(NUMBER_OF_COLUMNS):
            if self.is_a_deadly_move(column):
                return True
        return False
    
