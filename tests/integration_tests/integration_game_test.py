import pytest
import numpy as np
import copy 

from connect4.game import Game, Color

def test_quick_gameplay():
    game = Game.initialize_board()
    game.play(column = 0, player_turn = Color.YELLOW)
    game.play(column = 1, player_turn = Color.RED)
    game.play(column = 0, player_turn = Color.YELLOW)
    game.play(column = 2, player_turn = Color.RED)
    game.play(column = 0, player_turn = Color.YELLOW)
    game.play(column = 3, player_turn = Color.RED)
    game.play(column = 0, player_turn = Color.YELLOW)
    assert game.check_victory(Color.YELLOW)
    assert not game.check_victory(Color.RED)