import random

from src.connect4.game_state import GameState, Color
from src.connect4.game_state_tree import GameStateTree
import copy



def compute_game_state_tree_value(game_state_tree: GameStateTree, value_function: 'function', player: Color) -> float:
    all_subtrees = [subtree['game_state_tree'] for subtree in game_state_tree.get_all_subtrees()]
    while game_state_tree.value is None:
        for subtree in all_subtrees:
            subtree_children_values = [subtree_child.value for subtree_child in subtree.children_game_state_trees]
            if subtree.is_leaf():
                subtree.value = float(value_function(subtree.current_game_state, player))
            elif all([isinstance(subtree_children_value, float) for subtree_children_value in subtree_children_values]):
                subtree.value = max(subtree_children_values) if subtree.current_game_state.player_turn == player else min(subtree_children_values)
            else:
                pass   
    game_state_tree_value = game_state_tree.value
    game_state_tree.reinitialize_all_values()
    return game_state_tree_value

def compute_game_state_value(game_state: GameState, value_function: 'function', player: Color, depth) -> float:
    game_state_tree = GameStateTree.generate_tree_from_game_state(game_state, depth)
    return compute_game_state_tree_value(game_state_tree, value_function, player)

def make_decision(game_state: GameState, value_function: 'function', player: Color, depth: int, use_random: bool) -> int:
    assert game_state.player_turn == player # should be the turn of the player using this strategy
    values_of_all_possible_plays = []
    possible_futures = game_state.get_possible_futures()
    for possible_future_plays in possible_futures:
        potential_value = compute_game_state_value(possible_futures[possible_future_plays], value_function, player, depth)
        values_of_all_possible_plays[possible_future_plays] = potential_value
    assert not values_of_all_possible_plays == []

    max_value = max(values_of_all_possible_plays.values())
    keys_with_max_value = [key for key, value in values_of_all_possible_plays.items() if value == max_value]

    return random.choice(keys_with_max_value) if use_random else keys_with_max_value[-1]

# what to do if no possible plays ? should not happend as it would mean board is full but well..
    

# je parcours les noeuds tant que le pere n'a pas de valeur
# si j'ai un noeud sans enfant, ou si tous ses enfants ont une valeur, je calcule la valeur de mon noeud
# on continue jusqu'à tout avoir



    # check if there is a deadly move for other player next turn

    # check if there is a deadly move for ourselves next turn

    return 0

def evaluate_a_move_with_science(game_state: GameState, player: Color, column: int):
    assert column in game_state.get_possible_plays()
    game_state_copy = copy.deepcopy(game_state)
    game_state_copy.play(column)
    if game_state.check_if_victory_is_possible(player):
        return 5
    if game_state_copy.check_if_victory_is_possible(GameState.get_opponent(player)):
        return -5
    if game_state.is_a_deadly_move(column, player):
        return 4
    if game_state_copy.check_if_exists_a_deadly_move(GameState.get_opponent(player)):
        return -4
    return 0

# besoin d'un message qui dit : c'est fini pour moi si l'ordi est cit, ou juste qui dit la valeur des moves 
# et la valeur du move que lui a choisi
# bref des métriques qui montrent ce que l'ordi a fait quand il vient de le faire

# "rec terminale" le plus simple et efficace ?
def evaluate_a_move_with_science_and_depth(game_state: GameState, player: Color, column: int, depth: int, use_random:int):
    assert depth >= 0
    evaluation = evaluate_a_move_with_science(game_state, player, column)
    if evaluation == 0:
        if depth == 0:
            return 0
        else:
            if game_state.player_turn == player:
                return max([evaluate_a_move_with_science_and_depth(game_state, player, column, depth-1) for column in game_state.get_possible_plays()])
            else:
                return min([evaluate_a_move_with_science_and_depth(game_state, GameState.get_opponent(player), column, depth-1) for column in game_state.get_possible_plays()])
    else: 
        return evaluation

def make_scientific_decision(game_state: GameState, player: Color, use_random: bool = True) -> int:
    decisions_with_score = {column: evaluate_a_move_with_science(game_state, player, column) for column in game_state.get_possible_plays()}
    max_values = max(decisions_with_score.values())
    max_keys = [key for key, value in decisions_with_score.items() if value == max_values]
    return random.choice(max_keys) if use_random else max_keys[0]

def make_scientific_decision_with_depth(game_state: GameState, player: Color, use_random: bool, depth: int) -> int:
    decisions_with_score = {column: evaluate_a_move_with_science(game_state, player, column) for column in game_state.get_possible_plays()}
    max_values = max(decisions_with_score.values())
    max_keys = [key for key, value in decisions_with_score.items() if value == max_values]
    return max_keys[0]




