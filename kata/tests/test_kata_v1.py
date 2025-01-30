from src.main_v1 import minesweeper_basic, minesweeper_random, minesweeper_random_complete, minesweeper_with_numbers, minesweeper_with_adjacent_mines

def test_empty_grid():
    assert minesweeper_basic([0,0], []) == []

def test_no_mines():
    assert minesweeper_basic([2,2], []) == [[".","."], [".","."]]

def test_add_mine():
   assert minesweeper_basic([2,2], [[0,0]]) == [
       ["*", "."],
       [".", "."]
   ]

def test_mine_placement():
   result = minesweeper_random([2,2], [[1,1]])  # Example position
   # Count total mines in grid
   mine_count = sum(row.count('*') for row in result)
   assert mine_count == 1  # Verify exactly one mine
   assert len(result) == 2 and len(result[0]) == 2

def test_multiple_mine_placement():
    result = minesweeper_random([2,2], [], multiple_mines=True)  # Added multiple_mines flag
    print("\nGrid after placing mines:")
    for row in result:
        print(row)
    
    mine_count = sum(row.count('*') for row in result)
    total_squares = len(result) * len(result[0])
    print(f"\nNumber of mines placed: {mine_count}")
    print(f"Total squares in grid: {total_squares}")
    assert mine_count > 1 and mine_count <= total_squares

def test_single_one_adjacent_to_mine():
    # Test can work with any grid size
    grid_size = [4,3]  # or [5,3] or any size
    result = minesweeper_random(grid_size, [], ones=1, multiple_mines=False)
    print("\nGrid with mine and one adjacent '1':")
    for row in result:
        print(row)
    
    rows, cols = grid_size
    mine_count = sum(row.count('*') for row in result)
    one_count = sum(row.count('1') for row in result)
    print(f"\nMine count: {mine_count}")
    print(f"Number of '1's: {one_count}")
    assert mine_count == 1 and one_count == 1
    
    # Check adjacency using grid_size parameters
    adjacent_found = False
    for i in range(rows):
        for j in range(cols):
            if result[i][j] == '*':
                #print(f"\nFound mine at position [{i},{j}]")
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        #print(f"Checking adjacent position [{ni},{nj}]: {result[ni][nj]}")
                        if result[ni][nj] == '1':
                            adjacent_found = True
                            #print("Found adjacent '1'!")
    
    #print(f"\nAdjacent '1' found: {adjacent_found}")
    assert adjacent_found

def test_multiple_ones_adjacent_to_mine():
    grid_size = [5,3]  # or any size
    result = minesweeper_random(grid_size, [], multiple_ones=True)
    print("\nGrid with mine and multiple adjacent '1's:")
    for row in result:
        print(row)
    
    rows, cols = grid_size
    
    # Check we have one mine
    mine_count = sum(row.count('*') for row in result)
    print(f"\nMine count: {mine_count}")
    assert mine_count == 1
    
    # Check we have at least one '1'
    one_count = sum(row.count('1') for row in result)
    print(f"Number of '1's: {one_count}")
    assert one_count > 0
    
    # Check all '1's are adjacent to mine (non-diagonal)
    valid_ones = True
    mine_position = None
    
    # Find mine position
    for i in range(rows):
        for j in range(cols):
            if result[i][j] == '*':
                mine_position = (i,j)
                break
                
    # Check each '1' is adjacent to mine
    for i in range(rows):
        for j in range(cols):
            if result[i][j] == '1':
                # Check if this '1' is adjacent to mine
                mi, mj = mine_position
                if abs(i - mi) + abs(j - mj) != 1:  # Manhattan distance should be 1 for adjacency
                    valid_ones = False
                    
    print(f"All '1's are valid adjacent positions: {valid_ones}")
    assert valid_ones

def test_multiple_mines_with_multiple_ones():
    grid_size = [12,6]  # example size
    result = minesweeper_random_complete(grid_size)
    print("\nGrid with multiple mines and ones:")
    for row in result:
        print(row)
    
    rows, cols = grid_size
    total_squares = rows * cols
    
    # Count mines and ones
    mine_count = sum(row.count('*') for row in result)
    one_count = sum(row.count('1') for row in result)
    print(f"\nNumber of mines: {mine_count}")
    print(f"Number of '1's: {one_count}")
    
    # Verify we have at least one mine but not all squares
    assert 0 < mine_count < total_squares
    
    # Verify each '1' is adjacent to at least one mine
    valid_ones = True
    for i in range(rows):
        for j in range(cols):
            if result[i][j] == '1':
                # Check if this '1' has at least one adjacent mine
                has_adjacent_mine = False
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if result[ni][nj] == '*':
                            has_adjacent_mine = True
                            break
                if not has_adjacent_mine:
                    valid_ones = False
                    break
    
    print(f"All '1's are valid (adjacent to mines): {valid_ones}")
    assert valid_ones

def test_calculate_adjacent_mine_numbers():
    grid_size = [12, 6]  # As shown in image
    mine_position = [3, 4]  # Middle position for single mine
    result = minesweeper_with_numbers(grid_size, [mine_position])
    print("\nGrid with calculated numbers:")
    for row in result:
        print(row)
    
    rows, cols = grid_size
    
    # Verify grid size
    assert len(result) == rows and len(result[0]) == cols
    
    # Verify mine placement
    assert result[3][4] == "*"
    
    # Verify numbers around mine
    # Check the 8 positions around mine should have correct numbers
    # In image: positions above, below, left, right should be '1'
    positions_to_check = [
        (2, 4), # above
        (4, 4), # below
        (3, 3), # left
        (3, 5)  # right
    ]
    
    for i, j in positions_to_check:
        print(f"Checking position [{i},{j}]: {result[i][j]}")
        assert result[i][j] == "1"
    
    # Verify rest of grid is '.'
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in positions_to_check and (i, j) != (3, 4):
                assert result[i][j] == "."

def test_multiple_mines_with_numbers():
    grid_size = [12, 6]
    # mines should have col < 6 since grid is 12x6
    mine_positions = [(3, 2), (3, 3), (3, 4)]
    
    print(f"\nGrid size: {grid_size}")
    print(f"Mine positions: {mine_positions}")
    
    result = minesweeper_with_numbers(grid_size, mine_positions)
    
    print("\nGrid with multiple mines and numbers:")
    for row in result:
        print(row)
    
    # Test sequence:
    # 1. Verify grid dimensions
    assert len(result) == 12, f"Expected 12 rows, got {len(result)}"
    assert len(result[0]) == 6, f"Expected 6 cols, got {len(result[0])}"
    
    # 2. Verify mine placements
    for row, col in mine_positions:
        assert result[row][col] == "*", f"Expected * at [{row},{col}], got {result[row][col]}"
    
    # 3. Verify numbers around mines
    test_cases = [
        ((2, 2), "1"),  # Above first mine
        ((2, 3), "1"),  # Above second mine
        ((2, 4), "1"),  # Above third mine
        ((3, 1), "1"),  # Left of first mine
        ((3, 5), "1"),  # Right of last mine
        ((4, 2), "1"),  # Below first mine
        ((4, 3), "1"),  # Below second mine
        ((4, 4), "1"),  # Below third mine
        ((3, 3), "*"),  # Middle mine position
    ]
    
    print("\nChecking positions:")
    for (i, j), expected in test_cases:
        actual = result[i][j]
        print(f"Position [{i},{j}]: Expected {expected}, Got {actual}")
        assert actual == expected, f"Position [{i},{j}]: Expected {expected}, Got {actual}"

def test_random_multiple_mines_with_numbers():
    grid_size = [12, 6]
    print(f"\nGrid size: {grid_size}")
    
    result = minesweeper_with_numbers(grid_size)  # We'll modify function to generate random mines
    
    print("\nGrid with random mines and numbers:")
    for row in result:
        print(row)
    
    # Test sequence:
    # 1. Verify grid dimensions
    assert len(result) == 12, f"Expected 12 rows, got {len(result)}"
    assert len(result[0]) == 6, f"Expected 6 cols, got {len(result[0])}"
    
    # 2. Count mines placed
    mine_count = sum(row.count('*') for row in result)
    print(f"\nNumber of mines placed: {mine_count}")
    assert mine_count > 0, "Should have at least one mine"
    
    # 3. Verify numbers are correct
    for i in range(12):
        for j in range(6):
            if result[i][j] != '*':  # For non-mine positions
                # Count adjacent mines
                adjacent_mines = 0
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 12 and 0 <= nj < 6:
                        if result[ni][nj] == '*':
                            adjacent_mines += 1
                            
                if adjacent_mines > 0:
                    assert result[i][j] == str(adjacent_mines), \
                        f"Position [{i},{j}] shows {result[i][j]} but has {adjacent_mines} adjacent mines"

def test_minesweeper_with_adjacent_mines():
    grid_size = [12, 6]
    result = minesweeper_with_adjacent_mines(grid_size)
    
    print("\nGrid with mines and adjacent numbers (including diagonals):")
    for row in result:
        print(row)
    
    # 1. Verify grid dimensions
    assert len(result) == 12 and len(result[0]) == 6, "Grid size incorrect"
    
    # 2. Verify mine count and valid characters
    mine_count = 0
    max_adjacent_mines = 8  # Maximum possible adjacent mines (8 directions)
    valid_chars = set(['*', '.'] + [str(i) for i in range(1, max_adjacent_mines + 1)])
    
    for i in range(12):
        for j in range(6):
            char = result[i][j]
            assert char in valid_chars, f"Invalid character {char} at position [{i},{j}]"
            if char == '*':
                mine_count += 1
                
    print(f"\nNumber of mines placed: {mine_count}")
    print(f"Valid characters found: {sorted(list(set(char for row in result for char in row)))}")
    assert mine_count > 0, "No mines placed"

def test_eight_direction_adjacent_mines():
    grid_size = [10, 5]
    result = minesweeper_with_adjacent_mines(grid_size)

    print("\nGrid with mines and adjacent numbers:")
    for row in result:
        print(row)
    
    # Verify each cell's number matches its adjacent mine count
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if result[i][j] not in ['*', '.']:
                adjacent_mines = 0
                # Check all 8 directions
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < grid_size[0] and 0 <= nj < grid_size[1] and result[ni][nj] == '*':
                            adjacent_mines += 1
                
                shown_number = int(result[i][j])
                assert shown_number == adjacent_mines, \
                    f"Position [{i},{j}] shows {shown_number} but has {adjacent_mines} adjacent mines. Mine positions:\n" + \
                    "\n".join([f"[{ni},{nj}]" for di in [-1,0,1] for dj in [-1,0,1] 
                             if (di!=0 or dj!=0) and 0 <= (ni:=i+di) < grid_size[0] and 0 <= (nj:=j+dj) < grid_size[1] 
                             and result[ni][nj] == '*'])