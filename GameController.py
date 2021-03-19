class GameController():
    def __init__(self):
        '''
        Legal
        terminal test
        evaluation function

        '''
        self.PossibleActions = ['Attack', 'Insert', 'JumpOverOne', 'JumpOverTwo', 'JumpOverThree', 'DiagonalLeft',
                                'DiagonalRight']

    def ACTIONS(self, state_object):
        """
        :param state_object: StateClass object
        :return: List of actions
        """

        #possible_actions = {'Attack': set(), 'Insert': set(), 'JumpOverOne': set(), 'JumpOverTwo': set(),
         #                   'JumpOverThree': set(),
         #                   'DiagonalLeft': set(), 'DiagonalRight': set()}
        possible_actions = []
        if state_object.turn:
            # Possible Insert actions
            for pieceId in ['A1', 'A2', 'A3', 'A4']:
                possibleInsertPos = state_object.getPossibleInsertPosition()
                if (state_object.pieces[pieceId] is None) and len(possibleInsertPos) > 0:
                    for yPos in possibleInsertPos:
                        possible_actions.append(('Insert',pieceId, yPos))
            # All actions other than Insert
            for pieceId in ['A1', 'A2', 'A3', 'A4']:
                # Check all possible actions
                if state_object.pieces[pieceId] is not None:
                    for action in self.PossibleActions:
                        if state_object.isPiecePossibleToMove(action, pieceId):
                            possible_actions.append((action,pieceId,None))
                    '''
                    next_piece_position = state_object.state[piece_position[0] - 1, piece_position[1] - 1]
                    # DiagonalLeft
                    if (next_piece_position is None) and piece_position[0] - 1 >= -1 and piece_position[1] - 1 >= -1:
                        possible_actions['DiagonalLeft'].add((piece_position[0], piece_position[1]))
    
                    # DiagonalRight
                    next_piece_position = state_object.state[piece_position[0] - 1, piece_position[1] + 1]
                    if (next_piece_position is None) and piece_position[0] - 1 >= -1 and piece_position[1] + 1 <= 4:
                        possible_actions['DiagonalRight'].add((piece_position[0], piece_position[1]))
    
                    # JumpOverOne
                    if piece_position[0] - 2 >= -1:
                        # 'next_piece is None = -1' represents out of the board
                        # 'next_piece is None' represents free square to jump over to
                        next_piece = -1 if (piece_position[0] - 2) == -1 else state_object.state[
                            piece_position[0] - 2, piece_position[1]]
                        other_piece = state_object.state[piece_position[0] - 1, piece_position[1]]
    
                        if other_piece == 0 and (next_piece == -1 or next_piece is None):
                            possible_actions['JumpOverOne'].add((piece_position[0], piece_position[1]))
    
                    # JumpOverTwo
                    if piece_position[0] - 3 >= -1:
                        # 'next_piece is None = -1' represents out of the board
                        # 'next_piece is None' represents free square to jump over to
                        next_piece = -1 if piece_position[0] - 3 == -1 else state_object.state[
                            piece_position[0] - 3, piece_position[1]]
                        other_pieces = [state_object.state[piece_position[0] - x, piece_position[1]] for x in range(1, 3)]
    
                        if other_pieces[0] == 0 and other_pieces[1] == 0 and (next_piece == -1 or next_piece is None):
                            possible_actions['JumpOverTwo'].add((piece_position[0], piece_position[1]))
    
                    # JumpOverThree
                    if piece_position[0] - 4 >= -1:
                        # 'next_piece is None = -1' represents out of the board
                        # 'next_piece is None' represents free square to jump over to
                        next_piece = -1 if piece_position[0] - 4 == -1 else state_object.state[
                            piece_position[0] - 4, piece_position[1]]
                        other_pieces = [state_object.state[piece_position[0] - x, piece_position[1]] for x in range(1, 4)]
    
                        if other_pieces[0] == 0 and other_pieces[1] == 0 and other_pieces[2] == 0 and (
                                next_piece == -1 or next_piece is None):
                            possible_actions['JumpOverThree'].add((piece_position[0], piece_position[1]))
    
                    # Attack
                    if piece_position[0] - 1 >= 0:
                        next_piece = state_object.state[piece_position[0] - 1, piece_position[1]]
                        if next_piece == 0:
                            possible_actions['Attack'].add((piece_position[0], piece_position[1]))
                            '''
        else:
            #TODO Add the same logic for human player (0)
            # Possible Insert actions
            for pieceId in ['H1', 'H2', 'H3', 'H4']:
                possibleInsertPos = state_object.getPossibleInsertPosition()
                if (state_object.pieces[pieceId] is None) and len(possibleInsertPos) > 0:
                    for yPos in possibleInsertPos:
                        possible_actions.append(('Insert', pieceId, yPos))
            # All actions other than Insert
            for pieceId in ['H1', 'H2', 'H3', 'H4']:
                # Check all possible actions
                if state_object.pieces[pieceId] is not None:
                    for action in self.PossibleActions:
                        if state_object.isPiecePossibleToMove(action, pieceId):
                            possible_actions.append((action, pieceId, None))
        return possible_actions

    def areNoMovesAvailable(self,state_object):
        return len(self.ACTIONS(state_object)) == 0
