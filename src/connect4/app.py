from flask import Flask, jsonify, request, render_template
import time
import random

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.connect4.game import Game, GameState, Color

from src.connect4.make_decision import make_scientific_decision_with_depth


game = Game()
app = Flask(__name__)
is_thinking_computer = False 
game_over = False

# configuration parameters
PVE = True
WAITING_TIME = 0 # secs
COMPUTER_VISION_DEPTH = 2
# with 0 and not V2: it seems it makes pretty good decisions, wiht more... ?

def convert_game_state_to_json_compatible(game_state: GameState = GameState()):
    return [[cell.value for cell in row] for row in game_state.board.tolist()], game_state.player_turn.value

def generate_response_from_game(game):
    game_state = game.get_current_game_state()
    new_board_json_compatible, new_player_turn_value = convert_game_state_to_json_compatible(game_state)
    response = {
        'board':  new_board_json_compatible, 
        'player_turn': new_player_turn_value, 
    }
    return response

@app.route('/')
def index():
    game_state = game.get_current_game_state()
    board_json_compatible, player_turn_value = convert_game_state_to_json_compatible(game_state)
    return render_template('board.html', board=board_json_compatible, player_turn=player_turn_value)

def make_move(action: dict):
    current_player_turn = game.get_current_player_turn()
    global game_over
    if game_over:
        raise ValueError('Game is over, there is no point clicking...')

    match action['action_type']:
        case 'play_column_chosen_by_human':
            decision = action['column']
            game.play(decision)
        case 'play_scientific_decision':
            current_game_state = game.get_current_game_state()
            decision = make_scientific_decision_with_depth(current_game_state,
                                                player=current_player_turn, 
                                                use_random=False, 
                                                depth=COMPUTER_VISION_DEPTH
                                                )
            game.play(decision)
        case 'pass':
            pass
        case _:
            raise ValueError('What the heck?!')

    response = generate_response_from_game(game)
    game_over =  game.get_current_game_state().check_new_victory(decision, player=current_player_turn)
    response['winning_player'] = current_player_turn.value if game_over else Color.EMPTY.value

    return response

@app.route('/human_playing', methods=['POST'])
def make_move_human():
    global is_thinking_computer
    if is_thinking_computer: 
        return None
    # Assume we receive data through the POST request
    data = request.get_json()
    action = {'action_type' : 'play_column_chosen_by_human', 
                      'column' : data.get('column')}
    response = make_move(action)
    is_thinking_computer = True
    return jsonify(response)  

@app.route('/computer_playing', methods=['GET'])
def make_move_computer():
    time.sleep(WAITING_TIME*PVE)
    if PVE:
        action = {'action_type' : 'play_scientific_decision'}
    else:
        action = {'action_type' : 'pass'}
    response = make_move(action)
    global is_thinking_computer 
    is_thinking_computer = False
    return jsonify(response)  

@app.route('/reset_button_clicked', methods=['POST'])
def reset_board():
    global game_over
    global is_thinking_computer 
    game_over = False
    is_thinking_computer = False
    game.add_initialized_game_state()
    response = generate_response_from_game(game)
    return jsonify(response)

@app.route('/ctrl_z_button_clicked', methods=['POST'])
def ctrl_z():
    global game_over
    global is_thinking_computer 
    game_over = False
    is_thinking_computer = False
    game.move_pointer_backward()
    response = generate_response_from_game(game)
    return jsonify(response)

@app.route('/ctrl_y_button_clicked', methods=['POST'])
def ctrl_y():
    game.move_pointer_forward()
    response = generate_response_from_game(game)
    return jsonify(response)
    
if __name__ == '__main__':
    app.run(debug=True) # localhost
    # app.run(host='0.0.0.0', port=5000) 
