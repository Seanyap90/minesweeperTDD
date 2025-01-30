def minesweeper_basic(gridSize=[], mines=[]):
    if not gridSize:
        return []
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    for row, col in mines:
        grid[row][col] = "*"
        
    return grid

def minesweeper_random(gridSize=[], mines=[], ones=0, multiple_mines=False, multiple_ones=False):
    if not gridSize:
        return []
    import random
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    positions = [(i,j) for i in range(rows) for j in range(cols)]
    
    if multiple_mines:
        total_squares = rows * cols
        max_mines = min(total_squares - 1, total_squares // 2)
        num_mines = random.randint(2, max_mines)
        mine_positions = random.sample(positions, num_mines)
        for pos in mine_positions:
            grid[pos[0]][pos[1]] = "*"
    else:
        # Place single mine
        mine_pos = random.choice(positions)
        grid[mine_pos[0]][mine_pos[1]] = "*"
        
        if ones > 0 or multiple_ones:
            # Get valid adjacent positions (non-diagonal)
            adjacent_positions = []
            i, j = mine_pos
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    adjacent_positions.append((ni, nj))
            
            if adjacent_positions:
                if multiple_ones:
                    # Randomly choose how many ones to place
                    num_ones = random.randint(1, len(adjacent_positions))
                    one_positions = random.sample(adjacent_positions, num_ones)
                    for pos in one_positions:
                        grid[pos[0]][pos[1]] = "1"
                else:
                    # Place single one
                    one_pos = random.choice(adjacent_positions)
                    grid[one_pos[0]][one_pos[1]] = "1"
    
    return grid

def minesweeper_random_complete(gridSize=[]):
    if not gridSize:
        return []
    import random
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    # Place random number of mines
    total_squares = rows * cols
    max_mines = min(total_squares - 1, total_squares // 2)
    num_mines = random.randint(1, max_mines)
    positions = [(i,j) for i in range(rows) for j in range(cols)]
    mine_positions = random.sample(positions, num_mines)
    
    # Place mines
    for pos in mine_positions:
        grid[pos[0]][pos[1]] = "*"
    
    # Find all possible positions for ones (adjacent to mines)
    possible_one_positions = set()
    for mi, mj in mine_positions:
        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            ni, nj = mi + di, mj + dj
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == ".":
                possible_one_positions.add((ni, nj))
    
    # Place random number of ones in valid positions
    if possible_one_positions:
        num_ones = random.randint(1, len(possible_one_positions))
        one_positions = random.sample(list(possible_one_positions), num_ones)
        for pos in one_positions:
            grid[pos[0]][pos[1]] = "1"
    
    return grid

def minesweeper_with_numbers(gridSize=[], mines=[]):
    if not gridSize:
        return []
    import random
    rows, cols = gridSize
    grid = []
    
    # Create grid
    for i in range(rows):
        row = ["." for _ in range(cols)]
        grid.append(row)
    
    # If no mines specified, place random mines
    if not mines:
        total_squares = rows * cols
        num_mines = random.randint(1, total_squares // 4)
        possible_positions = [(i,j) for i in range(rows) for j in range(cols)]
        mines = random.sample(possible_positions, num_mines)
    
    # Place mines
    for row, col in mines:
        grid[row][col] = "*"
    
    # Calculate numbers - ONLY checking 4 adjacent positions (not diagonals)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "*":
                continue
                
            mine_count = 0
            # Only check up, down, left, right
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    if grid[ni][nj] == "*":
                        mine_count += 1
                        
            if mine_count > 0:
                grid[i][j] = str(mine_count)
    
    return grid

def minesweeper_with_adjacent_mines(gridSize=[]):
    if not gridSize:
        return []
    import random
    rows, cols = gridSize
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    
    # Place mines
    total_squares = rows * cols
    num_mines = random.randint(1, total_squares // 4)
    all_positions = [(i,j) for i in range(rows) for j in range(cols)]
    mine_positions = set(random.sample(all_positions, num_mines))
    
    for i, j in mine_positions:
        grid[i][j] = "*"
    
    # Calculate numbers looking at all 8 adjacent positions
    directions = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if not (i==0 and j==0)]
    for i in range(rows):
        for j in range(cols):
            if (i,j) not in mine_positions:
                count = 0
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and (ni,nj) in mine_positions:
                        count += 1
                if count > 0:
                    grid[i][j] = str(count)
                    
    return grid