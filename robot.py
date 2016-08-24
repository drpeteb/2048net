import time
import numpy as np
from game import IPlayer

class AIPlayer(IPlayer):

    def __init__(self, slow=False):
        self._slow = slow
        self._state_history = []
        self._score_history = []

    def get_move(self, state, score, available):
        if self._slow:
            time.sleep(1)
        self._score_history.append(score)
        self._state_history.append(state)

        # Replace this with a model prediction
        idx = np.random.randint(len(available))
        return available[idx]