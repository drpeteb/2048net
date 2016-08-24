import sys, time
from abc import ABCMeta, abstractmethod
import numpy as np
from board import Board, Direction

USER_MOVES = {"w":Direction.up,
              "s":Direction.down,
              "a":Direction.left,
              "d":Direction.right}


class IPlayer(metaclass=ABCMeta):
    @abstractmethod
    def get_move(self, state, available):
        pass


class HumanPlayer(IPlayer):
    def get_move(self, state, score, available):
        for key in USER_MOVES:
            print("{}: {}".format(key, USER_MOVES[key].name))
        move = None
        while move not in available:
            key = None
            while (key not in USER_MOVES):
                sys.stdout.flush()
                key = input("Select a move: ")
            move = USER_MOVES[key]
        return move


class DumbComputerPlayer(IPlayer):

    def __init__(self, slow=False):
        self._slow = slow

    def get_move(self, state, score, available):
        if self._slow:
            time.sleep(1)
        idx = np.random.randint(len(available))
        return available[idx]


class Game:
    """
    Interface between the state, the players and the display
    """

    def __init__(self, player, display=False):
        self._display = display
        self._board = Board()
        if not isinstance(player, IPlayer):
            raise TypeError("Must supply an instance of IPlayer to play 2048.")
        self._player = player

    def play(self):

        # Add an extra initial tile
        self._board.add_random_tile()

        # Main game loop
        while not self._board.is_game_over():
            self._board.add_random_tile()
            if self._display:
                self._board.display()

            # See what moves are available
            available = self._board.available_directions()
            if not available:
                break

            # Get a move from the player and do it
            move = self._player.get_move(self._board.state(), self._board.score(), available)
            self._board.move(move)

        if self._display:
            print("GAME OVER! You scored: {}".format(self._board.score()))
        return self._board.score()
