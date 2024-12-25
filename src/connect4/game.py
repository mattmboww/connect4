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


class Game:

    def __init__(self: Self, game_states: List[GameState] = None, pointer: int = 0) -> None:
        if game_states is None:
            initial_game_state = GameState().initialize()
            self.game_states = [initial_game_state]
        self.pointer = pointer

    def play(self: Self, column: int, player_turn: Color) -> Self:
        current_game_state = self.get_current_game_state()
        current_game_state = copy.deepcopy(current_game_state)
        current_game_state.play(column, player_turn)
        self.cut_game_states()
        self.game_states.append(current_game_state)
        self.move_pointer_forward()
        return self
    
    def get_current_game_state(self: Self) -> GameState:
        assert len(self.game_states) > 0
        return self.game_states[self.pointer]
    
    def get_current_player_turn(self: Self) -> Color:
        return self.get_current_game_state().player_turn
    
    def get_current_board(self: Self) -> Color:
        return self.get_current_game_state().board
    
    def add_initialized_game_state(self: Self) -> Self:
        self.cut_game_states()
        self.game_states.append(GameState().initialize())
        self.move_pointer_forward()
        return self  
    
    def cut_game_states(self: Self) -> Self:
        self.game_states = self.game_states[:self.pointer+1]
        return self
    
    def move_pointer_backward(self: Self) -> Self:
        assert self.pointer > 0
        self.pointer -= 1
        return self 
    
    def move_pointer_forward(self: Self) -> Self:
        assert self.pointer < len(self.game_states)-1
        self.pointer += 1
        return self 

    def play_and_check_victory(self: Self, column: int) -> Self:
        current_player_turn = self.get_current_player_turn()
        self.play(column, player_turn=current_player_turn)
        game_state = self.get_current_game_state()
        victory = game_state.check_victory(player=current_player_turn)
        return self, victory

