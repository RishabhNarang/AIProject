import numpy as np
from copy import deepcopy as deepcopy

from GameController import GameController

def isHumanPiece(pieceId):
    """
    Checks if the 'pieceId' is human piece or not
    :param pieceId: id of the piece
    :return: True if it is a human piece. False otherwise.
    """
    if pieceId in ['H1', 'H2', 'H3', 'H4']:
        return True
    return False


class StateClass:

    def __init__(self, TerminalPoints):
        '''
        0: Human (goes down)
        1: AI (AI goes up)
        '''

        # Size of the board
        self.boardHori, self.boardVert = 3, 4
        # Stores the turn of the player
        self.turn = 0
        # Stores how the board looks like
        self.state = np.array([[None, None, None], [None, None, None], [None, None, None], [None, None, None]])
        # Max points to achieve in the game
        self.TerminalPoints = TerminalPoints
        # Stores the positions of the pieces. Piece is not on board if the value is None
        self.pieces = {'H1': None, 'H2': None, 'H3': None, 'H4': None, 'A1': None, 'A2': None, 'A3': None, 'A4': None}
        # Stores the score of each player
        self.score = {1: 0, 0: 0}

    #
    def getOneHumanPieceNotOnBoard(self):
        '''
        :return: Returns either any piece id of human player which is not present on the board or returns None if all
        human pieces are on the board
        '''
        for pieceId in ['H1', 'H2', 'H3', 'H4']:
            if not self.isPieceOnBoard(pieceId):
                return pieceId
        return None

    def getOneAiPieceNotOnBoard(self):
        '''

        :return: Returns either any piece id of AI player which is not present on the board or returns None if all
        AI pieces are on the board
        '''
        for pieceId in ['A1', 'A2', 'A3', 'A4']:
            if not self.isPieceOnBoard(pieceId):
                return pieceId
        return None

    # Only for insert action, we use the position argument
    def RESULT(self, action, id, insertYPosition=None):
        """
        :param action: action to do in the current state
        :param id: id of the piece to perform the action on
        :param insertYPosition: If action is insert, then insert the piece on insertYPosition
        :return: the new state after performing 'action' on piece 'id' and id of the piece if it was removed from the
                board
        """
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
        """
        Remove a piece from the board present at location 'position'. This method should be called only when we are sure
        there is a piece present at location 'position'
        :param position: location of the piece to be removed
        :return: id of the piece which was removed from the location 'position'
        """
        for id, pos in self.pieces.items():
            if pos is not None and pos[0] == position[0] and pos[1] == position[1]:
                self.pieces[id] = None
                return id

    def isActionNameAndPieceIdValid(self, action, pieceId):
        """
        Check if action name and piece id are valid
        :param action: name of the action to be validated
        :param pieceId: id of the piece to be validated
        :return: True if validation succeeded. Otherwise False.
        """
        gameControl = GameController()
        if action not in gameControl.PossibleActions:
            return False
        if pieceId not in self.pieces.keys():
            return False
        return True

    def isPiecePossibleToMove(self, action, pieceId, insertColPosition=None):
        """
        Check if the 'action' can be performed on the piece 'pieceId' in the current state. 'insertColPosition' is
        required if the action is INSERT.
        :param action: name of the action to be performed
        :param pieceId: id of the piece to perform the action on.
        :param insertColPosition: location to insert the piece with id 'pieceId'
        :return: True if action can be performed. Otherwise, False.
        """
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
                    return self.state[current_position[0] - 1, current_position[1]] == 0
            else:
                if current_position[0] == 3:
                    return False
                else:
                    return self.state[current_position[0] + 1, current_position[1]] == 1

    def changeTurnsOnlyAndGetNextState(self):
        """
        Change the turn and return the next state. This method is used when one of the players have no moves
        available, so the turn is just passed on to the next player.
        :return: the next state with turn changed to next player.
        """
        newState = deepcopy(self)
        newState.turn = (self.turn + 1) % 2
        return newState, None

    def isPositionValid(self, yPosition):
        """
        Check if the position to insert entered by human is within the possible range of insertion.
        :param yPosition:
        :return:
        """
        return yPosition >= 0 and yPosition <= 2

    def isPieceOnBoard(self, pieceId):
        """
        Checks if a piece with id 'pieceId' is present on the board
        :param pieceId: id of the piece
        :return: True if piece is on the board. Otherwise, False.
        """
        return self.pieces[pieceId] is not None

    def getPossibleInsertPosition(self):
        """
        Return a list of column positions available to insert a piece for the current player.
        :return: a list of possible insert column positions
        """
        yPositions = []
        rowPos = 3 if self.turn else 0
        for i in range(0, 3):
            if self.state[rowPos, i] is None:
                yPositions.append(i)
        return yPositions

    def isLockedState(self):
        """
        Check if the game is in deadlock
        :return: True if the game is locked. False otherwise.
        """
        gameControl = GameController()
        nextState, pieceRemoved = self.changeTurnsOnlyAndGetNextState()
        # If no moves in current state and no moves in the next turn as well
        if gameControl.areNoMovesAvailable(self) and gameControl.areNoMovesAvailable(nextState):
            return True, (self.turn + 1) % 2
        return False, None

    def isTerminalState(self):
        """
        Check if the state is terminal or not (if the game has ended in this state)
        :return: True if state is terminal. False otherwise
        """
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
        """
        Just print the board.
        :return: Nothing
        """
        for i in range(0, 4):
            print("|", end=" ")
            for j in range(0, 3):
                if self.state[i, j] == None:
                    print("..", end=" ")
                    print("|", end=" ")
                else:
                    for piece in self.pieces.keys():
                        positionPiece = self.pieces[piece]
                        if positionPiece is not None and positionPiece[0] == i and positionPiece[1] == j:
                            print(piece, end=" ")
                            print("|", end=" ")
                            break
            print("")
