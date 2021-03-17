import numpy as np
from copy import deepcopy as deepcopy


class Piece:


    def __init__(self, id, position = None):
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
        #h_piece1, h_piece2, h_piece3, h_piece4 = Piece('H1'), Piece('H2'), Piece('H3'), Piece('H4')

        #self.HumanPieces = [Piece('H1'), Piece('H2'), Piece('H3'), Piece('H4')]
        #self.AiPieces = [Piece('A1'), Piece('A2'), Piece('A3'), Piece('A4')]
        self.pieces = {'H1': None, 'H2' : None, 'H3' : None, 'H4' : None, 'A1': None, 'A2' : None, 'A3' : None, 'A4' : None}
        #self.pieces = {1: set(), 0: set()}
        self.score = {1: 0, 0: 0}

    #Only for insert action, we use the position argument
    def getState(self, action,id, insertPosition = None):
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
                    newState.pieces[id] = [position[0] + 1, position[1] - 1]
                    newState.state[position[0] + 1, position[1] - 1] = self.turn
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
                    newState.pieces[id] = [position[0] + 1, position[1] + 1]
                    newState.state[position[0] + 1, position[1] + 1] = self.turn
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
            if self.turn:
                newState.pieces[id] = [insertPosition[0], insertPosition[1]]
                newState.state[insertPosition[0], insertPosition[1]] = self.turn
                newState.turn, self.turn = 0, 0
            else:
                newState.pieces[id] = [insertPosition[0], insertPosition[1]]
                newState.state[insertPosition[0], insertPosition[1]] = self.turn
                newState.turn, self.turn = 1, 1

        if action == 'Attack':
            if self.turn:
                newState.pieces[id] = [position[0] - 1, position[1]]
                #Get the id of the piece in front and remove its position
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
        for id,pos in self.pieces:
            if pos[0] == position[0] and pos[1] == position[1]:
                self.pieces[id] = None
                return id

    def isActionApplicable(self,action, position):
        return

    def isPositionValid(self, yPosition):
        return yPosition >= 0 and yPosition <= 2

    def printState(self):
        for i in range(0,4):
            print("|", end=" ")
            for j in range(0,3):
                if self.state[i,j] == None:
                    print(".", end=" ")
                    print("|", end=" ")
                else:
                    print(self.state[i,j], end=" ")
                    print("|", end=" ")
            print("")
