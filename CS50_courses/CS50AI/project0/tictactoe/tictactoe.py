"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Need to check how many X or O are courrently on board

    x_count = 0
    o_count = 0
    empty_count = 0

    # Reading board....
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
            elif cell == EMPTY:
                empty_count += 1

    if x_count > o_count:
        return O
    elif x_count <= o_count and empty_count > 0:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_actions.append((i, j))

    return possible_actions


# Defining a custom exception for an invalid action on the board


class InvalidAction(Exception):
    pass


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Doing a deep copy of the original board
    updated_board = copy.deepcopy(board)

    # Checking if the passed action is valid or applied on a non-empty cell
    if board[action[0]][action[1]] is not EMPTY:
        raise InvalidAction("This is not a valid action")

    # Determining which player moves
    move = player(updated_board)
    # Updating board, keeping the original
    updated_board[action[0]][action[1]] = move
    return updated_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking if there's a winner horizontally
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    # Checking if there's a winner vertically
    for col in range(3):
        column = [row[col] for row in board]
        if column.count(X) == 3:
            return X
        elif column.count(O) == 3:
            return O

    # Checking if there's a winner vertically
    diagonal = [board[i][i] for i in range(3)]
    counter_diagonal = [board[i][-i - 1] for i in range(3)]

    if diagonal.count(X) == 3 or counter_diagonal.count(X) == 3:
        return X
    elif diagonal.count(O) == 3 or counter_diagonal.count(O) == 3:
        return O

    # There's no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    count_empty = sum(row.count(EMPTY) for row in board)
    game_over = winner(board)

    # Game over because someone win the game or there are not empty cells because it's a tie
    if game_over is not None or count_empty == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    """
    if terminal(board):
        return None

    player_turn = player(board)
    possible_actions = actions(board)

    optimal_action = ()
    if player_turn == X:
        optimal_action = max(
            possible_actions,
            key=lambda action: min_value(result(board, action), -math.inf, math.inf),
        )
    else:
        optimal_action = min(
            possible_actions,
            key=lambda action: max_value(result(board, action), -math.inf, math.inf),
        )
    return optimal_action


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action), alpha, beta))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value
