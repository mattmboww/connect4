from typing import Self, List

from src.connect4.game_state import GameState

class GameStateTree:

    def __init__(self: Self, 
                 current_game_state: GameState = None, 
                 children_game_state_trees: List['GameStateTree'] = None) -> None:

        self.current_game_state = current_game_state
        self.children_game_state_trees = children_game_state_trees
    
    def is_leaf(self: Self) -> bool:
        return self.children_game_state_trees == []
    
    def get_all_nodes(self: Self) -> List['GameStateTree']:
        all_nodes = []
        game_state_trees_to_explore = [{'game_state_tree': self, 
                                        'father' : None, 
                                        'depth': 0}]
        explored_game_states = set()
        while game_state_trees_to_explore:
            currently_explored_game_state_tree = game_state_trees_to_explore.pop(0)
    
            all_nodes.append(currently_explored_game_state_tree)
            
            for next_game_state in currently_explored_game_state_tree['game_state_tree'].children_game_state_trees:
                if next_game_state not in explored_game_states:
                    game_state_trees_to_explore.append({'game_state_tree': next_game_state, 
                                                        'father' : currently_explored_game_state_tree['game_state_tree'],
                                                        'depth': currently_explored_game_state_tree['depth']+1})
                    explored_game_states.add(next_game_state)  

        return all_nodes
    
    def get_all_leaves(self: Self) -> List['GameStateTree']:
        return [node['game_state_tree'] for node in self.get_all_nodes() if node['game_state_tree'].is_leaf()]
        
    def get_depth(self: Self, node: 'GameStateTree') -> int:
        for some_node in self.get_all_nodes():
            if some_node['game_state_tree'] is node:
                return some_node['depth']
            
    def get_height(self: Self) -> int:
        return max([node['depth'] for node in self.get_all_nodes()])

    def get_father(self: Self, node: 'GameStateTree') -> 'GameStateTree':
        for some_node in self.get_all_nodes():
            if some_node['game_state_tree'] is node:
                return some_node['father']
    
    def extend_from_root(self: Self) -> Self:
        possible_futures = self.current_game_state.get_possible_futures()
        self.children_game_state_trees = [GameStateTree(possible_future, []) for possible_future in possible_futures]
        return self
    
    def extend(self: Self, depth: int) -> Self:
        for _ in range(depth):
            all_leaves = self.get_all_leaves()
            for leaf in all_leaves:
                leaf.extend_from_root()
        return self
    
    @staticmethod
    def compute_game_state_value(game_state: GameState, value_function: function, depth: int) -> float:
        game_state_tree = GameStateTree(game_state, [])
        game_state_tree.extend(depth)
        for depth in 


            
        return 0
    
