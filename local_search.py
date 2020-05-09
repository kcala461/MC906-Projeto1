from search import Node
from utils import argmin_random_tie

def hill_climbing_search(problem):
    """
    Search for a local minimum following a certain optimization function
    The function used for this problem was the distance function from the
    actual point to the goal point. Which is the same used for our second heuristics informed search.
    """
    # we use these two variables at the time of visualisations
    iterations = 0
    all_node_colors = []
    node_colors = {k : 'white' for k in set(problem.reachable_positions(problem.initial))}
    
    frontier = [(Node(problem.initial))]
    explored = set()
    
    # modify the color of frontier nodes to orange
    node_colors[Node(problem.initial).state] = "orange"
    iterations += 1
    all_node_colors.append(dict(node_colors))
    
    while True:
        # Popping first node of stack
        node = frontier.pop()

        # modify the currently searching node to red
        node_colors[node.state] = "red"
        iterations += 1
        all_node_colors.append(dict(node_colors))
        
        neighbors = node.expand(problem)
        if not neighbors:
            break
        # find the minimum between the neighbors
        neighbor = argmin_random_tie(neighbors, key=lambda node: problem.h2(node))
        
        # trying to find minimum 
        if problem.h2(neighbor) > problem.h2(node):
            # node is already the local minimum
            node_colors[node.state] = "green"
            all_node_colors.append(dict(node_colors))
            return iterations, all_node_colors, node
        
        # expand only for painting
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)
        
        for n in frontier:
            # modify the color of frontier nodes to orange
            node_colors[n.state] = "orange"
            all_node_colors.append(dict(node_colors))
        
        frontier.clear()
        frontier.append(neighbor) # append the last
            
        explored.add(node.state)

        # modify the color of explored nodes to gray
        node_colors[node.state] = "gray"
        
    return None