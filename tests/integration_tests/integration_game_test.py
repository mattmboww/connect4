import pytest
import numpy as np
import copy 

from connect4.game import Game, GameState, Color, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS

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
    game_state.play(column = 0, player_turn = Color.YELLOW)
    game_state.play(column = 1, player_turn = Color.RED)
    game_state.play(column = 0, player_turn = Color.YELLOW)
    game_state.play(column = 2, player_turn = Color.RED)
    game_state.play(column = 0, player_turn = Color.YELLOW)
    game_state.play(column = 3, player_turn = Color.RED)
    game_state.play(column = 0, player_turn = Color.YELLOW)
    assert game_state.check_victory(Color.YELLOW)
    assert not game_state.check_victory(Color.RED)

