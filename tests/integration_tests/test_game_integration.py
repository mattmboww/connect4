import pytest
import numpy as np
import copy 

from src.connect4.game_state import GameState, Color
from src.connect4.game import Game

from config import NUMBER_OF_ROWS, NUMBER_OF_COLUMNS


@pytest.fixture
def game_state():
    game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW) 
    return game_state

def test_Game_instanciation():
    game = Game()
    game_states = game.game_states
    assert len(game_states) == 1
    unique_game_state = game_states[0]
    assert np.all(unique_game_state.board) == np.all(GameState().initialize().board)
    assert unique_game_state.player_turn == GameState().initialize().player_turn

def test_quick_game_stateplay(game_state):
    game_state.play(column = 0)
    game_state.play(column = 1)
    game_state.play(column = 0)
    game_state.play(column = 2)
    game_state.play(column = 0)
    game_state.play(column = 3)
    game_state.play(column = 0)
    assert game_state.check_new_victory(last_column_played= 0, player=Color.YELLOW)
    assert not game_state.check_new_victory(last_column_played = 0, player=Color.RED)

def test_is_equal(game_state):
    assert game_state.is_equal(game_state)
    game_state_copy = copy.deepcopy(game_state)
    game_state.play(column = 3)
    assert not game_state.is_equal(game_state_copy)
    assert GameState().initialize().is_equal(GameState().initialize())

def test_is_included(game_state):
    game_state.play(column = 0)
    game_state_copy = copy.deepcopy(game_state)
    game_state.play(column = 3)
    assert game_state_copy.is_included_in(game_state_copy)
    assert game_state_copy.is_included_in(game_state)
    assert not game_state.is_included_in(game_state_copy)