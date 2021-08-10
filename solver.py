# solver.py
def find_zero(board):
    board_row = 0
    for row in board:
        board_col = 0
        for value in row:
            if value == 0:
                return [board_row, board_col]
            board_col += 1
        board_row += 1
    return None


def is_valid(board, value, row, col):
    num_row = len(board)
    num_col = len(board[0])

    for i in range(num_col):
        if board[row][i] == value and col != i:
            return False
    
    for i in range(num_row):
        if board[i][col] == value and row != i:
            return False
        
    start_row = row // 3
    start_col = col // 3

    for i in range(start_row*3, start_row*3 + 3):
        for j in range(start_col*3, start_col*3 + 3):
            if board[i][j] == value and (row != i or col != j):
                return False
    return True