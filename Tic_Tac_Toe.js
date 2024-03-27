// Initialize the game board
let board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
];

// Function to display the game board
function Gameboard(board) {
    const chars = {1: 'X', '-1': 'O', '0': ' '};
    for (let x = 0; x < 3; x++) {
        let row = '';
        for (let y = 0; y < 3; y++) {
            const ch = chars[board[x][y].toString()];
            row += `| ${ch} |`;
        }
        console.log(row + '\n' + '---------------');
    }
    console.log('===============');
}

// Function to check if the game has been won
function gameWon(board) {
    return winningPlayer(board, 1) || winningPlayer(board, -1);
}

// Function to check if a player has won the game
function winningPlayer(board, player) {
    const conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ];

    return conditions.some(condition => condition.every(cell => cell === player));
}

// Function to get the list of empty positions on the board
function blanks(board) {
    const blank = [];
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            if (board[x][y] === 0) {
                blank.push([x, y]);
            }
        }
    }
    return blank;
}

// Function to check if the board is full
function boardFull(board) {
    return blanks(board).length === 0;
}

// Function to set a move on the board for a player
function setMove(board, x, y, player) {
    board[x][y] = player;
}

// Function to calculate the score of the current board state
function getScore(board) {
    if (winningPlayer(board, 1)) {
        return 10;
    } else if (winningPlayer(board, -1)) {
        return -10;
    } else {
        return 0;
    }
}

// Function implementing the minimax algorithm with alpha-beta pruning
function abminimax(board, depth, alpha, beta, player) {
    let row = -1;
    let col = -1;

    // Base case: if the maximum depth is reached or the game is won, return the score
    if (depth === 0 || gameWon(board)) {
        return [row, col, getScore(board)];
    } else {
        // Recursive case: evaluate all possible moves and choose the best one
        for (const cell of blanks(board)) {
            setMove(board, cell[0], cell[1], player);
            const score = abminimax(board, depth - 1, alpha, beta, -player);

            if (player === 1) {
                // X is the maximizing player
                if (score[2] > alpha) {
                    alpha = score[2];
                    row = cell[0];
                    col = cell[1];
                }
            } else {
                // O is the minimizing player
                if (score[2] < beta) {
                    beta = score[2];
                    row = cell[0];
                    col = cell[1];
                }
            }

            // Undo the move
            setMove(board, cell[0], cell[1], 0);

            // Alpha-beta pruning
            if (alpha >= beta) {
                break;
            }
        }

        return [row, col, player === 1 ? alpha : beta];
    }
}

// Function for the computer player to make a move using the minimax algorithm
function o_comp(board) {
    if (blanks(board).length === 9) {
        const x = Math.floor(Math.random() * 3);
        const y = Math.floor(Math.random() * 3);
        setMove(board, x, y, -1);
        Gameboard(board);
    } else {
        const result = abminimax(board, blanks(board).length, -Infinity, Infinity, -1);
        setMove(board, result[0], result[1], -1);
        Gameboard(board);
    }
}

// Function for the human player to make a move
function playerMove(board) {
    let e = true;
    const moves = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 9: [2, 2]};
    while (e) {
        const move = parseInt(prompt('Enter a number between 1-9: '));
        if (move < 1 || move > 9) {
            alert('Invalid Move! Try again!');
        } else if (!blanks(board).some(([x, y]) => moves[move][0] === x && moves[move][1] === y)) {
            alert('Invalid Move! Try again!');
        } else {
            setMove(board, moves[move][0], moves[move][1], 1);
            Gameboard(board);
            e = false;
        }
    }
}

// Function to make a move based on the current player and mode (player vs. computer)
function makeMove(board, player, mode) {
    if (mode === 1) {
        if (player === 1) {
            playerMove(board);
        } else {
            o_comp(board);
        }
    }
}

// Function to play the game between a human player and a computer player
function pvc() {
    let order;
    do {
        order = parseInt(prompt('Enter 1 to go first or 2 to go second: '));
    } while (order !== 1 && order !== 2);

    Gameboard(board);

    while (!gameWon(board) && !boardFull(board)) {
        makeMove(board, 1, order);
        if (gameWon(board) || boardFull(board)) {
            break;
        }
    }
}

// Start the game
pvc();
