"""
The gameController class keeps track of all possible actions and for the human and AI in the game.
"""


class GameController():
    def __init__(self):
        self.PossibleActions = ['JumpOverOne', 'JumpOverTwo', 'JumpOverThree', 'DiagonalLeft',
                                'DiagonalRight', 'Attack', 'Insert']

    # Checks possible actions and adds it to a list, and then returns the list with possible actions
    def ACTIONS(self, state_object):
        """
        :param state_object: StateClass object
        :return: List of actions
        """
        possible_actions = []
        # All actions other than "Insert"
        for pieceId in ['A1', 'A2', 'A3', 'A4'] if state_object.turn else ['H1', 'H2', 'H3', 'H4']:
            # Check all possible actions, and add to list "possible_actions"
            if state_object.isPieceOnBoard(pieceId):
                for action in self.PossibleActions:
                    if state_object.isPiecePossibleToMove(action, pieceId):
                        possible_actions.append((action, pieceId, None))
        # Check if it is possible to "Insert" for either AI or Human
        possiblePieceToInsert = state_object.getOneAiPieceNotOnBoard() if state_object.turn else state_object.getOneHumanPieceNotOnBoard()
        if possiblePieceToInsert is not None:
            possibleInsertPos = state_object.getPossibleInsertPosition()
            for yPos in possibleInsertPos:
                # Add "Insert" to list of "possible_Actions"
                possible_actions.append(('Insert', possiblePieceToInsert, yPos))
        return possible_actions

    # Checks and returns if there are any available moves for current player
    def areNoMovesAvailable(self, state_object):
        return len(self.ACTIONS(state_object)) == 0
