from src.main_v2 import (
    minesweeper_basic,
    minesweeper_random,
    minesweeper_random_revised,
    minesweeper_with_numbers,
    minesweeper_with_adjacent_mines,
)

# Helper function to count mines or numbers in a grid
def count_in_grid(grid, char):
    return sum(row.count(char) for row in grid)

# Helper function to check if a position is adjacent to a mine
def is_adjacent_to_mine(grid, i, j, include_diagonals=True):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if include_diagonals:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == "*":
            return True
    return False

# Helper function to print the grid
def print_grid(grid, title="Grid"):
    print(f"\n{title}:")
    for row in grid:
        print(" ".join(row))

# Test empty grid
def test_empty_grid():
    result = minesweeper_basic([0, 0], [])
    print_grid(result, "Empty Grid")
    assert result == []

# Test grid with no mines
def test_no_mines():
    result = minesweeper_basic([2, 2], [])
    print_grid(result, "Grid with No Mines")
    assert result == [[".", "."], [".", "."]]

# Test adding a single mine
def test_add_mine():
    result = minesweeper_basic([2, 2], [[0, 0]])
    print_grid(result, "Grid with Single Mine")
    assert result == [["*", "."], [".", "."]]

# Test random mine placement
def test_mine_placement():
    result = minesweeper_random([2, 2])
    print_grid(result, "Grid with Random Mine Placement")
    mine_count = count_in_grid(result, "*")
    assert mine_count == 1
    assert len(result) == 2 and len(result[0]) == 2

# Test multiple mine placements
def test_multiple_mine_placement():
    result = minesweeper_random([2, 2], multiple_mines=True)
    print_grid(result, "Grid with Multiple Mines")
    mine_count = count_in_grid(result, "*")
    total_squares = len(result) * len(result[0])
    assert 2 <= mine_count <= total_squares // 2

# Test single '1' adjacent to a mine
def test_single_one_adjacent_to_mine(grid_size=None):
    if grid_size is None:
        grid_size = [5, 3]  # default size
    else:
        # Parse grid size from string "ROWSxCOLS" format
        rows, cols = map(int, grid_size.split('x'))
        grid_size = [rows, cols]
    
    result = minesweeper_random(grid_size, ones=1)
    print_grid(result, f"Grid {grid_size[0]}x{grid_size[1]} with Single '1' Adjacent to Mine")
    
    mine_count = count_in_grid(result, "*")
    one_count = count_in_grid(result, "1")
    assert mine_count == 1 and one_count == 1
    assert any(is_adjacent_to_mine(result, i, j, include_diagonals=False) 
              for i in range(grid_size[0]) 
              for j in range(grid_size[1]) 
              if result[i][j] == "1")

# Test multiple '1's adjacent to a mine
def test_multiple_ones_adjacent_to_mine(grid_size=None):
    if grid_size is None:
        grid_size = [5, 3]  # default size
    else:
        rows, cols = map(int, grid_size.split('x'))
        grid_size = [rows, cols]
    
    result = minesweeper_random(grid_size, multiple_ones=True)
    print_grid(result, f"Grid {grid_size[0]}x{grid_size[1]} with Multiple '1's Adjacent to Mine")
    
    mine_count = count_in_grid(result, "*")
    one_count = count_in_grid(result, "1")
    assert mine_count == 1 and one_count > 0
    assert all(is_adjacent_to_mine(result, i, j, include_diagonals=False) 
              for i in range(grid_size[0]) 
              for j in range(grid_size[1]) 
              if result[i][j] == "1")

# Test multiple mines with multiple '1's
def test_multiple_mines_with_multiple_ones(grid_size=None):
    if grid_size is None:
        grid_size = [12, 6]  # default size
    else:
        rows, cols = map(int, grid_size.split('x'))
        grid_size = [rows, cols]
    
    result = minesweeper_random_revised(grid_size)
    print_grid(result, f"Grid {grid_size[0]}x{grid_size[1]} with Multiple Mines and '1's")
    
    mine_count = count_in_grid(result, "*")
    one_count = count_in_grid(result, "1")
    total_squares = grid_size[0] * grid_size[1]
    assert 0 < mine_count < total_squares
    assert all(is_adjacent_to_mine(result, i, j, include_diagonals=False) 
              for i in range(grid_size[0]) 
              for j in range(grid_size[1]) 
              if result[i][j] == "1")

# Test numbers around a single mine
def test_calculate_adjacent_mine_numbers():
    grid_size = [12, 6]
    mine_position = (3, 4)
    result = minesweeper_with_numbers(grid_size, [mine_position])
    print_grid(result, "Grid with Numbers Around a Single Mine")
    assert len(result) == 12 and len(result[0]) == 6
    assert result[3][4] == "*"
    positions_to_check = [(2, 4), (4, 4), (3, 3), (3, 5)]
    for i, j in positions_to_check:
        assert result[i][j] == "1"
    assert all(result[i][j] == "." for i in range(12) for j in range(6) if (i, j) not in positions_to_check and (i, j) != (3, 4))

# Test multiple mines with numbers
def test_multiple_mines_with_numbers():
    grid_size = [12, 6]
    mine_positions = [(3, 2), (3, 3), (3, 4)]
    result = minesweeper_with_numbers(grid_size, mine_positions)
    print_grid(result, "Grid with Multiple Mines and Numbers")
    assert len(result) == 12 and len(result[0]) == 6
    for row, col in mine_positions:
        assert result[row][col] == "*"
    test_cases = [
        ((2, 2), "1"), ((2, 3), "1"), ((2, 4), "1"),
        ((3, 1), "1"), ((3, 5), "1"),
        ((4, 2), "1"), ((4, 3), "1"), ((4, 4), "1"),
    ]
    for (i, j), expected in test_cases:
        assert result[i][j] == expected

# Test random multiple mines with numbers
def test_random_multiple_mines_with_numbers():
    grid_size = [12, 6]
    result = minesweeper_with_numbers(grid_size)
    print_grid(result, "Grid with Random Mines and Numbers")
    assert len(result) == 12 and len(result[0]) == 6
    mine_count = count_in_grid(result, "*")
    assert mine_count > 0
    for i in range(12):
        for j in range(6):
            if result[i][j] != "*":
                adjacent_mines = sum(
                    1 for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= i + di < 12 and 0 <= j + dj < 6 and result[i + di][j + dj] == "*"
                )
                if adjacent_mines > 0:
                    assert result[i][j] == str(adjacent_mines)

# Test minesweeper with adjacent mines (including diagonals)
def test_minesweeper_with_adjacent_mines(grid_size=None):
    if grid_size is None:
        grid_size = [12, 6]  # default size
    else:
        rows, cols = map(int, grid_size.split('x'))
        grid_size = [rows, cols]
    
    rows, cols = grid_size
    result = minesweeper_with_adjacent_mines(grid_size)
    print_grid(result, f"Grid {rows}x{cols} with Adjacent Mines (Including Diagonals)")

    # Verify grid dimensions
    assert len(result) == rows, f"Expected {rows} rows, got {len(result)}"
    assert len(result[0]) == cols, f"Expected {cols} columns, got {len(result[0])}"

    # Count mines and ensure at least one mine is placed
    mine_count = count_in_grid(result, "*")
    assert mine_count > 0, "No mines were placed in the grid"

    # Verify that numbers correctly represent adjacent mines
    for i in range(rows):
        for j in range(cols):
            if result[i][j] not in ["*", "."]:
                # Count adjacent mines in all 8 directions
                adjacent_mines = sum(
                    1 for di in [-1, 0, 1] for dj in [-1, 0, 1]
                    if (di != 0 or dj != 0)  # Exclude the current cell
                    and 0 <= i + di < rows  # Check row bounds
                    and 0 <= j + dj < cols  # Check column bounds
                    and result[i + di][j + dj] == "*"  # Check for mines
                )
                # Ensure the number matches the count of adjacent mines
                assert result[i][j] == str(adjacent_mines), (
                    f"Position [{i},{j}] shows {result[i][j]} but has {adjacent_mines} adjacent mines."
                )