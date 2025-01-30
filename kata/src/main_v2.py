import random
from collections import defaultdict

def generate_positions(rows, cols):
    """Helper function to generate all positions in the grid."""
    return [(i, j) for i in range(rows) for j in range(cols)]

def get_adjacent_positions(i, j, rows, cols, include_diagonals=True):
    """Helper function to get valid adjacent positions."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if include_diagonals:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return [
        (i + di, j + dj)
        for di, dj in directions
        if 0 <= i + di < rows and 0 <= j + dj < cols
    ]

def minesweeper_basic(gridSize=[], mines=[]):
    if not gridSize:
        return []
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    for row, col in mines:
        grid[row][col] = "*"
        
    return grid

def minesweeper_random(gridSize=[], mines=[], ones=0, multiple_mines=False, multiple_ones=False):
    """Handles single/multiple mine placement with optional adjacent '1's.
    Developed to support basic random placement, then extended for multiple mines and '1's placement cases."""
    if not gridSize:
        return []
    
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    positions = generate_positions(rows, cols)
    
    if multiple_mines:
        total_squares = rows * cols
        max_mines = min(total_squares - 1, total_squares // 2)
        num_mines = random.randint(2, max_mines)
        mine_positions = random.sample(positions, num_mines)
        for pos in mine_positions:
            grid[pos[0]][pos[1]] = "*"
    else:
        mine_pos = random.choice(positions)
        grid[mine_pos[0]][mine_pos[1]] = "*"
        
        if ones > 0 or multiple_ones:
            adjacent_positions = get_adjacent_positions(mine_pos[0], mine_pos[1], rows, cols, include_diagonals=False)
            
            if adjacent_positions:
                if multiple_ones:
                    num_ones = random.randint(1, len(adjacent_positions))
                    one_positions = random.sample(adjacent_positions, num_ones)
                    for pos in one_positions:
                        grid[pos[0]][pos[1]] = "1"
                else:
                    one_pos = random.choice(adjacent_positions)
                    grid[one_pos[0]][one_pos[1]] = "1"
    
    return grid

def minesweeper_random_revised(gridSize=[]):
    """Creates a grid with multiple mines and multiple adjacent '1's in one pass.
    Consolidates the multiple mines and multiple '1's placement into a more efficient implementation."""
    if not gridSize:
        return []
    
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    total_squares = rows * cols
    max_mines = min(total_squares - 1, total_squares // 2)
    num_mines = random.randint(1, max_mines)
    positions = generate_positions(rows, cols)
    mine_positions = set(random.sample(positions, num_mines))
    
    for pos in mine_positions:
        grid[pos[0]][pos[1]] = "*"
    
    possible_one_positions = set()
    for mi, mj in mine_positions:
        adjacent_positions = get_adjacent_positions(mi, mj, rows, cols, include_diagonals=False)
        possible_one_positions.update(
            (ni, nj) for ni, nj in adjacent_positions if grid[ni][nj] == "."
        )
    
    if possible_one_positions:
        num_ones = random.randint(1, len(possible_one_positions))
        one_positions = random.sample(list(possible_one_positions), num_ones)
        for pos in one_positions:
            grid[pos[0]][pos[1]] = "1"
    
    return grid

def minesweeper_with_numbers(gridSize=[], mines=[]):
    """Places mines at specified positions (or randomly if none provided) and marks each adjacent cell with number of mines next to it, excluding diagonals."""
    if not gridSize:
        return []
    
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    if not mines:
        total_squares = rows * cols
        num_mines = random.randint(1, total_squares // 4)
        mines = set(random.sample(generate_positions(rows, cols), num_mines))
    
    for row, col in mines:
        grid[row][col] = "*"
    
    adjacent_mine_counts = defaultdict(int)
    for row, col in mines:
        for ni, nj in get_adjacent_positions(row, col, rows, cols, include_diagonals=False):
            if (ni, nj) not in mines:
                adjacent_mine_counts[(ni, nj)] += 1
    
    for (i, j), count in adjacent_mine_counts.items():
        grid[i][j] = str(count)
    
    return grid

def minesweeper_with_adjacent_mines(gridSize=[]):
    """Randomly places mines and marks each adjacent cell with count of neighboring mines, including diagonals."""
    if not gridSize:
        return []
    
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    total_squares = rows * cols
    num_mines = random.randint(1, total_squares // 4)
    mine_positions = set(random.sample(generate_positions(rows, cols), num_mines))
    
    for i, j in mine_positions:
        grid[i][j] = "*"
    
    adjacent_mine_counts = defaultdict(int)
    for i, j in mine_positions:
        for ni, nj in get_adjacent_positions(i, j, rows, cols, include_diagonals=True):
            if (ni, nj) not in mine_positions:
                adjacent_mine_counts[(ni, nj)] += 1
    
    for (i, j), count in adjacent_mine_counts.items():
        grid[i][j] = str(count)
    
    return grid