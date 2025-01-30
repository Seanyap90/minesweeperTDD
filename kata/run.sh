#!/bin/bash

# Get the directory where the script is located
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print section header
function print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

# Print grid helper function
function print_python_grid() {
    echo "from src.main_v2 import $1"
    echo "def print_grid(grid):"
    echo "    for row in grid:"
    echo "        print(' '.join(str(cell) for cell in row))"
    echo ""
    echo "grid = $1($2)"
    echo "print('Grid:')"
    echo "print_grid(grid)"
}

# Install dependencies
function install() {
    print_header "Installing Dependencies"
    python -m pip install --upgrade pip
    python -m pip install pytest
    python -m pip install --editable "$THIS_DIR/[dev]"
}

# Run all tests
function run_tests() {
    print_header "Running All Tests"
    python -m pytest tests/test_kata_v2.py -v -s
}

# Run basic tests
function run_basic_tests() {
    print_header "Running Basic Tests"
    python -m pytest tests/test_kata_v2.py -v -s -k "test_empty_grid or test_no_mines or test_add_mine"
}

# Run random placement tests
function run_random_tests() {
    print_header "Running Random Placement Tests"
    python -m pytest tests/test_kata_v2.py -v -s -k "test_mine_placement or test_multiple_mine_placement"
}

# Run ones placement tests
function run_ones_tests() {
    grid_size=${1:-"5x3"}  # Default size 5x3 for single/multiple ones tests
    print_header "Running Ones Placement Tests (Grid Size: $grid_size)"
    PYTHONPATH=. python -c "from tests.test_kata_v2 import test_single_one_adjacent_to_mine, test_multiple_ones_adjacent_to_mine; test_single_one_adjacent_to_mine('$grid_size'); test_multiple_ones_adjacent_to_mine('$grid_size')"
}

# Run complete tests
function run_ones_revised_tests() {
    grid_size=${1:-"12x6"}  # Default size 12x6 for multiple mines tests
    print_header "Running Complete Tests (Grid Size: $grid_size)"
    PYTHONPATH=. python -c "from tests.test_kata_v2 import test_multiple_mines_with_multiple_ones; test_multiple_mines_with_multiple_ones('$grid_size')"
}

# Run number calculation tests
function run_numbers_tests() {
    print_header "Running Number Calculation Tests"
    python -m pytest tests/test_kata_v2.py -v -s -k "test_calculate_adjacent_mine_numbers or test_multiple_mines_with_numbers or test_random_multiple_mines_with_numbers"
}

# Run adjacent mines tests
function run_adjacent_tests() {
    grid_size=${1:-"12x6"}  # Default size 12x6 for adjacent mines tests
    print_header "Running Adjacent Mines Tests (Grid Size: $grid_size)"
    PYTHONPATH=. python -c "from tests.test_kata_v2 import test_minesweeper_with_adjacent_mines; test_minesweeper_with_adjacent_mines('$grid_size')"
}

# Direct function executions from main_v2.py
function run_basic_grid() {
    grid_size=${1:-"10x6"}
    mines=${2:-"[[0,0],[1,1]]"}
    print_header "Running Basic Grid (Size: $grid_size, Mines: $mines)"
    rows=${grid_size%x*}
    cols=${grid_size#*x}
    PYTHONPATH=. python -c "$(print_python_grid "minesweeper_basic" "[$rows, $cols], $mines")"
}

function run_random_grid() {
    grid_size=${1:-"10x6"}
    print_header "Running Random Grid (Size: $grid_size)"
    rows=${grid_size%x*}
    cols=${grid_size#*x}
    PYTHONPATH=. python -c "$(print_python_grid "minesweeper_random" "[$rows, $cols]")"
}

function run_random_grid_revised() {
    grid_size=${1:-"10x6"}
    print_header "Running Random Grid (Revised) (Size: $grid_size)"
    rows=${grid_size%x*}
    cols=${grid_size#*x}
    PYTHONPATH=. python -c "$(print_python_grid "minesweeper_random_revised" "[$rows, $cols]")"
}

function run_numbers_grid() {
    grid_size=${1:-"10x6"}
    print_header "Running Numbers Grid (Size: $grid_size)"
    rows=${grid_size%x*}
    cols=${grid_size#*x}
    PYTHONPATH=. python -c "$(print_python_grid "minesweeper_with_numbers" "[$rows, $cols]")"
}

function run_adjacent_grid() {
    grid_size=${1:-"10x6"}
    print_header "Running Adjacent Grid (Size: $grid_size)"
    rows=${grid_size%x*}
    cols=${grid_size#*x}
    PYTHONPATH=. python -c "$(print_python_grid "minesweeper_with_adjacent_mines" "[$rows, $cols]")"
}

# Clean generated files
function clean() {
    print_header "Cleaning Generated Files"
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    find . -type f -name ".coverage" -delete
    find . -type d -name "*.egg-info" -exec rm -r {} +
    find . -type d -name "*.egg" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +
    find . -type d -name ".eggs" -exec rm -r {} +
    find . -type d -name "build" -exec rm -r {} +
    find . -type d -name "dist" -exec rm -r {} +
    rm -rf venv/
}

# Print help message
function print_help() {
    print_header "Minesweeper Test Runner Help"
    echo "Available commands:"
    echo "Test Commands:"
    echo "  install                     - Install dependencies"
    echo "  test                        - Run all tests"
    echo "  basic                       - Run basic minesweeper tests"
    echo "  random                      - Run random mine placement tests"
    echo "  ones [ROWSxCOLS]           - Run tests for '1's placement (default: 5x3)"
    echo "  revised [ROWSxCOLS]       - Run revisedtests for '1's placement (default: 12x6)"
    echo "  numbers                     - Run number calculation tests"
    echo "  adjacent [ROWSxCOLS]       - Run adjacent mines tests (default: 12x6)"
    echo ""
    echo "Direct Function Commands:"
    echo "  basic_grid [ROWSxCOLS] [MINES]  - Create basic grid (default: 10x6, [[0,0],[1,1]])"
    echo "  random_grid [ROWSxCOLS]         - Create random grid (default: 10x6)"
    echo "  random_grid_revised [ROWSxCOLS] - Create random grid with revised functions (default: 10x6)"
    echo "  numbers_grid [ROWSxCOLS]        - Create grid with numbers (default: 10x6)"
    echo "  adjacent_grid [ROWSxCOLS]       - Create grid with adjacent mines (default: 10x6)"
    echo ""
    echo "Utility Commands:"
    echo "  clean                       - Clean generated files"
    echo "  help                        - Show this help message"
    echo ""
    echo "Grid size format: ROWSxCOLS (e.g., 5x3)"
    echo "Mines format: [[row1,col1],[row2,col2],...] (e.g., '[[0,0],[1,1]]')"
}

# Main command processing
case "$1" in
    "install")
        install
        ;;
    "test")
        run_tests
        ;;
    "basic")
        run_basic_tests
        ;;
    "random")
        run_random_tests
        ;;
    "ones")
        run_ones_tests "$2"
        ;;
    "revised")
        run_ones_revised_tests "$2"
        ;;
    "numbers")
        run_numbers_tests
        ;;
    "adjacent")
        run_adjacent_tests "$2"
        ;;
    "basic_grid")
        run_basic_grid "$2" "$3"
        ;;
    "random_grid")
        run_random_grid "$2"
        ;;
    "random_grid_revised")
        run_random_grid_revised "$2"
        ;;
    "numbers_grid")
        run_numbers_grid "$2"
        ;;
    "adjacent_grid")
        run_adjacent_grid "$2"
        ;;
    "clean")
        clean
        ;;
    "help")
        print_help
        ;;
    *)
        echo "Unknown command: $1"
        print_help
        exit 1
        ;;
esac