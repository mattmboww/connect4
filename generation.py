import pytest
import numpy as np
import random
import multiprocessing
import time


from src.connect4.game_state import Color
from src.connect4.moves_sequence import MovesSequence, save_moves_sequences_as_pickle, load_moves_sequences_from_pickle, add_moves_sequences_to_pickle, read_statistics, convert_moves_sequence_to_game_state
from src.connect4.make_decision import generate_multiple_full_moves_sequences_with_multiprocessing, evaluate_a_move_with_science, generate_full_moves_sequence, generate_multiple_full_moves_sequences

if __name__ == "__main__":

    path_to_simulations = '/Users/matthieumbargaowona/Desktop/4FVN/connect4/output/moves_sequences/my_simulations.pkl'

    args = evaluate_a_move_with_science, evaluate_a_move_with_science, Color.YELLOW

    # generate stuff
    start = time.time()
    moves_sequences = generate_multiple_full_moves_sequences(args, n=10_000)
    print(time.time()-start)
    save_moves_sequences_as_pickle(moves_sequences=moves_sequences, output_path=path_to_simulations)

    # generate stuff with multiprocessing
    start = time.time()
    moves_sequences = generate_multiple_full_moves_sequences_with_multiprocessing(args, n=10_000, processes = 6)
    print(time.time()-start)
    save_moves_sequences_as_pickle(moves_sequences=moves_sequences, output_path=path_to_simulations)

    # TODO : checke combien de processes max on peut monter
    # TODO : comparer durée de calcul multi et normmal + verifier pas d'anomalie sur le normla
    # TODO : capter si coeur et processes cest equivalent

    # + long pour l'instant mais logique car petit volume de data

    # check the statistacs
    stats = read_statistics(path_to_simulations)
    print(stats)
