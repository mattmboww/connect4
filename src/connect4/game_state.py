from enum import Enum, auto
import numpy as np
from typing import Self, Set, List
import copy 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from config import NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, RECQUIRED_ALIGNED_PAWNS_TO_WIN


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
    
    @staticmethod
    def get_opponent(player):
        assert player != Color.EMPTY
        return Color.RED if player == Color.YELLOW else Color.YELLOW

    def switch_player_turn(self: Self) -> Self:
        self.player_turn = GameState.get_opponent(self.player_turn)
        return self

    def get_position_of_highest_pawn(self: Self, column: int) -> int:
        assert 0 <= column < NUMBER_OF_COLUMNS
        if np.all(self.board[:, column] == Color.EMPTY):
            return NUMBER_OF_ROWS # convention: if no pawn in a column, lowest pawn is "in the ground"
        else:
            return np.where(self.board[:, column] != Color.EMPTY)[0][0]
        
    def get_possible_plays(self: Self) -> Set[int]:
        return {column for column in range(NUMBER_OF_COLUMNS) if 0 < self.get_position_of_highest_pawn(column)}
    
    def get_possible_futures(self: Self) -> List['GameState']:
        return {possible_column_to_play: copy.deepcopy(self).play(possible_column_to_play) for possible_column_to_play in self.get_possible_plays()}
    
    def play(self: Self, column: int) -> Self:
        assert column in self.get_possible_plays()
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

    def check_vertical_victory(self: Self, i: int, j: int, player: Color) -> bool: # (moving to the bottom)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i+k > NUMBER_OF_ROWS-1: # reached end of the board 
                return False
            if self.board[i+k][j] != player: # found a different color than player's color
                return False
        return True

    def check_diagonal_victory_up_right(self: Self, i: int, j: int, player: Color) -> bool: # (moving to the top/right)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i-k > NUMBER_OF_ROWS-1 or j+k > NUMBER_OF_COLUMNS-1: # reached end of the board
                return False
            if self.board[i-k][j+k] != player: # found a different color than player's color
                return False
        return True
    
    def check_diagonal_victory_down_right(self: Self, i: int, j: int, player: Color) -> bool: # (moving to the bottom/right)
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i+k > NUMBER_OF_ROWS-1 or j+k > NUMBER_OF_COLUMNS-1: # reached end of the board
                return False
            if self.board[i+k][j+k] != player: # found a different color than player's color
                return False
        return True
    
    def check_new_horizontal_victory(self: Self, i: int, last_column_played: int, player):
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if last_column_played-k < 0:
                continue
            if self.check_horizontal_victory(i, last_column_played-k, player):
                return True
        return False
    
    def check_new_diagonal_victory_up_right(self: Self, i: int, last_column_played: int, player):
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i + k > NUMBER_OF_ROWS or last_column_played-k <0:
                continue
            if self.check_diagonal_victory_up_right(i+k, last_column_played-k, player):
                return True
        return False
    
    def check_new_diagonal_victory_down_right(self: Self, i: int, last_column_played: int, player):
        for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
            if i - k < 0 or last_column_played-k < 0:
                continue
            if self.check_diagonal_victory_down_right(i-k, last_column_played-k, player):
                return True
        return False

    def check_new_victory(self: Self, last_column_played: int, player: Color) -> bool:
        i = self.get_position_of_highest_pawn(last_column_played)
        if i==NUMBER_OF_ROWS:
            return False

        if self.check_new_horizontal_victory(i,last_column_played, player):
            return True
        
        if self.check_new_diagonal_victory_up_right(i, last_column_played, player):
            return True
    
        if self.check_new_diagonal_victory_down_right(i, last_column_played, player):
            return True

        if self.check_vertical_victory(i, last_column_played, player):
            return True

        return False
    
    def check_if_victory_is_possible(self: Self, player: Color) -> bool:
        for column in self.get_possible_plays():   
            game_state_copy = copy.deepcopy(self)
            game_state_copy.player_turn = player # to force player if necessary 
            game_state_copy.play(column)
            if game_state_copy.check_new_victory(last_column_played=column, player=player):
                return True   
        return False
    
    def is_a_deadly_move(self: Self, column: int, player: Color) -> bool:
        game_state_copy = copy.deepcopy(self)
        game_state_copy.player_turn = player
        game_state_copy.play(column)
        if game_state_copy.check_new_victory(last_column_played=column, player=player):
            return True
        for some_column in game_state_copy.get_possible_plays():
            new_game_state_copy = copy.deepcopy(game_state_copy)
            new_game_state_copy.play(some_column)
            if new_game_state_copy.check_new_victory(some_column, GameState.get_opponent(player)):
                return False # if opponent can just win the game, we did not make a deadly move...
            if not new_game_state_copy.check_if_victory_is_possible(player):
                return False
        return True
    
    def check_if_exists_a_deadly_move(self: Self, player: Color) -> bool:
        for column in self.get_possible_plays():
            if self.is_a_deadly_move(column, player):
                return True
        return False
    
    def is_full_board(self: Self) -> bool:
        return np.all(self.board != Color.EMPTY) 
        
    def plot(self: Self)-> None:
        board_copy = copy.deepcopy(self.board)
        value_array = np.vectorize(lambda status: status.value)(board_copy)
        colors = ['grey', 'yellow', 'red']  
        cmap = ListedColormap(colors)
        plt.imshow(value_array, cmap=cmap, interpolation='nearest')
        plt.colorbar(label="Valeur")
        plt.title("Visualisation avec Colormap personnalisée")
        plt.show()

    def is_included_in(self: Self, other_game_state) -> bool:
        for i in range(self.board.shape[0]): 
            for j in range(self.board.shape[1]):  
                if self.board[i,j] == Color.EMPTY:
                    continue
                if self.board[i,j] != other_game_state.board[i,j]:
                    return False
        return True
    
    def is_equal(self, other_game_state) -> bool:
        for i in range(self.board.shape[0]): 
            for j in range(self.board.shape[1]):  
                if self.board[i,j] != other_game_state.board[i,j]:
                    return False
        return True