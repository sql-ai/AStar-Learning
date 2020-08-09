# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
In search.py, you will implement generic search algorithms
"""
from gameState import *
from gameState import Directions
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessor(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expending to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
          actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined

class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost functions. This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x, y) positions in a pacman game.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal = (1, 1), start=None):
        """
        Stores the start and goal
        
        gameState: A GameState object
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPos()
        self.goal = goal
        self.costFn = costFn

        # For display purposes
        self._visited, self.visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal
        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

        For a given state, this function return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action required
        to get there, and 'stepCost' is the incremental cost of expanding
        to that successor
        """
        self.visitedlist.append(state)

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        included an illegal move, return 999999.
        """
        if actions == None:
            return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += self.costFn(x, y)
        return cost

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze. For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from gameState import Directions
    s = Directions.SOUTH
    W = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """Teach Pac-man agent how to use DFS to plan paths \
        through its maze world and find foods. """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Teach Pac-man agent Breadth First search algorithm to find paths \
        through its maze world."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Teach Pac-man agent uniform-cost search algorithm to find paths \
        through its maze world."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic functions estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.
    """
    return 0

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

def aStarSearch(problem, heuristic=manhattanHeuristic):
    """Teach Pac-man agent the A* graph search algorithm to find paths \
        through its maze world."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()

def adverserialSearch(problem, heuristic=nullHeuristic):
    """Teach pac-man minimax, expectimax adversarial search algorithms \
        find foods and avoid ghosts."""
    "*** YOUR CODE HERE ***"
    raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
adverserial = adverserialSearch