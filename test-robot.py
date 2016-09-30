import time
import numpy as np
import matplotlib.pyplot as plt
from game import Game
from robot import AIPlayer

NUM_IT = 1024
NUM_IN_BATCH = 16

netty = AIPlayer(slow=False)
scores = []
batch_averages = []
best_game = None
best_score = 0
start_time = time.time()

for nn in range(NUM_IT):
    this_batch = []
    for bb in range(NUM_IN_BATCH):
        g = Game(netty, display=False)
        final_score = g.play()
        scores.append(final_score)
        this_batch.append(final_score)
        netty.game_over(final_score)
        if final_score > best_score:
            best_score = final_score
            best_game = g
    ba = np.mean(np.array(this_batch))
    batch_averages.append(ba)
    print("It {:5d}: average score = {:6.1f}, time since started = {:6.1f}s".format(nn+1, ba, time.time()-start_time))
    netty.training_iteration()

fig = plt.figure()
ax = fig.add_subplot(2,1,1)
ax.plot(np.array(scores), 'k')
ax = fig.add_subplot(2,1,2)
ax.plot(np.array(batch_averages), 'k')
plt.show()

print("Best results:")
best_game._board.display()
