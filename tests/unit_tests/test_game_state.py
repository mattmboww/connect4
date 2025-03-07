import pytest
import numpy as np
import copy 

from src.connect4.game_state import GameState, Color, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, RECQUIRED_ALIGNED_PAWNS_TO_WIN


@pytest.fixture
def game_state():
    game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW) 
    return game_state

def test_initialize(game_state):
    initialized_game_state = game_state.initialize()
    assert np.all(initialized_game_state.board[:,:] == np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY))
    assert initialized_game_state.player_turn == Color.YELLOW

def test_switch_player_turn(game_state): 
    game_state.switch_player_turn()
    assert game_state.player_turn == Color.RED
    game_state.switch_player_turn()
    assert game_state.player_turn == Color.YELLOW

def test_get_position_of_highest_pawn(game_state):
    assert game_state.get_position_of_highest_pawn(column = 0) == NUMBER_OF_ROWS 
    game_state.board[0,0] = Color.RED
    assert game_state.get_position_of_highest_pawn(column = 0) == 0
    game_state.board[NUMBER_OF_ROWS-1,1] = Color.YELLOW
    assert game_state.get_position_of_highest_pawn(column = 1) == NUMBER_OF_ROWS-1

def test_get_possible_plays(game_state):
    assert game_state.get_possible_plays() == set(range(NUMBER_OF_COLUMNS))
    for _ in range(NUMBER_OF_ROWS):
        game_state.play(column=0)
    assert game_state.get_possible_plays() == set(range(1, NUMBER_OF_COLUMNS))

def test_get_possible_futures(game_state):
    assert len(game_state.get_possible_futures().values()) == NUMBER_OF_COLUMNS
    for _ in range(NUMBER_OF_ROWS):
        game_state.play(column=0)
    assert len(game_state.get_possible_futures().values()) == NUMBER_OF_COLUMNS-1
    other_game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.YELLOW), 
                     player_turn = Color.YELLOW) 
    assert len(list(other_game_state.get_possible_futures().values())) == 0
    other_game_state.board[0,0] = Color.EMPTY
    assert len(other_game_state.get_possible_futures().values()) == 1
    unique_possible_future = other_game_state.get_possible_futures()[0]
    assert np.all(unique_possible_future.board == np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.YELLOW))
    assert unique_possible_future.player_turn == Color.RED


def test_play_from_game_state(game_state):
    column = 0
    game_state.play(column)
    assert game_state.player_turn == Color.RED
    for i in range(NUMBER_OF_ROWS-1):
        assert game_state.board[i,column] == Color.EMPTY
    assert game_state.board[NUMBER_OF_ROWS-1,column] == Color.YELLOW
    game_state.play(column)
    assert game_state.board[NUMBER_OF_ROWS-2,column] == Color.RED
    assert game_state.board[NUMBER_OF_ROWS-1,column] == Color.YELLOW

def test_check_horizontal_victory(game_state):
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game_state.check_horizontal_victory(i, j, player=Color.YELLOW)
            assert not game_state.check_horizontal_victory(i, j, player=Color.RED)
    for j in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game_state.board[NUMBER_OF_ROWS-1,j] = Color.YELLOW
    assert game_state.check_horizontal_victory(NUMBER_OF_ROWS-1, 0, player=Color.YELLOW)
    assert not game_state.check_horizontal_victory(NUMBER_OF_ROWS-1, 0, player=Color.RED)
    assert not game_state.check_horizontal_victory(NUMBER_OF_ROWS-1, 1, player=Color.YELLOW)
    assert not game_state.check_horizontal_victory(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS, player=Color.YELLOW)

def test_check_new_horizontal_victory(game_state):
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game_state.check_new_horizontal_victory(i, j, player=Color.YELLOW)
            assert not game_state.check_new_horizontal_victory(i, j, player=Color.RED)
    for j in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game_state.board[NUMBER_OF_ROWS-1,j] = Color.YELLOW
    assert game_state.check_new_horizontal_victory(NUMBER_OF_ROWS-1, 0, player=Color.YELLOW)
    assert not game_state.check_new_horizontal_victory(NUMBER_OF_ROWS-1, 0, player=Color.RED)
    assert game_state.check_new_horizontal_victory(NUMBER_OF_ROWS-1, 1, player=Color.YELLOW) # different than for check_horizontal_victory
    assert not game_state.check_new_horizontal_victory(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS, player=Color.YELLOW)

def test_check_vertical_victory(game_state):
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game_state.check_vertical_victory(i, j, player=Color.YELLOW)
            assert not game_state.check_vertical_victory(i, j, player=Color.RED)
    for i in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game_state.board[NUMBER_OF_ROWS-1-i,0] = Color.YELLOW
    assert game_state.check_vertical_victory(NUMBER_OF_ROWS-RECQUIRED_ALIGNED_PAWNS_TO_WIN, 0, player=Color.YELLOW)
    assert not game_state.check_vertical_victory(NUMBER_OF_ROWS-1, 0, player=Color.RED)
    assert not game_state.check_vertical_victory(NUMBER_OF_ROWS-1, 1, player=Color.YELLOW)
    assert not game_state.check_vertical_victory(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS-1, player=Color.YELLOW)

def test_check_diagonal_victory_up_right(game_state):
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game_state.check_diagonal_victory_up_right(i, j, player=Color.YELLOW)
            assert not game_state.check_diagonal_victory_up_right(i, j, player=Color.RED)
    for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game_state.board[NUMBER_OF_ROWS-1-k,k] = Color.YELLOW
    assert game_state.check_diagonal_victory_up_right(NUMBER_OF_ROWS-1, 0, player=Color.YELLOW)
    assert not game_state.check_diagonal_victory_up_right(NUMBER_OF_ROWS-1, 0, player=Color.RED)
    assert not game_state.check_diagonal_victory_up_right(NUMBER_OF_ROWS-1, 1, player=Color.YELLOW)
    assert not game_state.check_diagonal_victory_up_right(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS-1, player=Color.YELLOW)

def test_check_new_diagonal_victory_up_right(game_state):
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            assert not game_state.check_new_diagonal_victory_up_right(i, j, player=Color.YELLOW)
            assert not game_state.check_new_diagonal_victory_up_right(i, j, player=Color.RED)
    for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        game_state.board[NUMBER_OF_ROWS-1-k,k] = Color.YELLOW
    assert game_state.check_new_diagonal_victory_up_right(NUMBER_OF_ROWS-1, 0, player=Color.YELLOW)
    assert not game_state.check_new_diagonal_victory_up_right(NUMBER_OF_ROWS-1, 0, player=Color.RED)
    assert not game_state.check_new_diagonal_victory_up_right(NUMBER_OF_ROWS-1, 1, player=Color.YELLOW)
    assert not game_state.check_new_diagonal_victory_up_right(NUMBER_OF_ROWS-1, NUMBER_OF_COLUMNS-1, player=Color.YELLOW)

def test_check_new_victory(game_state):
    assert not game_state.check_new_victory(last_column_played=0, player = Color.YELLOW)
    assert not game_state.check_new_victory(last_column_played=0, player = Color.RED)

    new_game_state = copy.deepcopy(game_state)
    for j in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        new_game_state.board[NUMBER_OF_ROWS-1,j] = Color.YELLOW
    assert new_game_state.check_new_victory(last_column_played=j, player = Color.YELLOW)
    assert not new_game_state.check_new_victory(last_column_played=j, player = Color.RED)

    new_game_state = copy.deepcopy(game_state)
    for i in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        new_game_state.board[NUMBER_OF_ROWS-1-i,0] = Color.YELLOW
    assert new_game_state.check_new_victory(last_column_played=0, player = Color.YELLOW)
    assert not new_game_state.check_new_victory(last_column_played=0, player = Color.RED)

    new_game_state = copy.deepcopy(game_state)
    for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN):
        new_game_state.board[NUMBER_OF_ROWS-1-k,k] = Color.YELLOW
    assert new_game_state.check_new_victory(last_column_played=k, player = Color.YELLOW)
    assert not new_game_state.check_new_victory(last_column_played=k, player = Color.RED)

def test_check_if_victory_is_possible(game_state):
    assert not game_state.check_if_victory_is_possible(player=Color.YELLOW)
    game_state.switch_player_turn()
    assert not game_state.check_if_victory_is_possible(player=Color.RED)
    game_state.board
    game_state.switch_player_turn()

    new_game_state = copy.deepcopy(game_state)
    for j in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN-1):
        new_game_state.board[NUMBER_OF_ROWS-1,j] = Color.YELLOW
    assert new_game_state.check_if_victory_is_possible(player = Color.YELLOW)
    new_game_state.switch_player_turn()
    assert not new_game_state.check_if_victory_is_possible(player = Color.RED)

    new_game_state = copy.deepcopy(game_state)
    for i in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN-1):
        new_game_state.board[NUMBER_OF_ROWS-1-i,0] = Color.YELLOW
    assert new_game_state.check_if_victory_is_possible(player = Color.YELLOW)
    new_game_state.switch_player_turn()
    assert not new_game_state.check_if_victory_is_possible(player = Color.RED)

    new_game_state = copy.deepcopy(game_state)
    for k in range(RECQUIRED_ALIGNED_PAWNS_TO_WIN-1):
        new_game_state.board[NUMBER_OF_ROWS-1-k,k] = Color.YELLOW
    assert not new_game_state.check_if_victory_is_possible(player = Color.YELLOW)
    new_game_state.switch_player_turn()
    assert not new_game_state.check_if_victory_is_possible(player = Color.RED)

def test_is_a_deadly_move(game_state):
    assert not game_state.is_a_deadly_move(column=0, player=Color.YELLOW)
    game_state.board[NUMBER_OF_ROWS-1,2] = Color.YELLOW
    game_state.board[NUMBER_OF_ROWS-1,3] = Color.YELLOW
    assert game_state.is_a_deadly_move(column=1, player=Color.YELLOW)

def test_check_if_exists_a_deadly_move(game_state):
    assert not game_state.check_if_exists_a_deadly_move(player=Color.YELLOW)
    game_state.board[NUMBER_OF_ROWS-1,2] = Color.YELLOW
    game_state.board[NUMBER_OF_ROWS-1,3] = Color.YELLOW
    assert game_state.check_if_exists_a_deadly_move(Color.YELLOW)

