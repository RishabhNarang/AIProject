from Board import GameBoard
import tkinter as tk

from GameController import GameController
from MiniMax import MiniMax
from StateClass import StateClass

if __name__ == "__main__":
    players = {0: 'Human', 1: "AI"}
    # root = tk.Tk()
    state = StateClass(5)
    gameControl = GameController()
    # possibleActions = gameControl.ACTIONS(state)
    print(
        "The actions available are : Insert, DiagonalLeft, DiagonalRight, JumpOverOne, JumpOverTwo, JumpOverThree, Attack")
    action, pieceId = '', ''
    position = [-1, -1]
    isHumanInDeadlock = False
    isAIInDeadlock = False
    while True:
        state.printState()
        if gameControl.areNoMovesAvailable(state):
            next_state = state.changeTurnsOnlyAndGetNextState()
            print("No moves available for you Human :D")
            isHumanInDeadlock = True
            #break
        else:
            isHumanInDeadlock = False
            while True:
                #state.printState()
                action = input("Choose one action to do: ")
                pieceId = input("Enter the piece id:")

                if action == 'Insert':
                    positionY = -1
                    while not state.isPositionValid(positionY):
                        positionY = int(input("Input the column position of piece:"))
                    if state.isPiecePossibleToMove(action, pieceId, positionY):
                        next_state, pieceRemoved = state.getState(action, pieceId, positionY)
                        break
                    else:
                        print("Cannot Insert at the specified position. Piece already exists!")
                        continue
                    #break
                    # TODO change images
                    # player1_img = tk.PhotoImage(file='accept.png')
                    # board.addpiece(pieceId,player1_img,0,positionY)
                else:
                    if not state.isActionNameAndPieceIdValid(action, pieceId):
                        continue
                    if state.isPiecePossibleToMove(action, pieceId):
                        next_state, pieceRemoved = state.getState(action, pieceId)
                        break
                    else:
                        print("The piece is not possible to move with the given action. Choose another action/piece.")
                        continue
        # AI's turn now
        action = ''
        state = next_state
        if gameControl.areNoMovesAvailable(state):
            next_state = state.changeTurnsOnlyAndGetNextState()
            print("No moves available for AI ")
            isAIInDeadlock = True
        else:
            isAIInDeadlock = False
            # Run minimax algo with next_state as the initial state for the AI
            # Returns the best action found
            actionFound = ''
            AI = MiniMax()
            actionFound, pieceId, insertPos = AI.Alpha_Beta_Search(state)
            #actionFound, pieceId, insertPos = AI.alpha_beta(state,1,float('-inf'),float('inf'))
            next_state,pieceRemoved = state.getState(actionFound, pieceId, insertPos)

        # Check for deadlock of the game
        if isHumanInDeadlock and isAIInDeadlock:
            print("Game ended! No more moves available for either player..")
            break
        state = next_state
    # Repeat until someone scores Max points
