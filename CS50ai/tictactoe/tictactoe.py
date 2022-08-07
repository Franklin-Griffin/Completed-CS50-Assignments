"""
Tic Tac Toe Player
"""

import math
from multiprocessing.sharedctypes import Value

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # balance of 1 is O's turn, balance of 0 is X's turn
    balance = 0

    for y in range(3):
        for x in range(3):
            if board[y][x] == X:
                balance += 1
            elif board[y][x] == O:
                balance -= 1

    return X if balance == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    
    for y in range(3):
        for x in range(3):
            if board[y][x] == EMPTY:
                actions.append((y, x))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action == None or board[action[0]][action[1]] != EMPTY:
        # Invalid move
        raise ValueError
    
    # Deep copy
    copyboard = [[None, None, None], [None, None, None], [None, None, None]]
    for y in range(3):
        for x in range(3):
            copyboard[y][x] = board[y][x]

    copyboard[
        action[0]][action[1]] = player(board)
    
    return copyboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal
    for y in range(3):
        # represents the number, positive or negative, of X/O in the row
        streak = 0
        for x in range(3):
            if board[y][x] == X:
                streak += 1
            elif board[y][x] == O:
                streak -= 1
        if streak == 3:
            return X
        elif streak == -3:
            return O

    # Vertical
    for x in range(3):
        # represents the number, positive or negative, of X/O in the column
        streak = 0
        for y in range(3):
            if board[y][x] == X:
                streak += 1
            elif board[y][x] == O:
                streak -= 1
        if streak == 3:
            return X
        elif streak == -3:
            return O

    # Diagonal
    streak = 0
    for z in range(3):
        if board[z][z] == X:
            streak += 1
        elif board[z][z] == O:
            streak -= 1
    if streak == 3:
        return X
    elif streak == -3:
        return O

    # Diagonal other way 
    streak = 0
    for z in range(3):
        if board[-z-1][z] == X:
            streak += 1
        elif board[z-1][-z] == O:
            streak -= 1
    if streak == 3:
        return X
    elif streak == -3:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    # Check if board is full
    for y in range(3):
        for x in range(3):
            if board[y][x] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    util = winner(board)
    return 1 if util == X else (-1 if util == O else 0)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        # max player
        bestAction = None
        bestV = -2
        for a in actions(board):
            v = MinValue(result(board, a), bestV)
            if v > bestV:
                bestV = v
                bestAction = a
        return bestAction

    else:
        # min player
        bestAction = None
        bestV = 2
        for a in actions(board):
            v = MaxValue(result(board, a), bestV)
            if v < bestV:
                bestV = v
                bestAction = a
        return bestAction


def MaxValue(board, prune):
    if terminal(board):
        return utility(board)
        
    v = -1
    for action in actions(board):
        v = max(v, MinValue(result(board, action), v))
        if v >= prune:
            return v
    return v


def MinValue(board, prune):
    if terminal(board):
        return utility(board)

    v = 1
    for action in actions(board):
        v = min(v, MaxValue(result(board, action), v))
        if v <= prune:
            return v
    return v