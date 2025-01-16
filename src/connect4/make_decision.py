import random
import copy
from pathlib import Path
from typing import List
import multiprocessing

from src.connect4.game_state import GameState, Color
from src.connect4.game_state_tree import GameStateTree
from src.connect4.moves_sequence import MovesSequence, get_moves_sequences_with_game_state, get_winning_moves_sequences
from src.connect4.utils import sigmoid

# TODO : parametre pour modifier le nioveauy de prfondeur de reflexion
# TODO if a move has five, no need to evaluate the other, can we use this for faster computation? > not sure its so useful
# TODO : reformuler cette fonction pour qu'elle dépende uniquement du game state et pas du coup joué (comme pour la partie history)
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

def generate_decisions_score_with_science(game_state: GameState, player: Color, move_evaluation_function: 'function'):
    decisions_with_score = {column: move_evaluation_function(game_state, player, column) for column in game_state.get_possible_plays()}
    return decisions_with_score

def make_decision_with_science(game_state: GameState, player: Color, move_evaluation_function: 'function', use_random: bool = True) -> int:
    decisions_with_science = generate_decisions_score_with_science(game_state, player, move_evaluation_function)
    max_values = max(decisions_with_science.values())
    max_keys = [key for key, value in decisions_with_science.items() if value == max_values]
    return random.choice(max_keys) if use_random else max_keys[0]

def evaluate_game_state_with_history(game_state: GameState, player: Color, moves_sequences: List[MovesSequence]) -> dict:
    moves_sequences_with_game_state = get_moves_sequences_with_game_state(moves_sequences, game_state)
    if len(moves_sequences_with_game_state) == 0:
        return 0 # no data => still no specific positive or negative value
    else:
        moves_sequences_with_game_state_that_won = get_winning_moves_sequences(moves_sequences_with_game_state, player)
        return sigmoid(len(moves_sequences_with_game_state_that_won)/len(moves_sequences_with_game_state))

def generate_decisions_score_with_history(game_state: GameState, player: Color, moves_sequence: List[MovesSequence]):
    decisions_with_history = {}
    for column in game_state.get_possible_plays():
        game_state_copy = copy.deepcopy(game_state)
        game_state_copy.play(column)
        decisions_with_history[column] = evaluate_game_state_with_history(game_state, player, moves_sequence)
    return decisions_with_history
    
def make_decision_with_history(game_state: GameState, player: Color, moves_sequences: List[MovesSequence], use_random: bool = True):
    decisions_with_score = generate_decisions_score_with_history(game_state, player, moves_sequences)
    max_values = max(decisions_with_score.values())
    max_keys = [key for key, value in decisions_with_score.items() if value == max_values]
    return random.choice(max_keys) if use_random else max_keys[0]

def make_decision(game_state: GameState, player: Color, move_evaluation_function: 'function', 
                  moves_sequences: List[MovesSequence], use_random: bool = True):
    decisions_with_science = generate_decisions_score_with_science(game_state, player, move_evaluation_function)
    if all(value == 0 for value in decisions_with_science.values()):
        return make_decision_with_history(game_state, player, moves_sequences, use_random)
    return make_decision_with_science(game_state, player, move_evaluation_function, use_random)
# TODO : use args and kwargs for more readbility

# TODO : fonction qui prend en compte l'histoire et la science pour générer des décisions > DONE
# TODO : test the function

# la value d'un gamestate, c'est la value que je vais sortir avec evaluate_a_move appliqué à ce gamestate <--- 0>
# en fait c'est la fonction make decision qui définit ça, mais elle l'utilise directement

# idée : entrainr modele avec ordinateurs betes, qui font du random (voir combien de temps ca prend), voir avec lv1
# se servir des resultats pour noter les etats qui autrement sont notés 0

# TODO : placer cette partie dans un fichier séparé (tout ce qui concerne la simulation de parties)

# def generate_full_moves_sequence(yellow_bot: 'function', red_bot: 'function', first_player: Color):
def generate_full_moves_sequence(args):
    yellow_bot, red_bot, first_player = args
    game_state = GameState()
    game_state.initialize()
    current_player = first_player
    winner = Color.EMPTY
    moves = []
    while not game_state.is_full_board():
        match current_player:
            case Color.YELLOW:
                current_bot = yellow_bot
            case Color.RED:
                current_bot = red_bot
            case _:
                raise ValueError('Unknow case for current_player...')
        move = make_decision_with_science(game_state, current_player, current_bot)
        game_state.play(move)
        moves.append(move)
        if game_state.check_new_victory(move, current_player):
            winner = current_player
            break
        current_player = GameState.get_opponent(current_player)
    return MovesSequence(first_player, moves, winner)

# def generate_multiple_full_moves_sequences(yellow_bot: 'function', red_bot: 'function', first_player: Color, n: int):
def generate_multiple_full_moves_sequences(args, n: int):
    return [generate_full_moves_sequence(args) for _ in range(n)]

# def generate_multiple_full_moves_sequences_with_multiprocessing(yellow_bot: 'function', red_bot: 'function', first_player: Color, n: int):
def generate_multiple_full_moves_sequences_with_multiprocessing(args, n, processes = 3):
    yellow_bot, red_bot, first_player = args
    # Création de la liste d'arguments sous forme de tuples
    args = [(yellow_bot, red_bot, first_player) for _ in range(n)]
    with multiprocessing.Pool(processes=processes) as pool:
        # Exécution parallèle en passant correctement les arguments
        results = pool.map(generate_full_moves_sequence, args)
    
    return results

