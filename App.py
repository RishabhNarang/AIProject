from Board import GameBoard
import tkinter as tk

from GameController import GameController
from StateClass import StateClass



if __name__ == "__main__":
    players = {0: 'Human', 1 : "AI"}
    root = tk.Tk()
    board = GameBoard(root)
    init_state = StateClass(10)
    gameControl = GameController()
    possibleActions = gameControl.ACTIONS(init_state)
    print("The actions available are : Insert, DiagonalLeft, DiagonalRight, JumpOverOne, JumpOverTwo, JumpOverThree, Attack")
    action =''
    position = [-1,-1]
    while action not in gameControl.PossibleActions or not gameControl.isActionApplicable(action,position):
        action = input("Choose one action to do: ")
        position = input("Input the position of piece:")
    next_state = init_state.getState(action,position)
    if action == 'Insert':
        #board.addpiece(players[])
    else:

    #Run minimax algo with next_state as the initial state for the AI
    #Returns the best action found
    action_found = ''

    init_state = next_state.getState(action_found, position)

    #Repeat until someone scores Max points

