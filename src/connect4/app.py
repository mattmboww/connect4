from flask import Flask, jsonify, request, render_template

from game import Game

game = Game()
game.initialize()
app = Flask(__name__)

def convert_game_to_json_compatible(game: Game = Game()):
    return [[cell.value for cell in row] for row in game.board.tolist()], game.player_turn.value

@app.route('/')
def index():
    board_json_compatible, player_turn_value = convert_game_to_json_compatible(game)
    return render_template('board.html', board=board_json_compatible, player_turn=player_turn_value)

@app.route('/box_clicking', methods=['POST'])
def receive_move():
    # Assume we receive data through the POST request
    data = request.get_json()
    column = data.get('column')
    game.play(column, player_turn=game.player_turn)
    board_json_compatible, player_turn_value = convert_game_to_json_compatible(game)
    response = {
        'board':  board_json_compatible, 
        'player_turn': player_turn_value
    }
    return jsonify(response)  

import numpy as np
from game import NUMBER_OF_COLUMNS, NUMBER_OF_ROWS, Color

@app.route('/reset_button_clicked', methods=['POST'])
def reset_board():
    # global game 
    # game = Game(board = np.full((NUMBER_OF_ROWS, NUMBER_OF_COLUMNS), Color.EMPTY), player_turn= Color.YELLOW )
    global game  
    game = game.initialize()

    board_json_compatible, player_turn_value = convert_game_to_json_compatible(game)
    response = {
        'board': board_json_compatible, 
        'player_turn': player_turn_value
    }
    return jsonify(response)

    

if __name__ == '__main__':
    app.run(debug=True)
