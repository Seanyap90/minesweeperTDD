.PHONY: all test clean basic random complete numbers adjacent help install \
        basic_grid random_grid random_complete_grid numbers_grid adjacent_grid

# Default grid sizes for different test types
SINGLE_ONE_GRID_SIZE ?= 5x3
MULTIPLE_MINES_GRID_SIZE ?= 12x12
GRID_SIZE ?= 12x12
MINES ?= "[[0,0],[1,1]]"

install:
	bash run.sh install

test:
	bash run.sh test

basic:
	bash run.sh basic

random:
	bash run.sh random

ones:
	bash run.sh ones $(SINGLE_ONE_GRID_SIZE)

revised:
	bash run.sh revised $(MULTIPLE_MINES_GRID_SIZE)

numbers:
	bash run.sh numbers

adjacent:
	bash run.sh adjacent $(MULTIPLE_MINES_GRID_SIZE)

# Direct function targets from main_v2.py
basic_grid:
	bash run.sh basic_grid $(GRID_SIZE) $(MINES)

random_grid:
	bash run.sh random_grid $(GRID_SIZE)

random_grid_revised:
	bash run.sh random_grid_revised $(GRID_SIZE)

numbers_grid:
	bash run.sh numbers_grid $(GRID_SIZE)

adjacent_grid:
	bash run.sh adjacent_grid $(GRID_SIZE)

clean:
	bash run.sh clean

help:
	bash run.sh help