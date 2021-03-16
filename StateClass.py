import numpy as np
from copy import deepcopy as deepcopy


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
        self.pieces = {1: set(), 0: set()}
        self.score = {1: 0, 0: 0}

    def getState(self, action, position):
        newState = deepcopy(self)
        # TODO: Update scores
        if action == 'DiagonalLeft':
            if self.turn:
                if position[0] - 1 == -1:
                    self.score[1] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] - 1, position[1] - 1))
                    newState.state[position[0] - 1, position[1] - 1] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0

            else:
                if position[0] + 1 == 4:
                    self.score[0] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] + 1, position[1] - 1))
                    newState.state[position[0] + 1, position[1] - 1] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'DiagonalRight':
            if self.turn:
                if position[0] - 1 == -1:
                    self.score[1] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] - 1, position[1] + 1))
                    newState.state[position[0] - 1, position[1] + 1] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0
            else:
                if position[0] + 1 == 4:
                    self.score[0] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] + 1, position[1] + 1))
                    newState.state[position[0] + 1, position[1] + 1] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'JumpOverOne':
            if self.turn:
                if position[0] - 2 == -1:
                    self.score[1] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] - 2, position[1]))
                    newState.state[position[0] - 2, position[1]] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0

            else:
                if position[0] + 2 == 4:
                    self.score[0] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] + 2, position[1]))
                    newState.state[position[0] + 2, position[1]] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'JumpOverTwo':
            if self.turn:
                if position[0] - 3 == -1:
                    self.score[1] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] - 3, position[1]))
                    newState.state[position[0] - 3, position[1]] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0
            else:
                if position[0] + 3 == 4:
                    self.score[0] += 1
                else:
                    newState.pieces[newState.turn].add((position[0] + 3, position[1]))
                    newState.state[position[0] + 3, position[1]] = self.turn
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'JumpOverThree':
            if self.turn:
                self.score[1] += 1
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 0
                self.turn = 0
            else:
                self.score[0] += 1
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.state[position[0], position[1]] = None
                newState.turn = 1
                self.turn = 1

        if action == 'Insert':
            if self.turn:
                newState.pieces[newState.turn].add((position[0], position[1]))
                newState.state[position[0], position[1]] = self.turn
                newState.turn, self.turn = 0, 0
            else:
                newState.pieces[newState.turn].add((position[0], position[1]))
                newState.state[position[0], position[1]] = self.turn
                newState.turn, self.turn = 1, 1

        if action == 'Attack':
            if self.turn:
                newState.pieces[newState.turn].add((position[0] - 1, position[1]))
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.pieces[(newState.turn + 1) % 2].remove((position[0] - 1, position[1]))
                newState.state[position[0] - 1, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn, self.turn = 0, 0
            else:

                newState.pieces[newState.turn].add((position[0] + 1, position[1]))
                newState.pieces[newState.turn].remove((position[0], position[1]))
                newState.pieces[(newState.turn + 1) % 2].remove((position[0] + 1, position[1]))
                newState.state[position[0] + 1, position[1]] = self.turn
                newState.state[position[0], position[1]] = None
                newState.turn, self.turn = 1, 1

        return
