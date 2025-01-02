import pytest 
import numpy as np

from src.connect4.game_state import GameState, Color, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, RECQUIRED_ALIGNED_PAWNS_TO_WIN
from src.connect4.value_functions import bipolar_value_function

@pytest.fixture
def game_state():
    game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.RED) 
    for i in range(3):
        game_state.board[NUMBER_OF_ROWS-1-i,0] = Color.RED
    return game_state

@pytest.fixture
def other_game_state():
    other_game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.RED) 
    for j in range(1, 3):
        other_game_state.board[NUMBER_OF_ROWS-1,j] = Color.RED
    return other_game_state

def test_bipolar_value_function(game_state, other_game_state):
    # testing with game_state
    assert bipolar_value_function(game_state, player=Color.YELLOW) == -1
    assert bipolar_value_function(game_state, player=Color.RED) == 1
    game_state.player_turn = Color.YELLOW
    assert bipolar_value_function(game_state, player=Color.YELLOW) == 0
    assert bipolar_value_function(game_state, player=Color.RED) == 0

    # testing with other_game_state
    assert bipolar_value_function(other_game_state, player=Color.YELLOW) == -1
    assert bipolar_value_function(other_game_state, player=Color.RED) == 1
    other_game_state.player_turn = Color.YELLOW
    assert bipolar_value_function(other_game_state, player=Color.YELLOW) == 0
    assert bipolar_value_function(other_game_state, player=Color.RED) == 0

    # testing with other_game_state with worse situation
    other_game_state.board[NUMBER_OF_ROWS-1,4] = Color.RED
    other_game_state.player_turn = Color.RED
    assert bipolar_value_function(other_game_state, player=Color.YELLOW) == -1
    assert bipolar_value_function(other_game_state, player=Color.RED) == 1
    other_game_state.player_turn = Color.YELLOW
    assert bipolar_value_function(other_game_state, player=Color.YELLOW) == 0
    assert bipolar_value_function(other_game_state, player=Color.RED) == 0
    
