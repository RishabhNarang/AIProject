import numpy as np
from copy import deepcopy as deepcopy

from GameController import GameController


class Piece:

    def __init__(self, id, position=None):
        self.id = id
        self.position = position


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
    def getState(self, action, id, insertYPosition=None):
        newState = deepcopy(self)
        position = self.pieces[id]
        pieceRemoved = None
        if action == 'DiagonalLeft':
            if self.turn:
                if position[0] - 1 == -1:
                    self.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 1, position[1] - 1]
                    newState.state[position[0] - 1, position[1] - 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0

            else:
                if position[0] + 1 == 4:
                    self.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 1, position[1] + 1]
                    newState.state[position[0] + 1, position[1] + 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'DiagonalRight':
            if self.turn:
                if position[0] - 1 == -1:
                    self.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 1, position[1] + 1]
                    newState.state[position[0] - 1, position[1] + 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0
            else:
                if position[0] + 1 == 4:
                    self.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 1, position[1] - 1]
                    newState.state[position[0] + 1, position[1] - 1] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'JumpOverOne':
            if self.turn:
                if position[0] - 2 == -1:
                    self.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 2, position[1]]
                    newState.state[position[0] - 2, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0

            else:
                if position[0] + 2 == 4:
                    self.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 2, position[1]]
                    newState.state[position[0] + 2, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'JumpOverTwo':
            if self.turn:
                if position[0] - 3 == -1:
                    self.score[1] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] - 3, position[1]]
                    newState.state[position[0] - 3, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0
            else:
                if position[0] + 3 == 4:
                    self.score[0] += 1
                    newState.pieces[id] = None
                    pieceRemoved = id
                else:
                    newState.pieces[id] = [position[0] + 3, position[1]]
                    newState.state[position[0] + 3, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'JumpOverThree':
            if self.turn:
                self.score[1] += 1
                newState.pieces[id] = None
                pieceRemoved = id
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0
            else:
                self.score[0] += 1
                newState.pieces[id] = None
                pieceRemoved = id
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'Insert':
            insertXPosition = 3 if self.turn else 0
            newState.pieces[id] = [insertXPosition, insertYPosition]
            newState.state[insertXPosition, insertYPosition] = self.turn
            if self.turn:
                newState.turn, self.turn = 0, 0
            else:
                newState.turn, self.turn = 1, 1

        if action == 'Attack':
            if self.turn:
                newState.pieces[id] = [position[0] - 1, position[1]]
                # Get the id of the piece in front and remove its position
                pieceRemoved = self.removePieceAt([position[0] - 1, position[1]])
                newState.state[position[0] - 1, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn, self.turn = 0, 0
            else:
                newState.pieces[id] = [position[0] + 1, position[1]]
                pieceRemoved = self.removePieceAt([position[0] + 1, position[1]])
                newState.state[position[0] + 1, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn, self.turn = 1, 1

        return newState, pieceRemoved

    def removePieceAt(self, position):
        for id, pos in self.pieces:
            if pos[0] == position[0] and pos[1] == position[1]:
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
        if action != 'Insert' and current_position is None:
            return False
        if action == 'DiagonalLeft':
            if self.turn:
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
            if self.turn:
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
            if self.turn:
                if current_position[0] == 0:
                    # Jump over not possible if it is just one step away from going out of board
                    return False
                elif current_position[0] == 1:
                    if self.state[current_position[0] - 1, current_position[1]] == (self.turn + 1) % 2:
                        # Front piece is other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] - 1, current_position[1]] == (self.turn + 1) % 2) and (
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
                    if self.state[current_position[0] + 1, current_position[1]] == (self.turn + 1) % 2:
                        # Front piece is other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] + 1, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] + 2, current_position[1]] is None):
                        # Front piece is other player's piece and jump over to an empty position
                        return True
                    else:
                        return False

        elif action == 'JumpOverTwo':
            if self.turn:
                if current_position[0] == 0 or current_position[0] == 1:
                    # JumpOverTwo not possible if it is just one/two steps away from going out of board
                    return False
                elif current_position[0] == 2:
                    if (self.state[current_position[0] - 1, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] - 2, current_position[1]] == (self.turn + 1) % 2):
                        # Both Front pieces are other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] - 1, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] - 2, current_position[1]] == (self.turn + 1) % 2) and (
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
                    if (self.state[current_position[0] + 1, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] + 2, current_position[1]] == (self.turn + 1) % 2):
                        # Both Front pieces are other player's piece and jump over takes you out of the board
                        return True
                    else:
                        return False
                else:
                    if (self.state[current_position[0] + 1, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] + 2, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] + 3, current_position[1]] is None):
                        # Both Front pieces are other player's piece and jump over to an empty position
                        return True
                    else:
                        return False

        elif action == 'JumpOverThree':
            if self.turn:
                if current_position[0] != 3:
                    # JumpOverThree not possible if it is not in the first row.
                    return False
                else:
                    if (self.state[current_position[0] - 1, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] - 2, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] - 3, current_position[1]] == (self.turn + 1) % 2):
                        # All Front piece are other player's pieces and jump out of the board
                        return True
                    else:
                        return False
            else:
                if current_position[0] != 0:
                    # JumpOverThree not possible if it is not in the first row.
                    return False
                else:
                    if (self.state[current_position[0] + 1, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] + 2, current_position[1]] == (self.turn + 1) % 2) and (
                            self.state[current_position[0] + 3, current_position[1]] == (self.turn + 1) % 2):
                        # All Front piece are other player's pieces and jump out of the board
                        return True
                    else:
                        return False
        elif action == 'Insert':
            if insertColPosition is None:
                return False
            if self.turn:
                return self.state[3, insertColPosition] is None
            else:
                return self.state[0, insertColPosition] is None
        elif action == 'Attack':
            if self.turn:
                if current_position[0] == 0:
                    return False
                else:
                    return self.state[current_position[0]-1, current_position[1]] == (self.turn+1) % 2
            else:
                if current_position[0] == 3:
                    return False
                else:
                    return self.state[current_position[0]+1, current_position[1]] == (self.turn + 1) % 2

    def changeTurnsOnlyAndGetNextState(self):
        newState = deepcopy(self)
        newState.turn = (self.turn + 1) % 2
        return newState

    def isPositionValid(self, yPosition):
        return yPosition >= 0 and yPosition <= 2

    def getPossibleInsertPosition(self):
        yPositions = []
        rowPos = 3 if self.turn else 0
        for i in range(0,3):
            if self.state[rowPos,i] is None:
                yPositions.append(i)
        return yPositions

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
