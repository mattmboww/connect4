from typing import Self, List
from pathlib import Path
import pickle

from src.connect4.game_state import GameState, Color


class MovesSequence:
    def __init__(self: Self, first_player: Color, moves: List[int], winner: Color) -> None:
        self.first_player = first_player
        self.moves = moves
        self.winner = winner
        
# some could be methods 
def save_moves_sequences_as_pickle(moves_sequences: List[MovesSequence], output_path: Path):
    with open(output_path, 'wb') as f:
        pickle.dump(moves_sequences, f)

def load_moves_sequences_from_pickle(input_path: Path):
    with open(input_path, 'rb') as f:
        loaded_data = pickle.load(f)
    return loaded_data

def add_moves_sequences_to_pickle(moves_sequences: List[MovesSequence], input_path: Path, output_path: Path):
    save_moves_sequences_as_pickle(load_moves_sequences_from_pickle(input_path) + moves_sequences, output_path)

def generate_full_moves_sequence(yellow_bot: 'function', red_bot: 'function', first_player: Color):
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
                raise ValueError()
        move = current_bot(game_state, current_player)
        game_state.play(move)
        moves.append(move)
        if game_state.check_new_victory(move, current_player):
            winner = current_player
            break
        current_player = GameState.get_opponent(current_player)
    return MovesSequence(first_player, moves, winner)

def convert_moves_sequence_to_game_state(moves_sequence: MovesSequence):
    game_state = GameState()
    game_state.initialize()
    game_state.player_turn = moves_sequence.first_player
    for move in moves_sequence.moves:
        game_state.play(column=move)
    return game_state

def generate_multiple_full_moves_sequences(yellow_bot: 'function', red_bot: 'function', first_player: Color, n: int):
    return [generate_full_moves_sequence(yellow_bot, red_bot, first_player) for _ in range(n)]

def read_statistics(input_path: Path):
    loaded_moves_sequences = load_moves_sequences_from_pickle(input_path)
    statistics = {}
    statistics['number_of_sequences'] = len(loaded_moves_sequences)
    statistics['number_of_yellow_first_player'] = len([move_sequence for move_sequence in loaded_moves_sequences 
                                                        if move_sequence.first_player == Color.YELLOW])
    statistics['number_of_yellow_victory'] = len([move_sequence for move_sequence in loaded_moves_sequences 
                                                        if move_sequence.winner == Color.YELLOW])
    statistics['number_of_red_victory'] = len([move_sequence for move_sequence in loaded_moves_sequences 
                                                        if move_sequence.winner == Color.RED])
    statistics['number_of_even'] = len([move_sequence for move_sequence in loaded_moves_sequences 
                                                        if move_sequence.winner == Color.EMPTY])
    statistics['first_board'] = 0
    return statistics
