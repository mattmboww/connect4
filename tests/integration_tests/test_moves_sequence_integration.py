import pytest
import numpy as np
import copy 
import logging 

from src.connect4.game_state import GameState, Color
from src.connect4.game import Game
from src.connect4.moves_sequence import MovesSequence, generate_full_moves_sequence, save_moves_sequences_as_pickle, load_moves_sequences_from_pickle, add_moves_sequences_to_pickle, read_statistics, convert_moves_sequence_to_game_state, generate_multiple_full_moves_sequences
from src.connect4.make_decision import make_scientific_decision

from config import NUMBER_OF_ROWS, NUMBER_OF_COLUMNS

@pytest.fixture
def test_path():
    test_path = 'output/moves_sequences/test.pkl'
    return test_path

@pytest.fixture
def number_of_sequences():
    number_of_sequences = 1
    return number_of_sequences

def test_generate_full_moves_sequence(test_path):
    moves_sequence = generate_full_moves_sequence(yellow_bot=make_scientific_decision, red_bot=make_scientific_decision, first_player=Color.YELLOW)
    # game_state.plot()
    save_moves_sequences_as_pickle(moves_sequences=[moves_sequence], output_path=test_path)

def test_generate_multiple_move_sequences():
    generate_multiple_full_moves_sequences(yellow_bot=make_scientific_decision, red_bot=make_scientific_decision, first_player=Color.YELLOW, n=3)

def test_load_moves_sequences_from_pickle(test_path):
    load_moves_sequences_from_pickle(input_path=test_path)
    
def test_add_moves_sequences_to_pickle(test_path, number_of_sequences):
    moves_sequences = []
    for _ in range(number_of_sequences):
        moves_sequence = generate_full_moves_sequence(yellow_bot=make_scientific_decision, red_bot=make_scientific_decision, first_player=Color.YELLOW)
        moves_sequences.append(moves_sequence)
    add_moves_sequences_to_pickle(moves_sequences=moves_sequences, input_path=test_path, output_path=test_path)

def test_convert_moves_sequence_to_game_state():
    moves_sequence = MovesSequence(first_player=Color.YELLOW, moves=[0,1,0,4], winner = None)
    convert_moves_sequence_to_game_state(moves_sequence)

def test_read_statistics(test_path, number_of_sequences):
    assert read_statistics(test_path)['number_of_sequences'] == number_of_sequences +1
    # assert read_statistics(test_path)['number_of_even'] == 42





# 10 M de game, normalement linéaire, donc on pourrai tmonter a 100 M assez facilement
# voir si on peut optimiser le code aussi
# on choppe jamais de victoire, tres chelou, a etudier 
# peut etre que statistiquement ça n'arrive pas mais je pense passe 

# problem : jouer une partie est bien trop long (de l'ordre de 2 sec)
# on est passé à moins d'une seconde en optimisant la verification des victoires

# 60 sec pour 100 extraits
# Une heure : 6000 parties : pas assez 
