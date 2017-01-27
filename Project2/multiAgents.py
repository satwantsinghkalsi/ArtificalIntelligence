# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        curPos = currentGameState.getPacmanPosition()
        ghostStates=successorGameState.getGhostPositions()
        minGhostdistance=float("inf")
        minGhostPos=newPos
        for position in ghostStates:
            distance=manhattanDistance(position,newPos)
            minGhostdistance=min(distance,minGhostdistance)
        minfooddistance=float("inf")
        minfoodpos=minGhostPos
        for food in newFood.asList():
            distance=manhattanDistance(food,newPos)
            distance1=manhattanDistance(food,minGhostPos)
            minfooddistance=min(distance,minfooddistance)

        if minGhostdistance<2:
            minGhostdistance=-10000
        else:
            minGhostdistance=10000

        return minGhostdistance+1.0/minfooddistance+successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        level=0
        numOfAdv=gameState.getNumAgents()-1
        actionList=gameState.getLegalActions(0)
        successors=[]
        result=None
        value=float("-inf")
        for action in actionList:
            successors.append((gameState.generateSuccessor(0,action),action))
        for successor in successors:
            val=minimax(1,successor[0],self.depth,self.evaluationFunction)
            if val>value:
                value=val
                result=successor[1]
        return result
        util.raiseNotDefined()

def minimax(crntagent,state,depth,evaluationFunction):
    if depth<=0 or state.isWin() or state.isLose():
        return evaluationFunction(state)
    if crntagent==0:
        value = float("-inf")
    else:
        value=float("inf")
    actionList = state.getLegalActions(crntagent)
    successors = []
    for action in actionList:
        successors.append((state.generateSuccessor(crntagent, action), action))
    for successor in successors:
        if crntagent==0:
            value=max(value,minimax(crntagent+1,successor[0],depth,evaluationFunction))
        elif crntagent==state.getNumAgents()-1:
            value = min(value, minimax(0, successor[0], depth-1, evaluationFunction))
        else:
            value = min(value, minimax(crntagent+1, successor[0], depth, evaluationFunction))
    return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        result = None
        alpha = float("-inf")
        beta = float("inf")
        crntagent = 0
        curdepth = 0
        res = self.minmaxalphabeta(gameState, crntagent, curdepth, alpha, beta)
        return res[0]

    def minmaxalphabeta(self, gameState, crntagent, curdepth, alpha, beta):
        if crntagent >= gameState.getNumAgents():
            crntagent = 0
            curdepth += 1
        if curdepth >= self.depth or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))

        if crntagent == 0:

            return self.maxFunc(gameState, crntagent, curdepth, alpha, beta)
        else:

            return self.minFunc(gameState, crntagent, curdepth, alpha, beta)

    def minFunc(self, gameState, crntagent, depth, alpha, beta):
        actions = gameState.getLegalActions(crntagent)
        if not gameState.getLegalActions(crntagent):
            return self.evaluationFunction(gameState)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        value = (None, float("inf"))
        for action in actions:
            successor = gameState.generateSuccessor(crntagent, action)
            res = self.minmaxalphabeta(successor,crntagent+1, depth, alpha, beta)
            if res[1] < value[1]:
                value = (action, res[1])
            if value[1] < alpha:
                return value
            beta = min(beta, value[1])
        return value

    def maxFunc(self, gameState,crntagent,depth, alpha, beta):
        actions = gameState.getLegalActions(0)
        if not gameState.getLegalActions(crntagent):
            return self.evaluationFunction(gameState)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        value = (None, float("-inf"))
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            res = self.minmaxalphabeta(successor,crntagent+1, depth, alpha, beta)
            if res[1] > value[1]:
                value = (action, res[1])
            if value[1] > beta:
                return value
            alpha = max(alpha,value[1])
        return value
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        actionList = gameState.getLegalActions(0)
        successors = []
        result = None
        value = float("-inf")
        for action in actionList:
            successors.append((gameState.generateSuccessor(0, action), action))
        for successor in successors:
            val = expectimax(1, successor[0], self.depth, self.evaluationFunction)
            if val > value:
                value = val
                result = successor[1]

        return result
        util.raiseNotDefined()

def expectimax(crntagent, state, depth, evaluationFunction):
    if depth <= 0 or state.isWin() or state.isLose():
        return evaluationFunction(state)

    if crntagent == 0:
        value = float("-inf")
    else:
        value = 0
    actionList = state.getLegalActions(crntagent)
    successors = []

    for action in actionList:
        successors.append((state.generateSuccessor(crntagent, action), action))
    prob = 1.0 / len(successors)
    for successor in successors:

        if crntagent == 0:
            value = max(value,expectimax(crntagent + 1, successor[0], depth, evaluationFunction))
        elif crntagent == state.getNumAgents() - 1:
            value += prob*expectimax(0, successor[0], depth - 1, evaluationFunction)
        else:
            value +=prob* expectimax(crntagent+1, successor[0], depth, evaluationFunction)
    return value

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food = currentGameState.getFood()

    pos = currentGameState.getPacmanPosition()

    ghostStates = currentGameState.getGhostStates()
    foodList = food.asList()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()

    distanceGhost = float("inf")
    scared = 0
    times = 1
    for time in scaredTimes:
        times += time
        if time > 2:
            scared += 1

    avgDist = 1
    ghostCount = 0
    for ghost in ghostPositions:
        d = manhattanDistance(ghost, pos)
        avgDist += d
        if d <= 15:
            ghostCount += 1
        distanceGhost = min(d, distanceGhost)

    avgDist = float(avgDist) / len(ghostPositions)
    distanceFood = float("inf")

    for food in foodList:
        d = manhattanDistance(food, pos)
        distanceFood = min(d, distanceFood)

    count = len(foodList) + 1

    legalMoves = len(currentGameState.getLegalActions(0)) + 1

    if distanceGhost < 2:
        distanceGhost = -100000
    else:
        distanceGhost = 0


    return distanceGhost + 1.0 / distanceFood + 10000.0 / count - 50000 * ghostCount + 50000 * scared - 1000 / times + 1.0 / avgDist + 1000.0 * (currentGameState.getScore() + 1)
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

