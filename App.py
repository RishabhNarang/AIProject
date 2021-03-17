from Board import GameBoard
import tkinter as tk

from GameController import GameController
from StateClass import StateClass


if __name__ == "__main__":
    players = {0: 'Human', 1 : "AI"}
    #root = tk.Tk()
    init_state = StateClass(10)
    gameControl = GameController()
    possibleActions = gameControl.ACTIONS(init_state)
    print("The actions available are : Insert, DiagonalLeft, DiagonalRight, JumpOverOne, JumpOverTwo, JumpOverThree, Attack")
    action =''
    position = [-1,-1]
    while True:
        init_state.printState()
        #board = GameBoard(root)
       # board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        while action not in gameControl.PossibleActions or not init_state.isActionApplicable(action,position):
            action = input("Choose one action to do: ")
            pieceId = input("Enter the piece id:")

        if action == 'Insert':
            positionY = -1
            while not init_state.isPositionValid(positionY):
                positionY = int(input("Input the column position of piece:"))
            positionX = 3 if init_state.turn else 0
            next_state, pieceRemoved = init_state.getState(action,pieceId, [positionX, positionY])
            #TODO change images
            #player1_img = tk.PhotoImage(file='accept.png')
            #board.addpiece(pieceId,player1_img,0,positionY)
        else:
            #Need to check if it goes outside the board
            next_state, pieceRemoved = init_state.getState(action, pieceId)
            #piecePositionAfterAction = next_state.getPiecePosition(pieceId)
            #board.placepiece(pieceId,piecePositionAfterAction[0], piecePositionAfterAction[1])
            #if pieceRemoved is not None:
                #board.removePiece(pieceRemoved)
        action = ''
        init_state = next_state
    #Run minimax algo with next_state as the initial state for the AI
    #Returns the best action found
    action_found = ''
    root.mainloop()
    init_state = next_state.getState(action_found, position)

    #Repeat until someone scores Max points

