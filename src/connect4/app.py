from flask import Flask, jsonify, request, render_template

from game import Game, GameState, Color

# game_state = GameState()
# game_state.initialize()
game = Game()
app = Flask(__name__)

def convert_game_state_to_json_compatible(game_state: GameState = GameState()):
    return [[cell.value for cell in row] for row in game_state.board.tolist()], game_state.player_turn.value

@app.route('/')
def index():
    game_state = game.get_current_game_state()
    board_json_compatible, player_turn_value = convert_game_state_to_json_compatible(game_state)
    return render_template('board.html', board=board_json_compatible, player_turn=player_turn_value)

@app.route('/box_clicking', methods=['POST'])
def receive_move():
    # Assume we receive data through the POST request
    data = request.get_json()
    column = data.get('column')
    game_state = game.get_current_game_state()
    current_player_turn = game.get_current_player_turn()
    game.play(column, player_turn=current_player_turn)
    game_state = game.get_current_game_state()
    victory = game_state.check_victory(player=current_player_turn)
    new_board_json_compatible, new_player_turn_value = convert_game_state_to_json_compatible(game_state)
    response = {
        'board':  new_board_json_compatible, 
        'player_turn': new_player_turn_value, 
        'winning_player': current_player_turn.value if victory else Color.EMPTY.value 
    }
    return jsonify(response)  

@app.route('/reset_button_clicked', methods=['POST'])
def reset_board():
    global game
    game.add_initialized_game_state()
    game_state = game.get_current_game_state()
    board_json_compatible, player_turn_value = convert_game_state_to_json_compatible(game_state)
    response = {
        'board': board_json_compatible, 
        'player_turn': player_turn_value
    }
    return jsonify(response)

@app.route('/cancel_button_clicked', methods=['POST'])
def cancel_move():
    pass
    

if __name__ == '__main__':
    app.run(debug=True)
