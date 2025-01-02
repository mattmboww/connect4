from typing import Self, List
import copy

from src.connect4.game_state import GameState, Color

class GameStateTree:

    def __init__(self: Self, 
                 current_game_state: GameState = None, 
                 children_game_state_trees: List['GameStateTree'] = None) -> None:

        if current_game_state is None: 
            raise ValueError('Error : game_state should be specified.')
        if children_game_state_trees is None:
            children_game_state_trees = []

        self.current_game_state = current_game_state
        self.children_game_state_trees = children_game_state_trees
        self.value = None
    
    def is_leaf(self: Self) -> bool:
        return self.children_game_state_trees == []
    
    def get_all_subtrees(self: Self) -> List['GameStateTree']:
        all_subtrees = []
        game_state_trees_to_explore = [{'game_state_tree': self, 
                                        'father' : None, 
                                        'depth': 0}]
        explored_game_states = set()
        while game_state_trees_to_explore:
            currently_explored_game_state_tree = game_state_trees_to_explore.pop(0)
    
            all_subtrees.append(currently_explored_game_state_tree)
            
            for next_game_state in currently_explored_game_state_tree['game_state_tree'].children_game_state_trees:
                if next_game_state not in explored_game_states:
                    game_state_trees_to_explore.append({'game_state_tree': next_game_state, 
                                                        'father' : currently_explored_game_state_tree['game_state_tree'],
                                                        'depth': currently_explored_game_state_tree['depth']+1})
                    explored_game_states.add(next_game_state)  

        return all_subtrees
    
    def get_all_leaves(self: Self) -> List['GameStateTree']:
        return [node['game_state_tree'] for node in self.get_all_subtrees() if node['game_state_tree'].is_leaf()]
        
    def get_depth(self: Self, node: 'GameStateTree') -> int:
        for some_node in self.get_all_subtrees():
            if some_node['game_state_tree'] is node:
                return some_node['depth']
            
    def get_height(self: Self) -> int:
        return max([node['depth'] for node in self.get_all_subtrees()]) + 1

    def get_father(self: Self, node: 'GameStateTree') -> 'GameStateTree':
        for some_node in self.get_all_subtrees():
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
    
    def compute_game_state_tree_value(self: Self, value_function: 'function', player: Color) -> float:
        all_subtrees = [subtree['game_state_tree'] for subtree in self.get_all_subtrees()]
        while self.value is None:
            for subtree in all_subtrees:
                subtree_children_values = [subtree_child.value for subtree_child in subtree.children_game_state_trees]
                if subtree.is_leaf():
                    subtree.value = value_function(subtree.current_game_state, player)
                elif all([isinstance(subtree_children_value, float) for subtree_children_value in subtree_children_values]):
                    subtree.value = max(subtree_children_values) if subtree.current_game_state.player_turn == player else min(subtree_children_values)
                else:
                    pass   
                if subtree==self:
                    print('self')
                else:
                    print('child')
                print(subtree.current_game_state.board)
                print('subtree: ', subtree.value)
                print('subtree: ', subtree.current_game_state.player_turn)
                print('self: ', self.value)
      
        return self.value
    
    @staticmethod
    def compute_game_state_value(game_state: GameState, value_function: 'function', player: Color, depth) -> float:
        game_state_tree = GameStateTree(game_state)
        game_state_tree.extend(depth)

        return game_state_tree.compute_game_state_tree_value(value_function, player)
        
    
# je parcours les noeuds tant que le pere n'a pas de valeur
# si j'ai un noeud sans enfant, ou si tous ses enfants ont une valeur, je calcule la valeur de mon noeud
# on continue jusqu'à tout avoir