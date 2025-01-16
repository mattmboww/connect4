from typing import Self, List
from pathlib import Path
import pickle
import numpy as np

from src.connect4.game_state import GameState, Color


class MovesSequence:
    def __init__(self: Self, first_player: Color, moves: List[int], winner: Color) -> None:
        self.first_player = first_player
        self.moves = moves
        self.winner = winner
        
# some could be methods 
def save_moves_sequences_as_pickle(moves_sequences: List[MovesSequence], output_path: Path) -> None:
    with open(output_path, 'wb') as f:
        pickle.dump(moves_sequences, f)

def load_moves_sequences_from_pickle(input_path: Path) -> MovesSequence:
    with open(input_path, 'rb') as f:
        loaded_data = pickle.load(f)
    return loaded_data

def add_moves_sequences_to_pickle(moves_sequences: List[MovesSequence], input_path: Path, output_path: Path) -> None:
    save_moves_sequences_as_pickle(load_moves_sequences_from_pickle(input_path) + moves_sequences, output_path)

def convert_moves_sequence_to_game_state(moves_sequence: MovesSequence) -> GameState:
    game_state = GameState()
    game_state.initialize()
    game_state.player_turn = moves_sequence.first_player
    for move in moves_sequence.moves:
        game_state.play(column=move)
    return game_state

def read_statistics(input_path: Path) -> None:
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
    statistics['mean_number_of_moves'] = float(np.round(np.mean([len(move_sequence.moves) 
                                                  for move_sequence in loaded_moves_sequences]), 2))
    return statistics

def get_moves_sequences_with_game_state(moves_sequences: List[MovesSequence], target_game_state: GameState) -> List[MovesSequence]:
    moves_sequences_with_occurences = []
    for moves_sequence in moves_sequences:
        current_game_state = GameState().initialize()
        for move in moves_sequence.moves:
            if not current_game_state.is_included_in(target_game_state):
                break
            if current_game_state.is_equal(target_game_state): 
                moves_sequences_with_occurences.append(moves_sequence)
                break
            current_game_state.play(move) 
    return moves_sequences_with_occurences
    
def get_winning_moves_sequences(moves_sequences: List[MovesSequence], player: Color):
    return [moves_sequence for moves_sequence in moves_sequences if moves_sequence.winner == player]
        
