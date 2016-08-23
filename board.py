import numpy as np
from enum import Enum

# Global variables
GRID_SIZE = 4
PROB2 = 0.9

class Direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3

class Board:
    """
    Current state of the game and methods to manipulate it
    """

    def __init__(self, grid=None):
        if grid is None:
            self._grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype='int')
        else:
            self._grid = grid

    def copy(self):
        return Board(self._grid.copy())

    def display(self):
        print("-------")
        for ii in range(GRID_SIZE):
            print(" ".join(["{0: >5}".format(2 ** entry) if (entry > 0) else "    ." for entry in self._grid[ii, :]]))
        print("-------")
        print("Current score: {}".format(self.score()))

    def state(self):
        return self._grid.flatten()

    def score(self):
        return np.sum((2 ** self._grid) * (self._grid > 0))

    def is_game_over(self):
        return (np.sum(self._grid == 0) == 0)

    def add_random_tile(self):
        num_empty = np.sum(self._grid == 0)
        zero_pos = np.where(self._grid == 0)
        idx = np.random.randint(num_empty)
        val = 1 if (np.random.rand() < PROB2) else 2
        self._grid[zero_pos[0][idx], zero_pos[1][idx]] = val

    def available_directions(self):
        available = []
        for direction in Direction:
            copy = self.copy()
            copy.move(direction)
            if not np.all(self._grid == copy._grid):
                available.append(direction)
        return available

    def move(self, direction):
        """
        Loop through the squares, moving 'upstream', and see if a tile should
        move into it.
        """

        if direction == Direction.up:
            for ii in range(GRID_SIZE-1):
                for jj in range(GRID_SIZE):
                    for kk in range(ii+1,GRID_SIZE):
                        if self._grid[kk, jj] != 0:
                            if self._grid[ii, jj] == 0:
                                self._grid[ii, jj] = self._grid[kk, jj]
                                self._grid[kk, jj] = 0
                            elif self._grid[ii, jj] == self._grid[kk, jj]:
                                self._grid[ii, jj] += 1
                                self._grid[kk, jj] = 0
                                break
                            else:
                                break

        elif direction == Direction.down:
            for ii in reversed(range(1,GRID_SIZE)):
                for jj in range(GRID_SIZE):
                    for kk in reversed(range(ii)):
                        if self._grid[kk, jj] != 0:
                            if self._grid[ii, jj] == 0:
                                self._grid[ii, jj] = self._grid[kk, jj]
                                self._grid[kk, jj] = 0
                            elif self._grid[ii, jj] == self._grid[kk, jj]:
                                self._grid[ii, jj] += 1
                                self._grid[kk, jj] = 0
                                break
                            else:
                                break

        elif direction == Direction.left:
            for jj in range(GRID_SIZE-1):
                for ii in range(GRID_SIZE):
                    for kk in range(jj+1,GRID_SIZE):
                        if self._grid[ii, kk] != 0:
                            if self._grid[ii, jj] == 0:
                                self._grid[ii, jj] = self._grid[ii, kk]
                                self._grid[ii, kk] = 0
                            elif self._grid[ii, jj] == self._grid[ii, kk]:
                                self._grid[ii, jj] += 1
                                self._grid[ii, kk] = 0
                                break
                            else:
                                break

        elif direction == Direction.right:
            for jj in reversed(range(1,GRID_SIZE)):
                for ii in range(GRID_SIZE):
                    for kk in reversed(range(jj)):
                        if self._grid[ii, kk] != 0:
                            if self._grid[ii, jj] == 0:
                                self._grid[ii, jj] = self._grid[ii, kk]
                                self._grid[ii, kk] = 0
                            elif self._grid[ii, jj] == self._grid[ii, kk]:
                                self._grid[ii, jj] += 1
                                self._grid[ii, kk] = 0
                                break
                            else:
                                break

        else:
            raise RuntimeError("Unrecognised move")
