# tests/test_board.py
import pytest
import numpy as np
import copy 

from connect4.board import Game, Color, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, RECQUIRED_ALIGNED_PAWNS_TO_WIN

@pytest.fixture
def game():
    game = Game(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW) 
    return game

def test_initialize_board():
    game = Game.initialize_board()
    assert np.all(game.board == Color.EMPTY)
    assert game.player_turn == Color.YELLOW

def test_switch_player_turn(game): 
    game.switch_player_turn()
    assert game.player_turn == Color.RED
    game.switch_player_turn()
    assert game.player_turn == Color.YELLOW

def test_get_position_of_highest_pawn(game):
    assert game.get_position_of_highest_pawn(column = 0) == NUMBER_OF_ROWS 
    game.board[0,0] = Color.RED
    assert game.get_position_of_highest_pawn(column = 0) == 0
    game.board[NUMBER_OF_ROWS-1,1] = Color.YELLOW
    assert game.get_position_of_highest_pawn(column = 1) == NUMBER_OF_ROWS-1

def test_play(game):
    column = 0
    game.play(column, player_turn = Color.YELLOW)
    assert game.player_turn == Color.RED
    for i in range(NUMBER_OF_ROWS-1):
        assert game.board[i,column] == Color.EMPTY
    assert game.board[NUMBER_OF_ROWS-1,column] == Color.YELLOW
    game.play(column, player_turn = Color.RED)
    assert game.board[NUMBER_OF_ROWS-2,column] == Color.RED
    assert game.board[NUMBER_OF_ROWS-1,column] == Color.YELLOW

def test_check_horizontal_victory(game):
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game.check_horizontal_victory(i, j, player_color=Color.YELLOW)
            assert not game.check_horizontal_victory(i, j, player_color=Color.RED)
    for j in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game.board[NUMBER_OF_ROWS-1,j] = Color.YELLOW
    assert game.check_horizontal_victory(NUMBER_OF_ROWS-1, 0, player_color=Color.YELLOW)
    assert not game.check_horizontal_victory(NUMBER_OF_ROWS-1, 0, player_color=Color.RED)
    assert not game.check_horizontal_victory(NUMBER_OF_ROWS-1, 1, player_color=Color.YELLOW)
    assert not game.check_horizontal_victory(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS, player_color=Color.YELLOW)

def test_check_vertical_victory(game):
    game = Game(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW) 
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game.check_vertical_victory(i, j, player_color=Color.YELLOW)
            assert not game.check_vertical_victory(i, j, player_color=Color.RED)
    for i in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game.board[NUMBER_OF_ROWS-1-i,0] = Color.YELLOW
    assert game.check_vertical_victory(NUMBER_OF_ROWS-1, 0, player_color=Color.YELLOW)
    assert not game.check_vertical_victory(NUMBER_OF_ROWS-1, 0, player_color=Color.RED)
    assert not game.check_vertical_victory(NUMBER_OF_ROWS-1, 1, player_color=Color.YELLOW)
    assert not game.check_vertical_victory(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS-1, player_color=Color.YELLOW)

def test_check_diagonal_victory(game):
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game.check_diagonal_victory(i, j, player_color=Color.YELLOW)
            assert not game.check_diagonal_victory(i, j, player_color=Color.RED)
    for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game.board[NUMBER_OF_ROWS-1-k,k] = Color.YELLOW
    assert game.check_diagonal_victory(NUMBER_OF_ROWS-1, 0, player_color=Color.YELLOW)
    assert not game.check_diagonal_victory(NUMBER_OF_ROWS-1, 0, player_color=Color.RED)
    assert not game.check_diagonal_victory(NUMBER_OF_ROWS-1, 1, player_color=Color.YELLOW)
    assert not game.check_diagonal_victory(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS-1, player_color=Color.YELLOW)

def test_check_victory(game):
    assert not game.check_victory(player_color = Color.YELLOW)
    assert not game.check_victory(player_color = Color.RED)

    new_game = copy.deepcopy(game)
    for j in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        new_game.board[NUMBER_OF_ROWS-1,j] = Color.YELLOW
    assert new_game.check_victory(player_color = Color.YELLOW)
    assert not new_game.check_victory(player_color = Color.RED)

    new_game = copy.deepcopy(game)
    for i in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        new_game.board[NUMBER_OF_ROWS-1-i,0] = Color.YELLOW
    assert new_game.check_victory(player_color = Color.YELLOW)
    assert not new_game.check_victory(player_color = Color.RED)

    new_game = copy.deepcopy(game)
    for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        new_game.board[NUMBER_OF_ROWS-1-k,k] = Color.YELLOW
    assert new_game.check_victory(player_color = Color.YELLOW)
    assert not new_game.check_victory(player_color = Color.RED)

