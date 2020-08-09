import os

class GameState:
    """
    A Layout manages the static information about the game board.
    """

    def __init__(self, layoutText):
        self.width = len(layoutText)
        self.height = len(layoutText[0])
        self.layoutText = layoutText
        self.restart()

    def restart(self):
        self.walls = [[c == '%' for c in row] for row in self.layoutText]
        self.food = [[c == '.' for c in row] for row in self.layoutText]
        for x, row in enumerate(self.layoutText):
            for y, cell in enumerate(row):
                if cell == 'P':
                    self.pacmanPos = (x, y)
        self.pacmanDir = Directions.EAST
        self.score = 0
        self.searchCost = 0



    def getSize(self):
        return self.width, self.height

    def getPacmanPos(self):
        return self.pacmanPos

    def getPacmanDir(self):
        return self.pacmanDir

    def getWalls(self):
        return self.walls

    def getFood(self):
        return self.food

    def movePacman(self, v):
        self.score -= 1
        self.pacmanPos = (self.pacmanPos[0] + v[0], self.pacmanPos[1] + v[1])
        dir = Actions.vectorToDirection(v)
        self.pacmanDir = dir;
        y, x = int(self.pacmanPos[0] + .5), int(self.pacmanPos[1] + .5)
        if self.food[y][x]:
            self.food[y][x] = False
            self.score += 10

def LoadGameState(filepath):
    if(not os.path.exists(filepath)):
        return None
    f = open(filepath)
    res = GameState([line.strip() for line in f])
    f.close()
    return res

def toList(grid):
    return [(x, y) for x, row in enumerate(grid) for y, cell in enumerate(row) if cell]

class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = { NORTH: WEST,
             SOUTH: EAST,
             EAST: NORTH,
             WEST: SOUTH}

    RIGHT = dict([(y, x) for x, y in list(LEFT.items())])

    REVERSE = { NORTH: SOUTH,
                SOUTH: NORTH,
                WEST: EAST,
                EAST: WEST,
                STOP: STOP}

class Actions:
    """
    A collection of state methods for manipulating move actions.
    """
    # Directions
    _directions = { Directions.NORTH: (-1, 0),
                    Directions.SOUTH: (1, 0),
                    Directions.EAST: (0, 1),
                    Directions.WEST: (0, -1)}

    _directionsAsList = list(_directions.items())

    TOLERANCE = 0.001

    @staticmethod
    def reverseDirection(action):
        return Directions.REVERSE[action]
    
    @staticmethod
    def vectorToDirection(vector):
        dy, dx = vector
        if dy > 0:
            return Directions.SOUTH
        if dy < 0:
            return Directions.NORTH
        if dx > 0:
            return Directions.EAST
        if dx < 0:
            return Directions.WEST
        return Directions.STOP

    @staticmethod
    def directionToVector(direction, speed = 1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)
    
    @staticmethod
    def getPossibleActions(position, direction, walls):
        possible = []
        x, y = position
        x_int, y_int = int(x + .5), int(y + .5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE):
            return [direction]
        
        for dir, vec in Actions._directionsAsList:
            dy, dx = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                possible.append(dir)
        return possible

    @staticmethod
    def getLegalNeighbors(position, walls):
        x, y = position
        x_int, y_int = int(x + .5), int(y + .5)
        neighbors = []
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_x = x_int + dx
            if next_x < 0 or next_x == walls.width:
                continue
            next_y = y_int + dy
            if next_y < 0 or next_y == walls.height:
                continue
            if not walls[next_x][next_y]:
                neighbors.append((next_x, next_y))
        return neighbors

    @staticmethod
    def getSuccessor(position, action):
        dx, dy = Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)

