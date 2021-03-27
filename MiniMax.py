from GameController import GameController
from StateClass import StateClass


class MiniMax:

    def __init__(self):
        '''
        Class to perform the minimax algorithm with alpha beta prunning
        '''

    def Alpha_Beta_Search(self, state,maxDepth = 8, gameControl=GameController(), alpha=float('-inf'), beta=float('inf')):
        """
        :param state: Instance of the StateClass
        :param gemeControl: Instance of the GameController class
        :param best_val: Initial values of optimal evaluation value
        :param beta: Initial value

        :return: resultingAction: Optimal action found by algorithm
                 resultingPiece: Piece id of the piece that shall perform the action
                 resultingInsertPos: If action is insert it returns column number of the inserted position,
                                     otherwise None

        """

        resultingAction, resultingPiece, resultingInsertPos = None, None, None
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            child_node, piece_removed = state.RESULT(action, pieceId, insertPos)
            value = self.Min_Value(child_node, maxDepth, alpha, beta)
            print("The action " + str(action) + " gives us eval value = " + str(value) + "after executing action.")

            if value > alpha:
                alpha = value
                resultingAction, resultingPiece, resultingInsertPos = action, pieceId, insertPos

        return resultingAction, resultingPiece, resultingInsertPos

    def Max_Value(self, state, depth, alpha, beta):

        """
        :param state: Instance of the StateClass
        :param depth: Current depth of minimax tree
        :param alpha: Current value of alpha
        :param beta: Current value of beta
        :return: Max value of all childrens evaluations value

        """

        # Checks if a terminal state is reached or max depth is reached
        if self.Cut_Off_Test(state, depth):
            return self.Eval(state)

        # Initialise
        maxVal = float('-inf')
        gameControl = GameController()
        noMovesAvailable = True

        # Find evaluation value of each child node
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            noMovesAvailable = False
            nextState, pieceRemoved = state.RESULT(action, pieceId, insertPos)
            value = self.Min_Value(nextState, depth - 1, alpha, beta)
            maxVal = max(maxVal, value)
            alpha = max(alpha, value)

            # Check if tree shall be pruned at current branch
            if beta < alpha:
                break

        # If no moves are available, parent and child node is identical and evaluation value from
        # the only child will be passed up
        if noMovesAvailable:
            nextState, pieceRemoved = state.changeTurnsOnlyAndGetNextState()
            value = self.Min_Value(nextState, depth - 1, alpha, beta)
            maxVal = max(maxVal, value)

        return maxVal

    def Min_Value(self, state, depth, alpha, beta):

        """
        :param state: Instance of the StateClass
        :param depth: Current depth of minimax tree
        :param alpha: Current value of alpha
        :param beta: Current value of beta
        :return: Min value of all childrens evaluations value

        """
        # Checks if a terminal state is reached or max depth is reached
        if self.Cut_Off_Test(state, depth):
            return self.Eval(state)

        # Initialise
        minVal = float('inf')
        gameControl = GameController()
        noMovesAvailable = True

        # Find evaluation value of each child node
        for (action, pieceId, insertPos) in gameControl.ACTIONS(state):
            noMovesAvailable = False
            nextState, pieceRemoved = state.RESULT(action, pieceId, insertPos)
            value = self.Max_Value(nextState, depth - 1, alpha, beta)
            minVal = min(minVal, value)
            beta = min(beta, value)

            # Check if tree shall be pruned at current branch
            if beta <= alpha:
                break

        # If no moves are available, parent and child node is identical and evaluation value from
        # the only child will be passed up
        if noMovesAvailable:
            nextState, pieceRemoved = state.changeTurnsOnlyAndGetNextState()
            value = self.Max_Value(nextState, depth - 1, alpha, beta)
            minVal = min(minVal, value)
        return minVal


    def Terminal_Test(self, state: StateClass):
        """
        :param state: Instance of the StateClass
        :return: True/False, winner
        """
        isTerminalState, winner = state.isTerminalState()
        return isTerminalState, winner

    def Eval(self, state: StateClass):
        """
        :param state: Instance of the StateClass
        :return: Value of linear evaluation function:
                 sum(weight_ai_i * feature_ai_i) - sum(weight_human_i * feature_human_i)
        """

        # Increase/decrease evaluation function with 1000 if the state is a winning state
        isTerminalState, winner = self.Terminal_Test(state)

        #Increase if AI is winner
        if isTerminalState and winner == 1:
            return 1000

        # Increase if human is winner
        elif isTerminalState and winner == 0:
            return -1000
        eval_val_ai, eval_val_human = 0, 0

        # Increase evaluation function if AI gains a point
        eval_val_ai += state.score[1] * 100

        # Decrease evaluation function if human gains a point
        eval_val_human += state.score[0] * 100

        # Increase evaluation function if AI is one step away from scoring point
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

        # Decreases evaluation function if human is one step away from scoring point
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

        # Increase evaluation value if attack will be possible from the child node
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

        # Decrease evaluation function according to row idx.
        for piece in ['A1', 'A2', 'A3', 'A4']:
            piece_position = state.pieces[piece]
            if piece_position is not None and (
                    state.isPiecePossibleToMove('DiagonalLeft', piece) or state.isPiecePossibleToMove('DiagonalRight',
                                                                                                      piece)):
                #If piece is two moves from achieving a point
                if piece_position[0] == 1:
                    eval_val_ai += 5
                    continue

                # If piece is three moves from achieving a point
                elif piece_position[0] == 2:
                    eval_val_ai += 3
                    continue

                # If piece is four moves from achieving a point
                elif piece_position[0] == 3:
                    eval_val_ai += 1
                    continue

        # Decrease evaluation function according to row idx.
        for piece in ['H1', 'H2', 'H3', 'H4']:
            piece_position = state.pieces[piece]
            if piece_position is not None and (
                    state.isPiecePossibleToMove('DiagonalLeft', piece) or state.isPiecePossibleToMove('DiagonalRight',
                                                                                                      piece)):
                # If piece is two moves from achieving a point
                if piece_position[0] == 2:
                    eval_val_human += 5
                    continue

                # If piece is three moves from achieving a point
                elif piece_position[0] == 1:
                    eval_val_human += 3
                    continue

                # If piece is four moves from achieving a point
                elif piece_position[0] == 0:
                    eval_val_human += 1
                    continue

        return eval_val_ai - eval_val_human

    def Cut_Off_Test(self, state, depth):
        """
        :param state: Instance of the StateClass class
        :param depth: Current depth
        :return: True if evaluation value is passed up to the root or the state is terminal
        """
        isTerminalState, winner = self.Terminal_Test(state)
        return depth == 0 or isTerminalState
