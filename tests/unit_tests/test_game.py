import pytest
import numpy as np
import copy 

from connect4.game import Game, Color
from connect4.gameState import NUMBER_OF_ROWS


def test_play_from_Game():
    game = Game()
    game.play(column=0)
    game.play(column=1)
    game.play(column=0)
    game.play(column=1)
    game_states = game.game_states
    assert len(game_states) == 5
    current_game_state = game_states[-1]
    assert current_game_state.board[NUMBER_OF_ROWS-1, 0] == Color.YELLOW
    assert current_game_state.board[NUMBER_OF_ROWS-2, 0] == Color.YELLOW
    assert current_game_state.board[NUMBER_OF_ROWS-1, 1] == Color.RED
    assert current_game_state.board[NUMBER_OF_ROWS-2, 1] == Color.RED

def test_current_game_state():
    pass

def test_add_initialized_game_state():
    pass
