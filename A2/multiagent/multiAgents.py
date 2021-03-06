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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        if successorGameState.isWin():
            return successorGameState.getScore()
        score = 0
        shortestfood = float('inf')
        for food in newFood.asList():
            dist = util.manhattanDistance(newPos, food)
            if dist <= shortestfood:
                shortestfood = dist
        score -= 2*shortestfood
        score -= 50*len(newFood.asList())
        shortestghost = float('inf')
        for ghost in newGhostStates:
            dist = util.manhattanDistance(newPos, ghost.getPosition())
            if dist <= shortestghost:
                shortestghost = dist
        if shortestghost <= 2:
            return -float('inf')
        score += shortestghost

        return successorGameState.getScore() + score

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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def MinimaxFunc(self, gameState, depth, agentIndex, numGhost):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return "noMove", self.evaluationFunction(gameState)
        if agentIndex == 0:
            value = -float('inf')
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nxt_move, nxt_value = self.MinimaxFunc(gameState.generateSuccessor(0, action), 
                                                                    depth, 1, numGhost)
                if nxt_value > value:
                    value, bestmove = nxt_value, action
        else:
            value = float('inf')
            actions = gameState.getLegalActions(agentIndex)
            if agentIndex < numGhost:
                for action in actions:
                    nxt_move, nxt_value = self.MinimaxFunc(gameState.generateSuccessor(agentIndex,
                                                            action), depth, agentIndex+1, numGhost)
                    if nxt_value < value:
                        value, bestmove = nxt_value, action
            else:
                for action in actions:
                    nxt_move, nxt_value = self.MinimaxFunc(gameState.generateSuccessor(agentIndex,
                                                            action), depth-1, 0, numGhost)
                    if nxt_value < value:
                        value, bestmove = nxt_value, action
        return bestmove, value

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
        bestmove, bestvalue = self.MinimaxFunc(gameState, self.depth, 0, gameState.getNumAgents() - 1)

        return bestmove


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def ABminimax(self, gameState, depth, agentIndex, numGhost, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return "noMove", self.evaluationFunction(gameState)
        if agentIndex == 0:
            value = -float('inf')
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nxt_move, nxt_value = self.ABminimax(gameState.generateSuccessor(0, action), 
                                                  depth, 1, numGhost, alpha, beta)
                if nxt_value > value:
                    value, bestmove = nxt_value, action
                if value >= beta:
                    return bestmove, value
                alpha = max(alpha, value)
        else:
            value = float('inf')
            actions = gameState.getLegalActions(agentIndex)
            if agentIndex < numGhost:
                for action in actions:
                    nxt_move, nxt_value = self.ABminimax(gameState.generateSuccessor(agentIndex,
                        action), depth, agentIndex+1, numGhost, alpha, beta)
                    if nxt_value < value:
                        value, bestmove = nxt_value, action
                    if value <= alpha:
                        return bestmove, value
                    beta = min(beta, value)
            else:
                for action in actions:
                    nxt_move, nxt_value = self.ABminimax(gameState.generateSuccessor(agentIndex,
                        action), depth-1, 0, numGhost, alpha, beta)
                    if nxt_value < value:
                        value, bestmove = nxt_value, action
                    if value <= alpha:
                        return bestmove, value
                    beta = min(beta, value)
        return bestmove, value


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestmove, bestvalue = self.ABminimax(gameState, self.depth, 0, gameState.getNumAgents()-1, -float('inf'), float('inf'))

        return bestmove


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def Expective(self, gameState, depth, agentIndex, numGhost):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return "noMove", self.evaluationFunction(gameState)
        if agentIndex == 0:
            value = -float('inf')
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nxt_move, nxt_value = self.Expective(gameState.generateSuccessor(0, action), 
                        depth, 1, numGhost)
                if nxt_value > value:
                    value, bestmove = nxt_value, action
        else:
            value = 0
            actions = gameState.getLegalActions(agentIndex)
            if agentIndex < numGhost:
                for action in actions:
                    nxt_move, nxt_value = self.Expective(gameState.generateSuccessor(agentIndex,
                        action), depth, agentIndex+1, numGhost)
                    value, bestmove = float(value) + (1.0/float(len(actions))) * nxt_value, Directions.STOP
            else:
                for action in actions:
                    nxt_move, nxt_value = self.Expective(gameState.generateSuccessor(agentIndex,
                        action), depth-1, 0, numGhost)
                    value, bestmove = float(value) + (1.0/float(len(actions))) * nxt_value, Directions.STOP
        return bestmove, value

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestmove, bestvalue = self.Expective(gameState, self.depth, 0, gameState.getNumAgents() - 1)

        return bestmove


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"     
    newPos = currentGameState.getPacmanPosition() 
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newPower = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    closestFood = newFood.width + newFood.height
    for foodPos in newFood.asList():
        dist = util.manhattanDistance(newPos, foodPos)
        if dist < closestFood:
            closestFood = float(dist)
    ghostlst = []
    for ghostPos in newGhostStates:
        ghostlst.append(util.manhattanDistance(newPos, ghostPos.getPosition()))
    closestGhost = float(min(ghostlst))
    if closestGhost < 2:
        closestGhost = -1000 

    if max(newScaredTimes)!= 0 and closestGhost < max(newScaredTimes):
        closestGhost = abs(closestGhost)


    return -2*closestFood - 50*len(newFood.asList()) + closestGhost - 3*len(newPower) + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
