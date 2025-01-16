import pytest
import numpy as np

from src.connect4.game_state import Color
from src.connect4.moves_sequence import MovesSequence, save_moves_sequences_as_pickle, load_moves_sequences_from_pickle, add_moves_sequences_to_pickle, read_statistics, convert_moves_sequence_to_game_state
from src.connect4.make_decision import evaluate_a_move_with_science, generate_full_moves_sequence, generate_multiple_full_moves_sequences


@pytest.fixture
def test_path():
    test_path = 'output/moves_sequences/test.pkl'
    return test_path

@pytest.fixture
def number_of_sequences():
    number_of_sequences = 3 #100_000
    return number_of_sequences

def test_generate_full_moves_sequence(test_path):
    moves_sequence = generate_full_moves_sequence(yellow_bot=evaluate_a_move_with_science, red_bot=evaluate_a_move_with_science, first_player=Color.YELLOW)
    # game_state.plot()
    save_moves_sequences_as_pickle(moves_sequences=[moves_sequence], output_path=test_path)

def test_generate_multiple_move_sequences():
    generate_multiple_full_moves_sequences(yellow_bot=evaluate_a_move_with_science, red_bot=evaluate_a_move_with_science, first_player=Color.YELLOW, n=3)

def test_load_moves_sequences_from_pickle(test_path):
    load_moves_sequences_from_pickle(input_path=test_path)
    
def test_add_moves_sequences_to_pickle(test_path, number_of_sequences):
    moves_sequences = [generate_full_moves_sequence(yellow_bot=evaluate_a_move_with_science, 
                                                    red_bot=evaluate_a_move_with_science, 
                                                    first_player=Color.YELLOW) 
                                            for _ in range(number_of_sequences)]
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

# si on diminue la profondeur de la vision > on va beaucoup plsu vite : 100 entrainements en 5 secondes
# 1 min = 1000
# il faudrait definir un parametre qui donne le degre d'intelligence de make_decision_with_science

# TODO regarder comment paralléliser la génération des parties > regarder asyncio etc, en profiter
# pour se metre au clair sur les concepts de paralélisation, concurrence etc
# comment faire en sorte de pas avoir a observer tropde trucs mais j uiste ce qui va compter
# TODO sortir cette génération des test pour que ce soit plus pratique et integrer un timestamp
# TODO : mettrer bar de chargement