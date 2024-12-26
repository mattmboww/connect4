from enum import Enum, auto
import numpy as np
from typing import Self, List
import copy 

from src.connect4.game_state import GameState

class GameStateTree:

    def __init__(self: Self, 
                 current_game_state: GameState = None, 
                 potential_next_game_states: List['GameStateTree'] = None) -> None:

        self.current_game_state = current_game_state
        self.potential_next_game_states = potential_next_game_states

    def is_leaf(self: Self) -> bool:
        return self.potential_next_game_states == []
    
    def get_all_leaves(self: Self) -> List['GameStateTree']:
        all_leaves = []
        game_state_trees_to_explore = [self]
        while game_state_trees_to_explore != []:
            currently_explored_game_state_tree = game_state_trees_to_explore[0]
            print(currently_explored_game_state_tree)
            if currently_explored_game_state_tree.is_leaf():
                all_leaves.append(currently_explored_game_state_tree)
            game_state_trees_to_explore += self.potential_next_game_states
            game_state_trees_to_explore = game_state_trees_to_explore[1:]
        return all_leaves
    
    def extend_to_future(self: Self, depth: int) -> Self:
        pass

        # donner la profondeur 