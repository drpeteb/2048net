from board import Board, Direction

USER_MOVES = {"w":Direction.up,
              "s":Direction.down,
              "a":Direction.left,
              "d":Direction.right}

class Game:
    """
    Interface between the state, the players and the display
    """

    def __init__(self):
        self._board = Board()

    def play(self):

        # Add an extra initial tile
        self._board.add_random_tile()

        # Main game loop
        while not self._board.is_game_over():
            self._board.add_random_tile()
            self._board.display()
            for key in USER_MOVES:
                print("{}: {}".format(key, USER_MOVES[key].name))

            # See what moves are available
            available = self._board.available_directions()
            if not available:
                break

            # Get and validate user input
            move = None
            while move not in available:
                key = None
                while (key not in USER_MOVES):
                    key = input("Select a move: ")
                move = USER_MOVES[key]
            self._board.move(move)

        print("GAME OVER! You scored: {}".format(self._board.score()))
        return self._board.score()
