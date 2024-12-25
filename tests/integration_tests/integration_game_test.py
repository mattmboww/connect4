import pytest
import numpy as np
import copy 

from connect4.game import Game, Color, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS

@pytest.fixture
def game():
    game = Game(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW) 
    return game

def test_quick_gameplay(game):
    game.play(column = 0, player_turn = Color.YELLOW)
    game.play(column = 1, player_turn = Color.RED)
    game.play(column = 0, player_turn = Color.YELLOW)
    game.play(column = 2, player_turn = Color.RED)
    game.play(column = 0, player_turn = Color.YELLOW)
    game.play(column = 3, player_turn = Color.RED)
    game.play(column = 0, player_turn = Color.YELLOW)
    assert game.check_victory(Color.YELLOW)
    assert not game.check_victory(Color.RED)