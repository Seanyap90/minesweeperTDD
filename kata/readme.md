# Minesweeper Grid Generator

A Python implementation of various Minesweeper grid generation algorithms with different configurations.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd minesweeper
```

2. Install dependencies:
```bash
make install
```

## Project Structure

```
minesweeper/
├── src/
│   └── main_v2.py        # Core implementation
├── tests/
│   └── test_kata_v2.py   # Test cases
├── Makefile              # Build and test automation
├── run.sh               # Shell script for running commands
└── README.md            # This file
```

## Usage

### Running Tests

1. Run all tests:
```bash
make test
```

2. Run specific test categories:
```bash
make basic              # Basic grid tests
make random            # Random placement tests
make ones              # Tests for '1's placement
make revised           # Tests for revised algorithm
make numbers           # Number calculation tests
make adjacent          # Adjacent mines tests
```

3. Run tests with custom grid sizes:
```bash
make ones SINGLE_ONE_GRID_SIZE=5x3
make revised MULTIPLE_MINES_GRID_SIZE=12x12
make adjacent MULTIPLE_MINES_GRID_SIZE=10x10
```

### Direct Grid Generation

1. Basic grid with specified mines:
```bash
make basic_grid GRID_SIZE=5x5 MINES="[[0,0],[1,1]]"
```

2. Random grid generation:
```bash
make random_grid GRID_SIZE=8x8
make random_grid_revised GRID_SIZE=10x10
```

3. Grid with numbers:
```bash
make numbers_grid GRID_SIZE=6x6
```

4. Grid with adjacent mines:
```bash
make adjacent_grid GRID_SIZE=7x7
```

### Default Grid Sizes
- Single '1' tests: 5x3
- Multiple mines tests: 12x12
- General grid operations: 12x12

### Using run.sh Directly

You can also use the run.sh script directly:
```bash
./run.sh basic_grid 5x5 "[[0,0],[1,1]]"
./run.sh random_grid 8x8
./run.sh numbers_grid 6x6
./run.sh adjacent_grid 7x7
```

### Utility Commands

1. View available commands:
```bash
make help
```

2. Clean generated files:
```bash
make clean
```

## Grid Symbol Legend
- `*`: Mine
- `1`: Cell adjacent to one mine
- `.`: Empty cell
- Numbers (2-8): Count of adjacent mines (in numbers_grid and adjacent_grid)

## Notes
- Grid sizes are specified in ROWSxCOLS format (e.g., 5x3)
- Mine positions are specified as [[row1,col1],[row2,col2],...] (e.g., '[[0,0],[1,1]]')
- The default grid size is 12x12 unless specified otherwise
- All tests include visual grid output with -s flag enabled
