from Problem import Node


class PriorityQueue:
    def __init__(self, maxsize=5000):
        self.maxsize = maxsize
        self.items = []
        self._index = 0

    def append(self, item, priority):
        if len(self.items) < self.maxsize:
            self.items.append((item, priority))

    def pop(self):
        self.items.sort(key=lambda x: x[1])
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
    node_colors = {k: 'white' for k in set(problem.reachable_positions(problem.initial))}

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
            node_colors[node.state] = "green"
            iterations += 1
            all_node_colors.append(dict(node_colors))
            return (iterations, all_node_colors, node)

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

def greedy_best_first_search(problem, h=None):
    """Greedy Best-first graph search is an informative searching algorithm with f(n) = h(n).
    You need to specify the h function when you call best_first_search, or
    else in your Problem subclass."""
    if h == None:
        h = problem.h2
    iterations, all_node_colors, node = best_first_graph_search_for_vis(problem, lambda n: h(n))
    return (iterations, all_node_colors, node)


def uniform_cost_search(problem, display=False):
    iterations, all_node_colors, node = best_first_graph_search_for_vis(problem, lambda node: node.path_cost)
    return (iterations, all_node_colors, node)

def astar_search_graph(problem, h=None, g=None):
    if h is None:
        h = problem.h
    if g is None:
        g = problem.g
    iterations, all_node_colors, node = best_first_graph_search_for_vis(problem, lambda n: g(n) + h(n))
    return iterations, all_node_colors, node