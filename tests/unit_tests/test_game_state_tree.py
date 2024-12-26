import pytest
import numpy as np
import copy 

from src.connect4.game_state_tree import GameStateTree
from src.connect4.game_state import GameState, Color
from config import NUMBER_OF_COLUMNS, NUMBER_OF_ROWS

@pytest.fixture
def game_state_tree(): # a simple game_state_tree made of an initial empty board with an unique leaf
    game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW) 
    new_game_state = copy.deepcopy(game_state)
    new_game_state.board[NUMBER_OF_ROWS-1,0] = Color.RED
    new_game_state_tree = GameStateTree(current_game_state=new_game_state, potential_next_game_states=[])
    game_state_tree = GameStateTree(current_game_state=game_state, potential_next_game_states=[])
    return game_state_tree

def test_is_leaf(game_state_tree):
    assert not game_state_tree.is_leaf() 
    assert game_state_tree.potential_next_game_states[0].is_leaf

def test_check_get_all_leaves(game_state_tree):
    assert len(game_state_tree.get_all_leaves()) == 1