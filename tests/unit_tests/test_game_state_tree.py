import pytest
import numpy as np
import copy 

from src.connect4.game_state_tree import GameStateTree
from src.connect4.game_state import GameState, Color
from config import NUMBER_OF_COLUMNS, NUMBER_OF_ROWS

@pytest.fixture
def game_state_tree(): # a simple game_state_tree made of an initial empty board with and 2 leaves
    root_game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.YELLOW) 
    
    first_leaf_game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.RED) 
    first_leaf_game_state.board[NUMBER_OF_ROWS-1,0] = Color.YELLOW
    first_leaf_game_state_tree = GameStateTree(current_game_state=first_leaf_game_state, children_game_state_trees=[])

    second_leaf_game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.RED) 
    second_leaf_game_state.board[NUMBER_OF_ROWS-1,1] = Color.YELLOW
    second_leaf_game_state_tree = GameStateTree(current_game_state=second_leaf_game_state, children_game_state_trees=[])

    game_state_tree = GameStateTree(current_game_state=root_game_state, children_game_state_trees=[first_leaf_game_state_tree, second_leaf_game_state_tree])
    return game_state_tree

@pytest.fixture
def other_game_state_tree():
    root_game_state = GameState(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), 
                     player_turn = Color.RED) 
    for k in range(2,4):
        root_game_state.board[NUMBER_OF_ROWS-1,k] = Color.RED
    other_game_state_tree = GameStateTree(root_game_state, [])
    return other_game_state_tree

def test_is_leaf(game_state_tree):
    assert not game_state_tree.is_leaf() 
    assert game_state_tree.children_game_state_trees[0].is_leaf()

def test_get_all_subtrees(game_state_tree):
    assert len([node['game_state_tree'] for node in game_state_tree.get_all_subtrees()]) == 3

def test_get_all_leaves(game_state_tree):
    assert len(game_state_tree.get_all_leaves()) == 2
    assert len(game_state_tree.children_game_state_trees[0].get_all_leaves()) == 1

def test_get_depth(game_state_tree):
    assert game_state_tree.get_depth(game_state_tree.current_game_state) == 0

def test_extend_from_root(game_state_tree):
    game_state_tree.children_game_state_trees = []
    initialized_game_state_tree = game_state_tree.extend_from_root()
    assert len(initialized_game_state_tree.children_game_state_trees) == NUMBER_OF_COLUMNS

def test_extend(game_state_tree):
    depth = 2
    initial_number_of_sons = 2
    game_state_tree = game_state_tree.extend(depth)
    assert len(game_state_tree.get_all_leaves()) == initial_number_of_sons*NUMBER_OF_COLUMNS**depth
    # all_leaves should not really be used here, but well...

def test_get_depth(game_state_tree):
    assert game_state_tree.get_depth(game_state_tree) == 0
    assert game_state_tree.get_depth(game_state_tree.children_game_state_trees[0]) == 1

def test_get_height(game_state_tree):
    assert game_state_tree.get_height() == 2

def test_plot(game_state_tree):
    digraph, matching_tree_and_id = game_state_tree.to_networkx_graph()
    assert len(digraph.nodes()) == 3
    assert len(matching_tree_and_id) == 3
    # game_state_tree.plot()

