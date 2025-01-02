from src.connect4.game_state import GameState, Color

def dummy_value_function(game_state: GameState, player: Color):
    return 0.0

# value is 1 if victory is possible, -1 if victory possible for opp, else 0
def bipolar_value_function(game_state: GameState, player: Color):
    """ 
    I take the point of view of a player : 
    if it is my turn potential win or deadly move -> +1, else 0
    if it is my opponent turn, if he wins or deadly move -> -1 
    """
    current_player = game_state.player_turn
    if current_player == player:
        return 1.0 if game_state.check_if_victory_is_possible(current_player) or game_state.check_if_exists_a_deadly_move(current_player) else 0.0  
    else:
        return -1.0 if game_state.check_if_victory_is_possible(current_player) or game_state.check_if_exists_a_deadly_move(current_player) else 0.0
         
    


