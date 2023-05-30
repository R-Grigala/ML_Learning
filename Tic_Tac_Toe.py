# Alpha-beta-pruning
# Alpha-beta pruning is a modified version of the minimax algorithm. It is an optimization technique for the minimax algorithm. As we have seen in the minimax search algorithm that the number of game states it has to examine are exponential in depth of the tree. Since we cannot eliminate the exponent, but we can cut it to half. Hence there is a technique by which without checking each node of the game tree we can compute the correct minimax decision, and this technique is called pruning. This involves two threshold parameter Alpha and beta for future expansion, so it is called alpha-beta pruning. It is also called as Alpha-Beta Algorithm. Alpha-beta pruning can be applied at any depth of a tree, and sometimes it not only prunes the tree leaves but also entire sub-tree. The two-parameter can be defined as:

# Alpha: The best (highest-value) choice we have found so far at any point along the path of Maximizer. The initial value of alpha is -∞.
# Beta: The best (lowest-value) choice we have found so far at any point along the path of Minimizer. The initial value of beta is +∞. The Alpha-beta pruning to a standard minimax algorithm returns the same move as the standard algorithm does, but it removes all the nodes which are not really affecting the final decision but making algorithm slow. Hence by pruning these nodes, it makes the algorithm fast.
# Algorithm:
# First, generate the entire game tree starting with the current position of the game all the way up to the terminal states.
# Apply the utility function to get the utility values for all the terminal states.
# Determine the utilities of the higher nodes with the help of the utilities of the terminal nodes. For instance, in the diagram below, we have the utilities for the terminal states written in the squares.
# Calculate the utility values with the help of leaves considering one layer at a time until the root of the tree.
# Eventually, all the backed-up values reach to the root of the tree, i.e., the topmost point. At that point, MAX has to choose the highest value.


from random import choice
from math import inf

# Initialize the game board
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Function to display the game board
def Gameboard(board):
    chars = {1: 'X', -1: 'O', 0: ' '}
    for x in board:
        for y in x:
            ch = chars[y]
            print(f'| {ch} |', end='')
        print('\n' + '---------------')
    print('===============')

# Function to clear the game board
def Clearboard(board):
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            board[x][y] = 0

# Function to check if a player has won the game
def winningPlayer(board, player):
    conditions = [[board[0][0], board[0][1], board[0][2]],
                  [board[1][0], board[1][1], board[1][2]],
                  [board[2][0], board[2][1], board[2][2]],
                  [board[0][0], board[1][0], board[2][0]],
                  [board[0][1], board[1][1], board[2][1]],
                  [board[0][2], board[1][2], board[2][2]],
                  [board[0][0], board[1][1], board[2][2]],
                  [board[0][2], board[1][1], board[2][0]]]

    if [player, player, player] in conditions:
        return True

    return False

# Function to check if the game has been won
def gameWon(board):
    return winningPlayer(board, 1) or winningPlayer(board, -1)

# Function to print the result of the game
def printResult(board):
    if winningPlayer(board, 1):
        print('X has won! ' + '\n')

    elif winningPlayer(board, -1):
        print('O\'s have won! ' + '\n')

    else:
        print('Draw' + '\n')

# Function to get the list of empty positions on the board
def blanks(board):
    blank = []
    for x, row in enumerate(board):
        for y, col in enumerate(row):
            if board[x][y] == 0:
                blank.append([x, y])

    return blank

# Function to check if the board is full
def boardFull(board):
    if len(blanks(board)) == 0:
        return True
    return False

# Function to set a move on the board for a player
def setMove(board, x, y, player):
    board[x][y] = player

# Function for the human player to make a move
def playerMove(board):
    e = True
    moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
             4: [1, 0], 5: [1, 1], 6: [1, 2],
             7: [2, 0], 8: [2, 1], 9: [2, 2]}
    while e:
        try:
            move = int(input('Enter a number between 1-9: '))
            if move < 1 or move > 9:
                print('Invalid Move! Try again!')
            elif not (moves[move] in blanks(board)):
                print('Invalid Move! Try again!')
            else:
                setMove(board, moves[move][0], moves[move][1], 1)
                Gameboard(board)
                e = False
        except(KeyError, ValueError):
            print('Enter a number!')

# Function to calculate the score of the current board state
def getScore(board):
    if winningPlayer(board, 1):
        return 10

    elif winningPlayer(board, -1):
        return -10

    else:
        return 0

# Function implementing the minimax algorithm with alpha-beta pruning
def abminimax(board, depth, alpha, beta, player):
    row = -1
    col = -1

    # Base case: if the maximum depth is reached or the game is won, return the score
    if depth == 0 or gameWon(board):
        return [row, col, getScore(board)]

    else:
        # Recursive case: evaluate all possible moves and choose the best one
        for cell in blanks(board):
            setMove(board, cell[0], cell[1], player)
            score = abminimax(board, depth - 1, alpha, beta, -player)

            if player == 1:
                # X is the maximizing player
                if score[2] > alpha:
                    alpha = score[2]
                    row = cell[0]
                    col = cell[1]

            else:
                # O is the minimizing player
                if score[2] < beta:
                    beta = score[2]
                    row = cell[0]
                    col = cell[1]

            # Undo the move
            setMove(board, cell[0], cell[1], 0)

            # Alpha-beta pruning
            if alpha >= beta:
                break

        if player == 1:
            return [row, col, alpha]

        else:
            return [row, col, beta]

# Function for the computer player to make a move using the minimax algorithm
def o_comp(board):
    if len(blanks(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        setMove(board, x, y, -1)
        Gameboard(board)

    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, -1)
        setMove(board, result[0], result[1], -1)
        Gameboard(board)

# Function for the human player to make a move using the minimax algorithm
def x_comp(board):
    if len(blanks(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        setMove(board, x, y, 1)
        Gameboard(board)

    else:
        result = abminimax(board, len(blanks(board)), -inf, inf, 1)
        setMove(board, result[0], result[1], 1)
        Gameboard(board)

# Function to make a move based on the current player and mode (player vs. computer or computer vs. computer)
def makeMove(board, player, mode):
    if mode == 1:
        if player == 1:
            playerMove(board)
        else:
            o_comp(board)
    else:
        if player == 1:
            o_comp(board)
        else:
            x_comp(board)

# Function to play the game between a human player and a computer player
def pvc():
    while True:
        try:
            order = int(input('Enter 1 to go first or 2 to go second: '))
            if order != 1 and order != 2:
                print('Invalid Input! Try again!')
            else:
                Gameboard(board)
                break
        except(KeyError, ValueError):
            print('Enter a number!')

    while not gameWon(board) and not boardFull(board):
        makeMove(board, 1, order)
        if gameWon(board) or boardFull(board):
            break
        makeMove(board, -1, order)

    printResult(board)
    Clearboard(board)

# Function to play the game between two computer players
def cvc():
    Gameboard(board)
    while not gameWon(board) and not boardFull(board):
        makeMove(board, 1, 2)
        if gameWon(board) or boardFull(board):
            break
        makeMove(board, -1, 2)

    printResult(board)
    Clearboard(board)

# Main function to start the game
def main():
    while True:
        try:
            mode = int(input('Enter 1 to play against the computer or 2 for computer vs. computer: '))
            if mode != 1 and mode != 2:
                print('Invalid Input! Try again!')
            else:
                if mode == 1:
                    pvc()
                else:
                    cvc()

                play_again = input('Do you want to play again? (yes/no): ')
                if play_again.lower() == 'no':
                    break
        except(KeyError, ValueError):
            print('Enter a number!')

# Start the game
if __name__ == '__main__':
    main()
