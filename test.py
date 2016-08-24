import numpy as np
from game import Game, HumanPlayer, DumbComputerPlayer
from robot import AIPlayer

#p = HumanPlayer()
#p = DumbComputerPlayer(slow=True)
p = AIPlayer(slow=False)

g = Game(p, display=True)
g.play()

print(p._score_history)
for state in p._state_history:
    print(state)