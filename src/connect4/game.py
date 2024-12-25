from enum import Enum, auto
import numpy as np
from typing import Self, List
import copy 
import random


from game_state import GameState, Color, NUMBER_OF_COLUMNS

class Game:

    def __init__(self: Self, game_states: List[GameState] = None, pointer: int = 0) -> None:
        if game_states is None:
            initial_game_state = GameState().initialize()
            self.game_states = [initial_game_state]
        self.pointer = pointer

    def play(self: Self, column: int) -> Self:
        current_game_state = self.get_current_game_state()
        current_game_state = copy.deepcopy(current_game_state)
        current_game_state.play(column)
        self.cut_game_states()
        self.game_states.append(current_game_state)
        self.move_pointer_forward()
        return self
    
    def play_randomly(self: Self) -> Self:
        random_column = random.randint(0, NUMBER_OF_COLUMNS-1)
        return self.play(random_column)
    
    def get_current_game_state(self: Self) -> GameState:
        assert len(self.game_states) > 0
        return self.game_states[self.pointer]
    
    def get_current_player_turn(self: Self) -> Color:
        return self.get_current_game_state().player_turn
    
    def get_current_board(self: Self) -> Color:
        return self.get_current_game_state().board
    
    def add_initialized_game_state(self: Self) -> Self:
        self.cut_game_states()
        self.game_states.append(GameState().initialize())
        self.move_pointer_forward()
        return self  
    
    def cut_game_states(self: Self) -> Self:
        self.game_states = self.game_states[:self.pointer+1]
        return self
    
    def move_pointer_backward(self: Self) -> Self:
        assert self.pointer > 0
        self.pointer -= 1
        return self 
    
    def move_pointer_forward(self: Self) -> Self:
        assert self.pointer < len(self.game_states)-1
        self.pointer += 1
        return self 

