import numpy as np
from  copy import deepcopy as deepcopy
class StateClass:

    def __init__(self, TerminalPoints):
        '''
        0: Human (goes down)
        1: AI (AI goes up)
        '''
        self.boardHori, self.boardVert = 3,4
        self.turn = 0
        self.state = np.array([[None, None, None], [None, None, None], [None, None, None], [None, None, None]])
        self.TerminalPoints = TerminalPoints
        self.pieces = {1: set(), 0: set()}


    def getState(self, action, position):
        newstate = deepcopy(self)
        if action == 'DiagonalLeft':
            if self.turn:

                newstate.pieces[newstate.turn].add((position[0]-1, position[1]-1))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))

                newstate.state[position[0]-1, position[1]-1] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 0
                self.turn = 0

            else:
                newstate.pieces[newstate.turn].add((position[0]+1, position[1]-1))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0]+1, position[1]-1] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 1
                self.turn = 1

        if action == 'DiagonalRight':
            if self.turn:
                newstate.pieces[newstate.turn].add((position[0]-1, position[1]+1))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))

                newstate.state[position[0]-1, position[1]+1] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 0
                self.turn = 0
            else:
                newstate.pieces[newstate.turn].add((position[0]+1, position[1]+1))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0]+1, position[1]+1] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 1
                self.turn = 1

        if action == 'JumpOverOne':
            if self.turn:
                newstate.pieces[newstate.turn].add((position[0] + 2,position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0] + 2,position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 0
                self.turn = 0

            else:
                newstate.pieces[newstate.turn].add((position[0] -2, position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0] -2, position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 1
                self.turn = 1

        if action == 'JumpOverTwo':
            if self.turn:
                newstate.pieces[newstate.turn].add((position[0] + 3,position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0] + 3,position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 0
                self.turn = 0
            else:
                newstate.pieces[newstate.turn].add((position[0] -3, position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0] -3, position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 1
                self.turn = 1

        if action == 'JumpOverThree':
            if self.turn:
                newstate.pieces[newstate.turn].add((position[0] + 4,position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0] + 4,position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 0
                self.turn = 0
            else:
                newstate.pieces[newstate.turn].add((position[0] -4, position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.state[position[0] -4, position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn = 1
                self.turn = 1

        if action == 'Insert':
            if self.turn:
                newstate.pieces[newstate.turn].add((position[0],position[1]))
                newstate.state[position[0],position[1]] = self.turn
                newstate.turn, self.turn = 0, 0
            else:
                newstate.pieces[newstate.turn].add((position[0], position[1]))
                newstate.state[position[0],position[1]] = self.turn
                newstate.turn, self.turn = 1,1

        if action == 'Attack':
            if self.turn:
                newstate.pieces[newstate.turn].add((position[0]-1,position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.pieces[(newstate.turn+1)%2].remove((position[0]-1,position[1]))
                newstate.state[position[0]-1,position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn, self.turn= 0, 0
            else:

                newstate.pieces[newstate.turn].add((position[0]+1, position[1]))
                newstate.pieces[newstate.turn].remove((position[0], position[1]))
                newstate.pieces[(newstate.turn+1)%2].remove((position[0]+1, position[1]))
                newstate.state[position[0]+1, position[1]] = self.turn
                newstate.state[position[0], position[1]] = None
                newstate.turn, self.turn = 1, 1

        return


class GameController(StateClass):
    def __init__(self):
        '''
        Legal
        terminal test
        evaluation function

        '''
        self.PossibleActions = ['Attack', 'Insert', 'JumpOverOne', 'JumpOverTwo', 'JumpOverThree', 'DiagonalLeft', 'DiagonalRight']

    def ACTIONS(self, StateObject):

        '''
        :param state: StateClass: StateClass object
        :return: List of actions
        '''

        PossibleActions ={'Attack': {}, 'Insert': {}, 'JumpOverOne': {}, 'JumpOverTwo': {}, 'JumpOverThree': {}, 'DiagonalLeft': {}, 'DiagonalRight': {}}
        if StateObject.turn:
            if (len(StateObject.pieces[1]) < 4) and (None in StateObject.state[3,:]):
                PossibleActions['Insert'].add(True)

            







            for piece in StateObject.pieces[1]:















