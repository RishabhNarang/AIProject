import numpy as np
from copy import deepcopy as deepcopy

from GameController import GameController


class Piece:

    def __init__(self, id, position=None):
        self.id = id
        self.position = position


def isHumanPiece(pieceId):
    if pieceId in ['H1','H2', 'H3','H4']:
        return True
    return False


class StateClass:

    def __init__(self, TerminalPoints):
        '''
        0: Human (goes down)
        1: AI (AI goes up)
        '''
        self.boardHori, self.boardVert = 3, 4
        self.turn = 0
        self.state = np.array([[None, None, None], [None, None, None], [None, None, None], [None, None, None]])
        self.TerminalPoints = TerminalPoints
        self.pieces = {'H1': None, 'H2': None, 'H3': None, 'H4': None, 'A1': None, 'A2': None, 'A3': None, 'A4': None}
        self.score = {1: 0, 0: 0}

    # Only for insert action, we use the position argument
    def RESULT(self, action, id, insertYPosition=None):
        newState = deepcopy(self)
        position = self.pieces[id]
        pieceRemoved = None
        if action == 'DiagonalLeft':
            if self.turn:
                if position[0] - 1 == -1:
                    newState.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 1, position[1] - 1]
                    newState.state[position[0] - 1, position[1] - 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0

            else:
                if position[0] + 1 == 4:
                    newState.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 1, position[1] + 1]
                    newState.state[position[0] + 1, position[1] + 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1

        if action == 'DiagonalRight':
            if self.turn:
                if position[0] - 1 == -1:
                    newState.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 1, position[1] + 1]
                    newState.state[position[0] - 1, position[1] + 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0
            else:
                if position[0] + 1 == 4:
                    newState.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 1, position[1] - 1]
                    newState.state[position[0] + 1, position[1] - 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1

        if action == 'JumpOverOne':
            if self.turn:
                if position[0] - 2 == -1:
                    newState.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 2, position[1]]
                    newState.state[position[0] - 2, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0

            else:
                if position[0] + 2 == 4:
                    newState.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 2, position[1]]
                    newState.state[position[0] + 2, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1

        if action == 'JumpOverTwo':
            if self.turn:
                if position[0] - 3 == -1:
                    newState.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 3, position[1]]
                    newState.state[position[0] - 3, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0
            else:
                if position[0] + 3 == 4:
                    newState.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 3, position[1]]
                    newState.state[position[0] + 3, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1

        if action == 'JumpOverThree':
            if self.turn:
                newState.score[1] += 1
                newState.pieces[id] = None
                pieceRemoved = id
                newState.state[position[0], position[1]] = None
                newState.turn = 0
            else:
                newState.score[0] += 1
                newState.pieces[id] = None
                pieceRemoved = id
                newState.state[position[0], position[1]] = None
                newState.turn = 1

        if action == 'Insert':
            insertXPosition = 3 if self.turn else 0
            newState.pieces[id] = [insertXPosition, insertYPosition]
            newState.state[insertXPosition, insertYPosition] = self.turn
            if self.turn:
                newState.turn = 0
            else:
                newState.turn = 1

        if action == 'Attack':
            if self.turn:
                # Get the id of the piece in front and remove its position
                pieceRemoved = newState.removePieceAt([position[0] - 1, position[1]])
                newState.pieces[id] = [position[0] - 1, position[1]]
                newState.state[position[0] - 1, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0
            else:
                pieceRemoved = newState.removePieceAt([position[0] + 1, position[1]])
                newState.pieces[id] = [position[0] + 1, position[1]]
                newState.state[position[0] + 1, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1

        return newState, pieceRemoved

    def removePieceAt(self, position):
        for id, pos in self.pieces.items():
            if pos is not None and pos[0] == position[0] and pos[1] == position[1]:
                self.pieces[id] = None
                return id

    def isActionNameAndPieceIdValid(self, action, pieceId):
        gameControl = GameController()
        if action not in gameControl.PossibleActions:
            return False
        if pieceId not in self.pieces.keys():
            return False
        return True

    def isPiecePossibleToMove(self, action, pieceId, insertColPosition=None):
        current_position = self.pieces[pieceId]
        isAIPiece = not isHumanPiece(pieceId)
        # Boundary cases
        ## If piece is not on board and actions other than insert can't be performed
        if action != 'Insert' and current_position is None:
            return False

        ## If piece is already on board and insert action is called
        if action == 'Insert' and current_position is not None:
            return False

        if action == 'DiagonalLeft':
            if isAIPiece:
                # Piece can always go out of board if it is one step away from going out of board
                if current_position[0] - 1 == -1:
                    return True
                else:
                    if current_position[1] - 1 < 0:
                        # If piece is in the leftmost column(from the perspective of the player), then it can't go any
                        # further left
                        return False
                    if self.state[current_position[0] - 1, current_position[1] - 1] is not None:
                        # Cant move if the diagonal left position is not empty
                        return False
                    else:
                        # The diagonal left position is empty
                        return True
            else:
                # Piece can always go out of board if it is one step away from going out of board
                if current_position[0] + 1 == 4:
                    return True
                else:
                    if current_position[1] + 1 > 2:
                        # If piece is in the leftmost column(from the perspective of the player), then it can't go any
                        # further left
                        return False
                    if self.state[current_position[0] + 1, current_position[1] + 1] is not None:
                        # Cant move if the diagonal left position is not empty
                        return False
                    else:
                        # The diagonal left position is empty
                        return True

        elif action == 'DiagonalRight':
            if isAIPiece:
                # Piece can always go out of board if it is one step away from going out of board
                if current_position[0] - 1 == -1:
                    return True
                else:
                    if current_position[1] + 1 > 2:
                        # If piece is in the rightmost column(from the perspective of the player), then it can't go any
                        # further right
                        return False
                    if self.state[current_position[0] - 1, current_position[1] + 1] is not None:
                        # Cant move if the diagonal right position is not empty
                        return False
                    else:
                        # The diagonal right position is empty
                        return True
            else:
                # Piece can always go out of board if it is one step away from going out of board
                if current_position[0] + 1 == 4:
                    return True
                else:
                    if current_position[1] - 1 < 0:
                        # If piece is in the rightmost column(from the perspective of the player), then it can't go any
                        # further right
                        return False
                    if self.state[current_position[0] + 1, current_position[1] - 1] is not None:
                        # Cant move if the diagonal right position is not empty
                        return False
                    else:
                        # The diagonal right position is empty
                        return True

        elif action == 'JumpOverOne':
            if isAIPiece:
                if current_position[0] == 0:
                    # Jump over not possible if it is just one step away from going out of board
                    return False
                elif current_position[0] == 1:
                    if self.state[current_position[0] - 1, current_position[1]] == 0:
                        # Front piece is other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] - 1, current_position[1]] == 0) and (
                            self.state[current_position[0] - 2, current_position[1]] is None):
                        # Front piece is other player's piece and jump over to an empty position
                        return True
                    else:
                        return False
            else:
                if current_position[0] == 3:
                    # Jump over not possible if it is just one step away from going out of board
                    return False
                elif current_position[0] == 2:
                    if self.state[current_position[0] + 1, current_position[1]] == 1:
                        # Front piece is other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] + 1, current_position[1]] == 1) and (
                            self.state[current_position[0] + 2, current_position[1]] is None):
                        # Front piece is other player's piece and jump over to an empty position
                        return True
                    else:
                        return False

        elif action == 'JumpOverTwo':
            if isAIPiece:
                if current_position[0] == 0 or current_position[0] == 1:
                    # JumpOverTwo not possible if it is just one/two steps away from going out of board
                    return False
                elif current_position[0] == 2:
                    if (self.state[current_position[0] - 1, current_position[1]] == 0) and (
                            self.state[current_position[0] - 2, current_position[1]] == 0):
                        # Both Front pieces are other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] - 1, current_position[1]] == 0) and (
                            self.state[current_position[0] - 2, current_position[1]] == 0) and (
                            self.state[current_position[0] - 3, current_position[1]] is None):
                        # Both Front piece are other player's piece and jump over to an empty position
                        return True
                    else:
                        return False
            else:
                if current_position[0] == 2 or current_position[0] == 3:
                    # JumpOverTwo not possible if it is just one/two steps away from going out of board
                    return False
                elif current_position[0] == 1:
                    if (self.state[current_position[0] + 1, current_position[1]] == 1) and (
                            self.state[current_position[0] + 2, current_position[1]] == 1):
                        # Both Front pieces are other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] + 1, current_position[1]] == 1) and (
                            self.state[current_position[0] + 2, current_position[1]] == 1) and (
                            self.state[current_position[0] + 3, current_position[1]] is None):
                        # Both Front pieces are other player's piece and jump over to an empty position
                        return True
                    else:
                        return False

        elif action == 'JumpOverThree':
            if isAIPiece:
                if current_position[0] != 3:
                    # JumpOverThree not possible if it is not in the first row.
                    return False
                else:
                    if (self.state[current_position[0] - 1, current_position[1]] == 0) and (
                            self.state[current_position[0] - 2, current_position[1]] == 0) and (
                            self.state[current_position[0] - 3, current_position[1]] == 0):
                        # All Front piece are other player's pieces and jump out of the board
                        return True
                    else:
                        return False
            else:
                if current_position[0] != 0:
                    # JumpOverThree not possible if it is not in the first row.
                    return False
                else:
                    if (self.state[current_position[0] + 1, current_position[1]] == 1) and (
                            self.state[current_position[0] + 2, current_position[1]] == 1) and (
                            self.state[current_position[0] + 3, current_position[1]] == 1):
                        # All Front piece are other player's pieces and jump out of the board
                        return True
                    else:
                        return False
        elif action == 'Insert':
            if insertColPosition is None:
                return False
            if isAIPiece:
                return self.state[3, insertColPosition] is None
            else:
                return self.state[0, insertColPosition] is None
        elif action == 'Attack':
            if isAIPiece:
                if current_position[0] == 0:
                    return False
                else:
                    return self.state[current_position[0]-1, current_position[1]] == 0
            else:
                if current_position[0] == 3:
                    return False
                else:
                    return self.state[current_position[0]+1, current_position[1]] == 1

    def changeTurnsOnlyAndGetNextState(self):
        newState = deepcopy(self)
        newState.turn = (self.turn + 1) % 2
        return newState, None

    def isPositionValid(self, yPosition):
        return yPosition >= 0 and yPosition <= 2

    def isPieceOnBoard(self, pieceId):
        return self.pieces[pieceId] is not None

    def getPossibleInsertPosition(self):
        yPositions = []
        rowPos = 3 if self.turn else 0
        for i in range(0,3):
            if self.state[rowPos,i] is None:
                yPositions.append(i)
        return yPositions

    def isLockedState(self):
        gameControl = GameController()
        nextState, pieceRemoved = self.changeTurnsOnlyAndGetNextState()
        if gameControl.areNoMovesAvailable(self) and gameControl.areNoMovesAvailable(nextState):
            return True, (self.turn + 1) % 2
        return False, None

    def isTerminalState(self):
        isGameLocked, loser = self.isLockedState()
        if isGameLocked:
            return True, (loser + 1) % 2
        elif self.score[0] == self.TerminalPoints:
            return True, 0
        elif self.score[1] == self.TerminalPoints:
            return True, 1
        else:
            return False, None

    def printState(self):
        for i in range(0, 4):
            print("|", end=" ")
            for j in range(0, 3):
                if self.state[i, j] == None:
                    print(".", end=" ")
                    print("|", end=" ")
                else:
                    print(self.state[i, j], end=" ")
                    print("|", end=" ")
            print("")