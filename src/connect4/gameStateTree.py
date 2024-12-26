from enum import Enum, auto
import numpy as np
from typing import Self, List
import copy 

from gameState import GameState

class Game:

    def __init__(self: Self, 
                 current_game_state: GameState = None, 
                 potential_next_game_states: List[GameState] = []) -> None:

        self.current_game_state = current_game_state
        self.potential_next_game_states = potential_next_game_states

    def extend_toward_future():
        pass