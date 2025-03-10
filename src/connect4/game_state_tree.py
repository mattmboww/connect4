from typing import Self, List
import copy

from src.connect4.game_state import GameState, Color
from typing import List, Optional

import matplotlib.pyplot as plt
import networkx as nx

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
    
    def to_networkx_graph(self) -> nx.DiGraph:
        """
        Convert the GameStateTree to a networkx graph, where each node's name is
        the memory address of the subtree (id()), and edges represent parent-child relationships.
        """
        graph = nx.DiGraph()
        def add_subtree_to_graph(tree: 'GameStateTree', matching_tree_and_id):
            node_id = id(tree)
            graph.add_node(node_id)  # Add the node
            # Add edges for children
            matching_tree_and_id[node_id] = tree
            for child in tree.children_game_state_trees:
                child_id = id(child)
                graph.add_node(child_id)  # Ensure the child is added as a node
                graph.add_edge(node_id, child_id)  # Add an edge from parent to child
                matching_tree_and_id[child_id] = child
                # Recursively add the child's subtrees
                add_subtree_to_graph(child, matching_tree_and_id)
            return matching_tree_and_id

        matching_tree_and_id = add_subtree_to_graph(self, matching_tree_and_id={})
        return graph, matching_tree_and_id
    
    def plot(self: Self) -> None:
        graph, matching_node_id_to_subtree = self.to_networkx_graph()
        pos = nx.spring_layout(graph, seed=42, k=0.5, iterations=50)  
        labels = {index: matching_node_id_to_subtree[index].value for index in matching_node_id_to_subtree}
        nx.draw(graph, pos, with_labels=True, labels=labels, node_size=300, node_color="skyblue", font_size=10, font_weight='bold', edge_color='gray')
        plt.title("Graph of GameStateTree")
        plt.show()

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
        possible_future_game_state = list(self.current_game_state.get_possible_futures().values())
        self.children_game_state_trees = [GameStateTree(possible_future, []) for possible_future in possible_future_game_state]
        return self
    
    def extend(self: Self, depth: int) -> Self:
        for _ in range(depth):
            all_leaves = self.get_all_leaves()
            for leaf in all_leaves:
                leaf.extend_from_root()
        return self
    
    @staticmethod
    def generate_tree_from_game_state(game_state: GameState, depth:int) -> 'GameStateTree':
        return GameStateTree(game_state).extend(depth)
    
    def reinitialize_all_values(self: Self) -> Self:
        for subtree in self.get_all_subtrees():
            subtree['game_state_tree'].value = None
    
 