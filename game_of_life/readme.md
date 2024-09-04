#######################################################################################################################

# 1. Introduction

This is a simple project to re-create my own personal version of the game of life. The game of life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

# 2. Rules

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed—births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick (in other words, each generation is a pure function of the preceding one). The rules continue to be applied repeatedly to create further generations.

# 3. How to run

To run the game of life, simply run the following command in the terminal:

```bash
python game_of_life.py
```

# 3.5 COMMANDS

- Space: Pause/Resume the simulation
- Up/Down arrows: Increase/Decrease simulation speed
- R: Reset to an empty grid
- G: Reset to the Gosper Glider
- 1/2/3: Change brush size
- Left click/drag: Add cells
- Right click: Remove cells
- L: Place a glider at the cursor position
- B: Place a blinker at the cursor position
- P: Place a pulsar at the cursor position
- M: Randomize the grid

# 4. Dependencies

This project requires the following dependencies:

- numpy
- matplotlib

To install these dependencies, run the following command in the terminal:

```bash
pip install numpy matplotlib
```

# 5. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# 6. Acknowledgements

- [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [Nature of Code](https://natureofcode.com/book/chapter-7-cellular-automata/)
- [Python Programming](https://pythonprogramming.net/game-life-python-plays-tetris-pygame/)
- [Geeks for Geeks](https://www.geeksforgeeks.org/conways-game-life-python-implementation/)
- [Stack Overflow](https://stackoverflow.com/questions/47950131/conways-game-of-life-python)
- [GitHub] https://github.com/matheusgomes28/pygame-life/commits?author=matheusgomes28
