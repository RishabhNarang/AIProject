
class GameController():
    def __init__(self):
        self.PossibleActions = ['Attack', 'Insert', 'JumpOverOne', 'JumpOverTwo', 'JumpOverThree', 'DiagonalLeft',
                                'DiagonalRight']

    def ACTIONS(self, state_object):
        """
        :param state_object: StateClass object
        :return: List of actions
        """
        possible_actions = []
        if state_object.turn:
            # Possible Insert actions
            possiblePieceToInsert = state_object.getOneAiPieceNotOnBoard()
            if possiblePieceToInsert is not None:
                possibleInsertPos = state_object.getPossibleInsertPosition()
                for yPos in possibleInsertPos:
                    possible_actions.append(('Insert', possiblePieceToInsert, yPos))
            # All actions other than Insert
            for pieceId in ['A1', 'A2', 'A3', 'A4']:
                # Check all possible actions
                if state_object.isPieceOnBoard(pieceId):
                    for action in self.PossibleActions:
                        if state_object.isPiecePossibleToMove(action, pieceId):
                            possible_actions.append((action, pieceId, None))

        else:
            # Possible Insert actions
            possiblePieceToInsert = state_object.getOneHumanPieceNotOnBoard()
            if possiblePieceToInsert is not None:
                possibleInsertPos = state_object.getPossibleInsertPosition()
                for yPos in possibleInsertPos:
                    possible_actions.append(('Insert', possiblePieceToInsert, yPos))
            # All actions other than Insert
            for pieceId in ['H1', 'H2', 'H3', 'H4']:
                # Check all possible actions
                if state_object.isPieceOnBoard(pieceId):
                    for action in self.PossibleActions:
                        if state_object.isPiecePossibleToMove(action, pieceId):
                            possible_actions.append((action, pieceId, None))
        return possible_actions

    def areNoMovesAvailable(self, state_object):
        return len(self.ACTIONS(state_object)) == 0
