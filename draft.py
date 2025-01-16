from pathlib import Path

from src.connect4.moves_sequence import read_statistics, get_moves_sequences_with_game_state
from src.connect4.game_state import GameState, Color

from src.connect4.make_decision import evaluate_game_state_with_history, load_moves_sequences_from_pickle



input_path = Path('/Users/matthieumbargaowona/Desktop/4FVN/connect4/output/moves_sequences/test_dumb.pkl')
stats = read_statistics(input_path)
print(stats)

initial_state=GameState().initialize()
value_of_initial_state_for_yellow = evaluate_game_state_with_history(initial_state, player=Color.YELLOW, moves_sequences=load_moves_sequences_from_pickle(input_path))
print(value_of_initial_state_for_yellow)

second_state = initial_state.play(0)
value_of_second_state_for_yellow = evaluate_game_state_with_history(second_state, player=Color.RED, moves_sequences=load_moves_sequences_from_pickle(input_path))
print(value_of_second_state_for_yellow)

third_state = initial_state.play(0)
value_of_second_state_for_yellow = evaluate_game_state_with_history(second_state, player=Color.RED, moves_sequences=load_moves_sequences_from_pickle(input_path))
print(value_of_second_state_for_yellow)

# j'ai un premier echantillon de taille 100_000 sur lequel faire des stats
# il est full dumb
# TODO : alternance quand on génére les résultats pour déterminer qui commecne

loaded_moves_sequences = load_moves_sequences_from_pickle(input_path)
print(loaded_moves_sequences[0].moves)
print(loaded_moves_sequences[1].moves)

# TODO : problem : it is time consuming to compute value of a game state, can be used to play but no realluy to
# generate more intelligent games for now...

