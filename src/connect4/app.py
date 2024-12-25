from flask import Flask, jsonify, request, render_template
import time

from game import Game, GameState, Color

game = Game()
app = Flask(__name__)
is_thinking_computer = False 

# configuration parameters
PVE = True
WAITING_TIME = 0.6 # secs

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

def make_move(action):
    current_player_turn = game.get_current_player_turn()
    if action['action_type'] == 'play_column':
        game.play(action['column'])
    if action['action_type'] == 'play_randomly':
        game.play_randomly()
    if action['action_type'] == 'pass':
        pass
    response = generate_response_from_game(game)
    victory =  game.get_current_game_state().check_victory(player=current_player_turn)
    response['winning_player'] = current_player_turn.value if victory else Color.EMPTY.value
    return response

@app.route('/human_playing', methods=['POST'])
def make_move_human():
    global is_thinking_computer
    if is_thinking_computer: 
        return None
    # Assume we receive data through the POST request
    data = request.get_json()
    action = {'action_type' : 'play_column', 
                      'column' : data.get('column')}
    response = make_move(action)
    is_thinking_computer = True
    return jsonify(response)  

@app.route('/computer_playing', methods=['GET'])
def make_move_computer():
    time.sleep(WAITING_TIME)
    if PVE:
        action = {'action_type' : 'play_randomly'}
    else:
        action = {'action_type' : 'pass'}
    response = make_move(action)
    global is_thinking_computer 
    is_thinking_computer = False
    return jsonify(response)  

@app.route('/reset_button_clicked', methods=['POST'])
def reset_board():
    game.add_initialized_game_state()
    response = generate_response_from_game(game)
    return jsonify(response)

@app.route('/ctrl_z_button_clicked', methods=['POST'])
def ctrl_z():
    game.move_pointer_backward()
    response = generate_response_from_game(game)
    return jsonify(response)

@app.route('/ctrl_y_button_clicked', methods=['POST'])
def ctrl_y():
    game.move_pointer_forward()
    response = generate_response_from_game(game)
    return jsonify(response)
    
if __name__ == '__main__':
    app.run(debug=True)
