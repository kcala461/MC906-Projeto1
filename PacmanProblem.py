import readMaze as rM
from problem import Problem
from node import Node
import math


class PacmanProblem(Problem):
    def __init__(self, initial, goal, maze=None):
        self.initial = initial
        self.goal = goal
        if maze == None:
            self.maze, self.mazeY, self.mazeX = rM.readMaze()
        else:
            self.maze, self.mazeY, self.mazeX = rM.readMaze(maze)
    
    def actions(self, state):
        actions = []
        # left
        if self.maze[state[0], state[1]-1] == 2:
            if state[1] -1 < 0:
                actions.append((state[0], self.mazeX -1))
            else:
                actions.append((state[0], state[1]-1))
        # right
        if state[1] + 1 == self.mazeX and self.maze[state[0], 0] == 2:
            actions.append((state[0], 0))
        elif state[1] + 1 < self.mazeX and self.maze[state[0], state[1]+1] == 2:
            actions.append((state[0], state[1]+1))
                
        # up
        if self.maze[state[0]-1, state[1]] == 2:
            if state[0] -1 < 0:
                actions.append((self.mazeY-1, state[1]))
            else:
                actions.append((state[0]-1, state[1]))
        # down
        if state[0] + 1 == self.mazeY and self.maze[0, state[1]] == 2:
            actions.append((0, state[1]))
        elif state[0] + 1 < self.mazeY and self.maze[state[0]+1, state[1]] == 2:
            actions.append((state[0]+1, state[1]))
        
        return actions
    
    def result(self, state, action):
        return action
    
    def path_cost(self, c, state1, action, state2):
        return c+1

    def reachable_positions(self, state):
        positions = []
        queue = [state]

        while queue:
            position = queue.pop(0)
            positions.append(position)
            actions = self.actions(position)

            for action in actions:
                alreadyVisited = False
                for item in positions:
                    if item == action:
                        alreadyVisited = True
                        break

                if alreadyVisited == False:
                    queue.append(action)

        return positions

    def reachable(self, state1, state2):
        positions = self.reachable_positions(state1)

        return state2 in positions

    def value(self, state):
        return -1

    # Calcula a distancia entre duas posicoes, valido apenas para posicoes que fazem parte da sol
    # Usando djikstra
    def distance(self, state1, state2, lim=100000):
        if state1 == state2:
            return 0, [state1]

        # dicicionario com formato item: [distancia, visitado (0 = nao, 1 = sim)]
        d = dict.fromkeys(self.reachable_positions(state1), [math.inf, 0, []])
        d[state1] = [0, 0, [state1]]

        i = 0
        while min({l[1] for l in d.values()}) == 0 and i < lim:
            m = math.inf
            current = None
            path = []
            for k, v in d.items():
                if v[1] == 0 and v[0] < m:
                    current = k
                    m = v[0]
                    path = v[2]

            d[current] = [m, 1, path]

            neighbors = self.actions(current)
            for neighbor in neighbors:
                if d[neighbor][1] == 0 and m+1 < d[neighbor][0]:
                    pathCopy = path.copy()
                    pathCopy.append(neighbor)
                    d[neighbor] = [m+1, 0, pathCopy]
                    if neighbor == state2:
                        return m+1, pathCopy

            current = None
            i = i+1

        try:
            return d[state2][0], pathCopy
        except KeyError:
            return math.inf, []