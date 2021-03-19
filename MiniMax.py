import numpy as np

from GameController import GameController


class MiniMax:

    def __init__(self):
        '''
        0: Human (goes down)
        1: AI (AI goes up)
        '''

    def alpha_beta(self, state_object, depth: int, alpha: float, beta: float):
        if depth == 0 or self.Terminal_Test(state_object):
            return self.Eval(state_object), None
        return self.MaxValue(state_object, depth, alpha, beta)

    def MaxValue(self, state,depth, alpha, beta):
        maxAction = None
        maxPiece = None
        maxInsertPos = None
        if self.Cut_Off_Test(state,depth):
            return self.Eval(state), maxAction, maxPiece, maxInsertPos
        v = np.NINF
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState,pieceRemoved = state.getState(action, pieceId, insertPos)
            minValue, minAction, minPiece, minInsertPos = self.Min_Value(nextState,depth-1, alpha, beta)
            if minValue > beta:
                return minValue, action, minPiece, minInsertPos
            if minValue > v:
                maxAction, v, maxPiece, maxInsertPos = action, minValue, minPiece, minInsertPos
                alpha = max(alpha, v)
        return v, maxAction, maxPiece, maxInsertPos

    def MinValue(self, state,depth, alpha, beta):
        minAction = None
        minPiece = None
        minInsertPos = None
        if self.Cut_Off_Test(state,depth):
            return self.Eval(state), minAction, minPiece, minInsertPos
        v = np.NINF
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState, pieceRemoved = state.getState(action, pieceId, insertPos)
            maxValue, maxAction, maxPiece, maxInsertPos = self.Max_Value(nextState,depth-1, alpha, beta)
            if maxValue < alpha:
                return maxValue, action, maxPiece, maxInsertPos
            if maxValue < v:
                minAction, v, minPiece, minInsertPos = action, maxValue, maxPiece, maxInsertPos
                beta = min(beta, v)
        return v, minAction, minPiece, minInsertPos

    def Alpha_Beta_Search(self, state):
        v, action, pieceId, insertPos = self.Max_Value(state, np.NINF, np.Inf)
        return action, pieceId, insertPos

    def Max_Value(self, state, alpha, beta):
        maxAction = None
        maxPiece = None
        maxInsertPos = None
        if self.Terminal_Test(state):
            return self.Utility(state), maxAction, maxPiece, maxInsertPos
        v = np.NINF
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState,pieceRemoved = state.getState(action, pieceId, insertPos)
            minValue, minAction, minPiece, minInsertPos = self.Min_Value(nextState, alpha, beta)
            if minValue > beta:
                return minValue, action, minPiece, minInsertPos
            if minValue > v:
                maxAction, v, maxPiece, maxInsertPos = action, minValue, minPiece, minInsertPos
                alpha = max(alpha, v)
        return v, maxAction, maxPiece, maxInsertPos

    def Terminal_Test(self, state):
        return state.score[state.turn] == state.TerminalPoints

    def Utility(self, state):
        if state.score[1] == state.TerminalPoints:
            return 1
        elif state.score[0] == state.TerminalPoints:
            return -1

    def Eval(self, state):
        return

    def Cut_Off_Test(self, state, depth):
        return depth == 0 or self.Terminal_Test(state)

    def Min_Value(self, state, alpha, beta):
        minAction = None
        minPiece = None
        minInsertPos = None
        if self.Terminal_Test(state):
            return self.Utility(state), minAction, minPiece, minInsertPos
        v = np.NINF
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState, pieceRemoved = state.getState(action, pieceId, insertPos)
            maxValue, maxAction, maxPiece, maxInsertPos = self.Max_Value(nextState,alpha, beta)
            if maxValue < alpha:
                return maxValue, action, maxPiece, maxInsertPos
            if maxValue < v:
                minAction, v, minPiece, minInsertPos = action, maxValue, maxPiece, maxInsertPos
                beta = min(beta, v)
        return v, minAction, minPiece, minInsertPos
