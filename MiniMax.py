import numpy as np

from GameController import GameController
from StateClass import StateClass


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

    def MaxValue(self, state, depth, alpha, beta):
        maxAction = None
        maxPiece = None
        maxInsertPos = None

        v = float('-inf')
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState,pieceRemoved = state.RESULT(action, pieceId, insertPos)
            minValue, minAction, minPiece, minInsertPos = self.MinValue(nextState,depth-1, alpha, beta)
            if minValue > beta:
                return minValue, action, minPiece, minInsertPos
            if minValue > v:
                maxAction, v, maxPiece, maxInsertPos = action, minValue, minPiece, minInsertPos
                alpha = max(alpha, v)
        return v, maxAction, maxPiece, maxInsertPos

    def MinValue(self, state, depth, alpha, beta):
        minAction = None
        minPiece = None
        minInsertPos = None
        v = float('inf')
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState, pieceRemoved = state.RESULT(action, pieceId, insertPos)
            maxValue, maxAction, maxPiece, maxInsertPos = self.MaxValue(nextState,depth-1, alpha, beta)
            if maxValue < alpha:
                return maxValue, action, maxPiece, maxInsertPos
            if maxValue < v:
                minAction, v, minPiece, minInsertPos = action, maxValue, maxPiece, maxInsertPos
                beta = min(beta, v)
        return v, minAction, minPiece, minInsertPos

    def Alpha_Beta_Search(self, state):
        gameControl = GameController()
        best_val = float('-inf')
        beta = float('inf')
        resultingAction, resultingPiece, resultingInsertPos = None, None, None
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            child_node, piece_removed = state.RESULT(action, pieceId, insertPos)
            value = self.Min_Value(child_node, 0, best_val, beta)
            if value > best_val:
                best_val = value
                resultingAction, resultingPiece, resultingInsertPos = action, pieceId, insertPos

        return resultingAction, resultingPiece, resultingInsertPos

    def Max_Value(self, state, depth, alpha, beta):
        if self.Cut_Off_Test(state, depth):
            return self.Eval(state)
        v = float('-inf')
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState, pieceRemoved = state.RESULT(action, pieceId, insertPos)
            value = self.Min_Value(nextState, depth - 1, alpha, beta)
            if value > beta:
                return value
            alpha = max(alpha, v)
        return value

    def Min_Value(self, state, depth, alpha, beta):
        if self.Cut_Off_Test(state, depth):
            return self.Eval(state)
        value = float('inf')
        gameControl = GameController()
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            nextState, pieceRemoved = state.RESULT(action, pieceId, insertPos)
            value = self.Max_Value(nextState, depth - 1, alpha, beta)
            if value < alpha:
                return value
            beta = min(beta, value)
        return value


    def Terminal_Test(self, state):
        return state.score[state.turn] == state.TerminalPoints

    def Utility(self, state):
        if state.score[1] == state.TerminalPoints:
            return 1
        elif state.score[0] == state.TerminalPoints:
            return -1

    def Eval(self, state: StateClass):
        eval_val_ai, eval_val_human = 0, 0
        # AI
        eval_val_ai += state.score[1] * 100
        eval_val_human += state.score[0] * 100
        ## one step awy from scoring a point
        for piece in ['A1', 'A2', 'A3', 'A4']:
            piece_position = state.pieces[piece]
            if piece_position is not None:
                if piece_position[0] == 0:
                    eval_val_ai += 50
                    continue
                elif state.turn == 1 and piece_position[0] == 1:
                    if state.isPiecePossibleToMove('JumpOverOne', piece):
                        eval_val_ai += 50
                        continue
                elif state.turn == 1 and piece_position[0] == 2:
                    if state.isPiecePossibleToMove('JumpOverTwo', piece):
                        eval_val_ai += 50
                        continue
                elif state.turn == 1 and piece_position[0] == 3:
                    if state.isPiecePossibleToMove('JumpOverThree', piece):
                        eval_val_ai += 50
                        continue

        for piece in ['H1', 'H2', 'H3', 'H4']:
            piece_position = state.pieces[piece]
            if piece_position is not None:
                if piece_position[0] == 3:
                    eval_val_human += 50
                    continue
                elif state.turn == 0 and piece_position[0] == 2:
                    if state.isPiecePossibleToMove('JumpOverOne', piece):
                        eval_val_human += 50
                        continue
                elif state.turn == 0 and piece_position[0] == 1:
                    if state.isPiecePossibleToMove('JumpOverTwo', piece):
                        eval_val_human += 50
                        continue
                elif state.turn == 0 and piece_position[0] == 0:
                    if state.isPiecePossibleToMove('JumpOverThree', piece):
                        eval_val_human += 50
                        continue
        ## Attack
        if state.turn:
            for piece in ['A1', 'A2', 'A3', 'A4']:
                if state.isPiecePossibleToMove('Attack', piece):
                    eval_val_ai += 20
                    # we break here because only 1 attack is possible in the turn
                    break
        else:
            for piece in ['H1', 'H2', 'H3', 'H4']:
                if state.isPiecePossibleToMove('Attack', piece):
                    eval_val_human += 20
                    # we break here because only 1 attack is possible in the turn
                    break

        ## How far pieces are from scoring a point
        for piece in ['A1', 'A2', 'A3', 'A4']:
            piece_position = state.pieces[piece]
            if piece_position is not None and (
                    state.isPiecePossibleToMove('DiagonalLeft', piece) or state.isPiecePossibleToMove('DiagonalRight',
                                                                                                      piece)):
                if piece_position[0] == 1:
                    eval_val_ai += 5
                    continue
                elif piece_position[0] == 2:
                    eval_val_ai += 3
                    continue
                elif piece_position[0] == 3:
                    eval_val_ai += 1
                    continue

        for piece in ['H1', 'H2', 'H3', 'H4']:
            piece_position = state.pieces[piece]
            if piece_position is not None and (
                    state.isPiecePossibleToMove('DiagonalLeft', piece) or state.isPiecePossibleToMove('DiagonalRight',
                                                                                                      piece)):
                if piece_position[0] == 2:
                    eval_val_human += 5
                    continue
                elif piece_position[0] == 1:
                    eval_val_human += 3
                    continue
                elif piece_position[0] == 0:
                    eval_val_human += 1
                    continue
        return eval_val_ai - eval_val_human

    def Cut_Off_Test(self, state, depth):
        return depth == 0 or self.Terminal_Test(state)
