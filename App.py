from GameController import GameController
from MiniMax import MiniMax
from StateClass import StateClass
import sys,argparse

if __name__ == "__main__":
    #in order to start the game:
    #App.py --maxpoints <maxpoints> --maxdepth <maxdepth>
    players = {0: 'Human', 1: "AI"}
    #create a StateClass object with terminal points given as argument by the user
    parser = argparse.ArgumentParser()

    parser.add_argument('--maxPoints', help='Maximum points needed to win')
    parser.add_argument('--maxDepth', help='How deep the AI should search')
    args = parser.parse_args()
    maxPoints = int(args.maxPoints) if args.maxPoints is not None else 5
    maxDepth = int(args.maxDepth) if args.maxDepth is not None else 8
    state = StateClass(maxPoints)
    gameControl = GameController()
    # possibleActions = gameControl.ACTIONS(state)
    print(
        "--> The actions available in the game are : Insert, DiagonalLeft, DiagonalRight, JumpOverOne, JumpOverTwo, JumpOverThree, Attack")
    print(
        "--> You are given 4 pieces to use in the game: H1, H2, H3, H4. (The pieces name are case sensitive)")
    state.printState()
    action, pieceId = '', ''
    position = [-1, -1]

    winner = None
    isGameEnded = False
    while not isGameEnded:
        if gameControl.areNoMovesAvailable(state):
            # To check if the game has gone in deadlock
            #if so game is over and winner is the one who didn't cause the deadlock
            isGameEnded, winner = state.isTerminalState()
            if isGameEnded:
                break
            #if game is not over just swich turns
            next_state,pieceRemoved = state.changeTurnsOnlyAndGetNextState()
            print("No moves available for you Human :D")
        else:
            
            while True:
                isGameEnded, winner = state.isTerminalState()
                if isGameEnded:
                    break
                # choose action and the piece to act
                action = input("Choose one action to do: ")
                pieceId = input("Enter the piece id:")

                if action == 'Insert':
                    while not state.isActionNameAndPieceIdValid(action, pieceId):
                        print("The piece Id is not valid. Enter again!")
                        pieceId = input("Enter the piece id:")
                        continue
                    positionY = -1
                    while not state.isPositionValid(positionY):
                        positionY = int(input("Input the column position of piece:"))
                        if not state.isPositionValid(positionY):
                            print("Please enter one of the values: 0,1,2")
                    # If the piece can be inserted in the input position
                    if state.isPiecePossibleToMove(action, pieceId, positionY):
                        #return what is the state caused by the insertion
                        next_state, pieceRemoved = state.RESULT(action, pieceId, positionY)
                        lastMoveMadeBy = 0
                        print("Human score =  " + str(next_state.score[0]))
                        print("AI score =  " + str(next_state.score[1]))
                        print("Human turn is finished")
                        next_state.printState()
                        print("")
                        break
                    else:
                        print("Cannot Insert at the specified position. Piece already exists!")
                        continue
                else:
                    #for invalid input just re-ask the user
                    if not state.isActionNameAndPieceIdValid(action, pieceId):
                        print("The action name/ pieceId is not valid. Enter again!")
                        continue
                    #for any other action/piece combination if it is posible
                    #print the next state and the score
                    if state.isPiecePossibleToMove(action, pieceId):
                        next_state, pieceRemoved = state.RESULT(action, pieceId)
                        lastMoveMadeBy = 0
                        print("Human score =  " + str(next_state.score[0]))
                        print("AI score =  " + str(next_state.score[1]))
                        print("Human turn is finished")
                        next_state.printState()
                        print("")
                        break
                    else:
                        print("The piece is not possible to move with the given action. Choose another action/piece.")
                        continue
        # AI's turn now
        action = ''
        state = next_state #current state becomes the state that AI's action caused
        if gameControl.areNoMovesAvailable(state):
            isGameEnded, winner = state.isTerminalState()
            if isGameEnded:
                break
            next_state = state.changeTurnsOnlyAndGetNextState()
            print("No moves available for AI ")
        else:
            isGameEnded, winner = state.isTerminalState()
            if isGameEnded:
                break
            actionFound = ''
            #run the minimax algorithm with alpha-beta pruning
            AI = MiniMax()
            #get what action to perform, which piece will perform it and if it is
            #an insert position specify where to insert it
            actionFound, pieceId, insertPos = AI.Alpha_Beta_Search(state,maxDepth)
            print("Action found by AI is :("+ actionFound +","+pieceId+","+(str(insertPos) if insertPos is not None else "") +")")
            next_state,pieceRemoved = state.RESULT(actionFound, pieceId, insertPos)
            lastMoveMadeBy = 1
            print("Human score =  " + str(next_state.score[0]))
            print("AI score =  " + str(next_state.score[1]))
            print("AI turn is finished")
            next_state.printState()
            print("")
        state = next_state #current state becomes the state that AI's action caused
        # Repeat until someone scores Max points or game goes in deadlock
    winPlayer = "AI" if winner == 1 else "Human"
    print('The game has ended. Winner is: ' + winPlayer)
