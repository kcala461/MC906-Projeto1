

from search import Node
import sys

class PriorityQueue:
    def __init__(self, maxsize=5000):
        self.maxsize = maxsize
        self.items = []
        self._index = 0

    def append(self, item, priority):
        if len(self.items) < self.maxsize:
            self.items.append((item, priority))

    def pop(self):
        self.items.sort(key=lambda x:x[1])
        return self.items.pop(0)[0]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.items):
            result = self.items[self._index]
            self._index = self._index + 1
            return result
        raise StopIteration

    def isEmpty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

def best_first_graph_search_for_vis(problem, f):
    iterations = 0
    all_node_colors = []
    node_colors = {k : 'white' for k in set(problem.reachable_positions(problem.initial))}
    
    node = Node(problem.initial)
    
    node_colors[node.state] = "red"
    iterations += 1
    all_node_colors.append(dict(node_colors))
    
    frontier = PriorityQueue()
    frontier.append(node, f(node))

    node_colors[node.state] = "orange"
    iterations += 1
    all_node_colors.append(dict(node_colors))
    
    explored = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        
        node_colors[node.state] = "red"
        iterations += 1
        all_node_colors.append(dict(node_colors))
        
        if problem.goal_test([node.state for node in node.path()]):
            # Todos os nós que estavam sendo explorados são abandonados
            for item in node_colors.keys():
                if node_colors[item] != "white":
                    node_colors[item] = "gray"

            for item in node.path():
                node_colors[item.state] = "green"
                node_colors[problem.initial] = "red"
 
            iterations += 1
            all_node_colors.append(dict(node_colors))
            return(iterations, all_node_colors, node)
        
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child, f(child))
                node_colors[child.state] = "orange"
                iterations += 1
                all_node_colors.append(dict(node_colors))
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child, f(child))
                    node_colors[child.state] = "orange"
                    iterations += 1
                    all_node_colors.append(dict(node_colors))

        node_colors[node.state] = "gray"
        iterations += 1
        all_node_colors.append(dict(node_colors))
    return iterations, all_node_colors, node

def astar_search_graph(problem, h=None , g=None):
    if h == None:
        h = problem.h2
    if g == None:
        g = problem.g
    iterations, all_node_colors, node = best_first_graph_search_for_vis(problem, 
                                                                lambda n: g(n) + h(n))
    return(iterations, all_node_colors, node)



def greedy_best_first_search(problem, h=None):
    """Greedy Best-first graph search is an informative searching algorithm with f(n) = h(n).
    You need to specify the h function when you call best_first_search, or
    else in your Problem subclass."""
    if h == None:
        h = problem.h2
    iterations, all_node_colors, node = best_first_graph_search_for_vis(problem, lambda n: h(n))
    return(iterations, all_node_colors, node)

def uniform_cost_search(problem, display=False):
    iterations, all_node_colors, node = best_first_graph_search_for_vis(problem, lambda node: node.path_cost)
    return(iterations, all_node_colors, node)

# def argmax_random_tie(neighbors, key):
#     if key == None:
#         key = problem.h

def hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""
    current = Node(problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors,
                                     key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) <= problem.value(current.state):
            break
        current = neighbor
    return current.state



def recursive_best_first_search_for_vis(problem, h=None):
    """[Figure 3.26] Recursive best-first search"""
    # we use these two variables at the time of visualizations
    iterations = 0
    all_node_colors = []
    node_colors = {k : 'white' for k in set(problem.reachable_positions(problem.initial))}
    
    h = problem.h2
    
    def RBFS(problem, node, flimit):
        nonlocal iterations
        def color_city_and_update_map(node, color):
            node_colors[node.state] = color
            nonlocal iterations
            iterations += 1
            all_node_colors.append(dict(node_colors))
            
        if problem.goal_test([node.state for node in node.path()]):
            color_city_and_update_map(node, 'green')
            return (iterations, all_node_colors, node), 0  # the second value is immaterial
        
        successors = node.expand(problem)
        if len(successors) == 0:
            color_city_and_update_map(node, 'gray')
            return (iterations, all_node_colors, None), sys.maxsize
        
        for s in successors:
            color_city_and_update_map(s, 'orange')
            s.f = max(s.path_cost + h(s), node.f)
            
        while True:
            # Order by lowest f value
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if problem.goal_test([best]):
                color_city_and_update_map(best, 'green')
                return (iterations, all_node_colors, best) 
            if best.f > flimit:
                color_city_and_update_map(node, 'gray')
                return (iterations, all_node_colors, None), best.f
            
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = sys.maxsize
                
            node_colors[node.state] = 'gray'
            node_colors[best.state] = 'red'
            iterations += 1
            all_node_colors.append(dict(node_colors))
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result[2] is not None:
                color_city_and_update_map(node, 'green')
                return result, best.f
            else:
                color_city_and_update_map(node, 'red')
            
    node = Node(problem.initial)
    node.f = h(node)
    
    node_colors[node.state] = 'red'
    iterations += 1
    all_node_colors.append(dict(node_colors))
    result, bestf = RBFS(problem, node, sys.maxsize)
    return result

# def recursive_best_first_search(problem, h=None):
#     """[Figure 3.26] Recursive best-first search (RBFS) is an
#     informative search algorithm. Like A*, it uses the heuristic
#     f(n) = g(n) + h(n) to determine the next node to expand, making
#     it both optimal and complete (iff the heuristic is consistent).
#     To reduce memory consumption, RBFS uses a depth first search
#     and only retains the best f values of its ancestors."""
#     h = problem.h
#     def RBFS(problem, node, flimit):
#         if problem.goal_test(node.state):
#             return node, 0   # (The second value is immaterial)
#         successors = node.expand(problem)
#         if len(successors) == 0:
#             return None, infinity
#         for s in successors:
#             s.f = max(s.path_cost + h(s), node.f)
#         while True:
#             # Order by lowest f value
#             successors.sort(key=lambda x: x.f)
#             best = successors[0]
#             if best.f > flimit:
#                 return None, best.f
#             if len(successors) > 1:
#                 alternative = successors[1].f
#             else:
#                 alternative = infinity
#             result, best.f = RBFS(problem, best, min(flimit, alternative))
#             if result is not None:
#                 return result, best.f

#     node = Node(problem.initial)
#     node.f = h(node)
#     result, bestf = RBFS(problem, node, infinity)
#     return result



        