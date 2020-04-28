import readMaze as rM
from search import Node, Problem
import math
import functools


class PacmanProblem(Problem):
    def __init__(self, initial, goal, maze=None):
        self.initial = initial
        self.goal = goal
        if maze == None:
            self.maze, self.mazeY, self.mazeX = rM.readMaze()
        else:
            self.maze, self.mazeY, self.mazeX = rM.readMaze(maze)
    
    # for a given position returns the adjacent positions that are gray paths
    def adjacent(self, position):
        adjacent = []
        # left
        if self.maze[position[0], position[1]-1] == 2:
            if position[1] -1 < 0:
                adjacent.append((position[0], self.mazeX -1))
            else:
                adjacent.append((position[0], position[1]-1))
        # right
        if position[1] + 1 == self.mazeX and self.maze[position[0], 0] == 2:
            adjacent.append((position[0], 0))
        elif position[1] + 1 < self.mazeX and self.maze[position[0], position[1]+1] == 2:
            adjacent.append((position[0], position[1]+1))
                
        # up
        if self.maze[position[0]-1, position[1]] == 2:
            if position[0] -1 < 0:
                adjacent.append((self.mazeY-1, position[1]))
            else:
                adjacent.append((position[0]-1, position[1]))
        # down
        if position[0] + 1 == self.mazeY and self.maze[0, position[1]] == 2:
            adjacent.append((0, position[1]))
        elif position[0] + 1 < self.mazeY and self.maze[position[0]+1, position[1]] == 2:
            adjacent.append((position[0]+1, position[1]))
        
        return adjacent

    # returns the possible child states for the given state
    def actions(self, state):
        if len(state) == 0:
            return []

        states = []
        adjacent = self.adjacent(state[-1])
        for position in adjacent:
            stateCopy = state.copy()
            states.append(stateCopy.append(position))
        
        return states

    # the goal is reached if all positions that are reachable through the initial state are in the solution 
    # and the first and last positions in the solution are the initial position and goal position
    def goal_test(self, state):
        return all(position in state for position in set(self.positionsInSolution)) and state[-1] == self.goal and state[0] == self.initial
    
    def result(self, state, action):
        pass
    
    def path_cost(self, c, position1, action, position2):
        # Se as posicoes n forem adjacentes entao nao ha um caminho direto de pos1 pra pos2
        if abs(position1[0] - position2[0]) > 1 or abs(position1[1] - position2[1]) > 1:
            return math.inf
        return c+1

    # Retorna uma lista com todas as posicoes alcancaveis a partir da posicao dada, inclusive essa posicao
    def reachable_positions(self, startPosition):
        positions = []
        queue = [startPosition]

        while queue:
            position = queue.pop(0)
            positions.append(position)
            actions = self.adjacent(position)

            for action in actions:
                alreadyVisited = False
                for item in positions:
                    if item == action:
                        alreadyVisited = True
                        break

                if alreadyVisited == False:
                    queue.append(action)

        return set(positions)

    # Diz se uma posicao eh alcancavel a partir de outra (True ou False)
    def reachable(self, position1, position2):
        positions = self.reachable_positions(position1)
        return position2 in positions


    # Cada posicao andada custa 1, porem cada ponto unico recolhido vale 2
    def value(self, state):
        return -1 * len(state) + 2 * len(set(state))

    # Calcula a distancia entre duas posicoes, valido apenas para posicoes que fazem parte da sol
    @functools.lru_cache(maxsize=4096)
    def distance(self, position1, position2, returnPath=False, lim=100000):
        if position1 == position2:
            if returnPath:
                return 0, [position1]
            else:
                return 0

        # dicicionario com formato { item: [distancia, visitado (0 = nao, 1 = sim)], ... }
        d = dict.fromkeys(self.reachable_positions(position1), [math.inf, 0, []])
        d[position1] = [0, 0, [position1]]

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

            neighbors = self.adjacent(current)
            for neighbor in neighbors:
                if d[neighbor][1] == 0 and m+1 < d[neighbor][0]:
                    pathCopy = path.copy()
                    pathCopy.append(neighbor)
                    d[neighbor] = [m+1, 0, pathCopy]
                    if neighbor == position2:
                        return m+1, pathCopy

            current = None
            i = i+1

        try:
            if returnPath:
                return d[position2][0], pathCopy
            else:
                return d[position2][0]
        except KeyError:
            if returnPath:
                return math.inf, []
            else:
                return math.inf