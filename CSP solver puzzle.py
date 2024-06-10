Backtrack_sudoku_calls = 0
forward_checking_calls = 0
maintain_arc_consistency_calls = 0


def solve_sudoku(board):
    if is_complete(board):
        return board

    row, col = find_empty_cell(board)
    for value in range(1, 10):
        if is_valid(board, row, col, value):
            board[row][col] = value
            result = solve_sudoku(board)
            if result is not None:
                return result

            board[row][col] = 0  # Backtrack if the value is not valid

    return None


def solve_sudoku_with_forward_checking(board):
    global forward_checking_calls
    ##forward_checking_calls += 1

    if is_complete(board):
        return board

    row, col = find_empty_cell(board)
    for value in range(1, 10):
        if is_valid(board, row, col, value):
            board[row][col] = value

            if forward_checking(board, row, col):
                forward_checking_calls += 1
                result = solve_sudoku_with_forward_checking(board)
                if result is not None:
                    return result

            board[row][col] = 0  # Backtrack if the value is not valid

    return None


def solve_sudoku_with_arc_consistency(board):
    global maintain_arc_consistency_calls
    maintain_arc_consistency_calls += 1
    
    

    if is_complete(board):
        return board

    row, col = find_empty_cell(board)
    
    for value in range(1, 10):
        if is_valid(board, row, col, value):
            board[row][col] = value

            if maintain_arc_consistency(board):
                maintain_arc_consistency_calls += 1

                result = solve_sudoku_with_arc_consistency(board)
                if result is not None:
                    return result

            board[row][col] = 0  # Backtrack if the value is not valid
            

    return None
    
      

  



def solve_sudoku_with_backtracking(board):
    global Backtrack_sudoku_calls
    ##Backtrack_sudoku_calls += 1
    # Check if the Sudoku board is complete
    if is_complete(board):
        return board

    # Find the next empty cell in the Sudoku board
    row, col = find_empty_cell(board)

    # Try assigning values from 1 to 9 to the empty cell
    for value in range(1, 10):
        if is_valid(board, row, col, value):
            # Assign the value to the cell
            board[row][col] = value

            # Recursively solve the Sudoku board
            Backtrack_sudoku_calls += 1
            result = solve_sudoku_with_backtracking(board)

            # If a solution is found, return it
            if result is not None:
                return result

            # Backtrack by resetting the value if the assigned value doesn't lead to a solution
            board[row][col] = 0

    # If no value leads to a solution, return None
    return None


def is_complete(board):
    # Check if the Sudoku board is complete
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True


def find_empty_cell(board):
    # Find the next empty cell in the Sudoku board
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None, None


def is_valid(board, row, col, value):
    # Check if assigning the value to the cell at (row, col) is valid
    # by ensuring it doesn't violate the Sudoku rules

    # Check if the value is already in the same row or column
    for i in range(9):
        if board[row][i] == value or board[i][col] == value:
            return False

    # Check if the value is in the same 3x3 box
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for i in range(box_start_row, box_start_row + 3):
        for j in range(box_start_col, box_start_col + 3):
            if board[i][j] == value:
                return False

    return True


def forward_checking(board, row, col):
    # Apply forward checking to reduce the domains of the unassigned variables

    # Check the current row and column
    for i in range(9):
        if board[row][i] == 0 and not has_valid_assignment(board, row, i):
            return False
        if board[i][col] == 0 and not has_valid_assignment(board, i, col):
            return False

    # Check the current 3x3 box
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for i in range(box_start_row, box_start_row + 3):
        for j in range(box_start_col, box_start_col + 3):
            if board[i][j] == 0 and not has_valid_assignment(board, i, j):
                return False

    return True


def has_valid_assignment(board, row, col):
    # Check if there is at least one valid assignment for the cell at (row, col)
    for value in range(1, 10):
        if is_valid(board, row, col, value):
            return True
    return False


def maintain_arc_consistency(board):
    queue = []

    # Add all empty cells to the queue
    if maintain_arc_consistency_calls == 1:

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    queue.append((row, col))

    while queue:
        row, col = queue.pop(0)

        if revise(board, row, col):
            if board[row][col] == 0:  # If the domain becomes empty, return False
                return False

            # Add all affected neighbors to the queue
            neighbors = get_neighbors(row, col)
            for neighbor in neighbors:
                queue.append(neighbor)

    return True


def revise(board, row, col):
    revised = False
    domain = get_domain(board, row, col)

    for value in domain:
        if not has_support(board, row, col, value):
            board[row][col] = 0  # Remove the value from the domain
            revised = True

    return revised


def has_support(board, row, col, value):
    # Check if there is at least one neighbor that supports the value for the cell at (row, col)
    neighbors = get_neighbors(row, col)

    for neighbor in neighbors:
        n_row, n_col = neighbor
        if board[n_row][n_col] == 0 and is_valid(board, n_row, n_col, value):
            return True

    return False


def get_domain(board, row, col):
    # Get the domain (possible values) for the cell at (row, col)
    domain = set(range(1, 10))

    # Remove values that are already assigned in the same row and column
    for i in range(9):
        domain.discard(board[row][i])
        domain.discard(board[i][col])

    # Remove values that are already assigned in the same 3x3 box
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for i in range(box_start_row, box_start_row + 3):
        for j in range(box_start_col, box_start_col + 3):
            domain.discard(board[i][j])

    return domain


def get_neighbors(row, col):
    # Get the neighbors of the cell at (row, col)
    neighbors = []

    # Add all cells in the same row
    for i in range(9):
        if i != col:
            neighbors.append((row, i))

    # Add all cells in the same column
    for i in range(9):
        if i != row:
            neighbors.append((i, col))

    # Add all cells in the same 3x3 box
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for i in range(box_start_row, box_start_row + 3):
        for j in range(box_start_col, box_start_col + 3):
            if i != row and j != col:
                neighbors.append((i, j))

    return neighbors


def print_board(board):
    for row in board:
        print(row)


# Example Sudoku board
sudoku_board = [
   [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
sudoku_board2 = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
sudoku_board3 = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


print()

print("Sudoku solved with forward checking:")
solution = solve_sudoku_with_forward_checking(sudoku_board)
if solution is not None:
    print_board(solution)
else:
    print("No solution exists for the given sudoku board")

print()

print("Sudoku solved with arc consistency:")
solution1 = solve_sudoku_with_arc_consistency(sudoku_board2)
if solution1 is not None:
    print_board(solution1)
else:
    print("No solution exists for the given Sudoku board.")

print()

print("Sudoku solved with backtracking")
solutionBT = solve_sudoku_with_backtracking(sudoku_board3)
if solutionBT is not None:
    print_board(solutionBT)
else:
    print("No solution exists for the given Sudoku board.")

print()

print("Recursive count for forward checking: ")
print(forward_checking_calls)

print()

print("Recursive count for Arc consistency: ")
print(maintain_arc_consistency_calls)

print()

print("Recursive count for Back tracking: ")
print(Backtrack_sudoku_calls)
