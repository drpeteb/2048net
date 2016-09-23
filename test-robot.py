import numpy as np
import matplotlib.pyplot as plt
from game import Game
from robot import AIPlayer

NUM_IT = 200
NUM_IN_BATCH = 10

netty = AIPlayer(slow=False)
scores = []
batch_averages = []

for nn in range(NUM_IT):
    print(nn)
    this_batch = []
    for bb in range(NUM_IN_BATCH):
        g = Game(netty, display=False)
        final_score = g.play()
        scores.append(final_score)
        this_batch.append(final_score)
        netty.game_over(final_score)
    batch_averages.append(np.mean(np.array(this_batch)))
    netty.training_iteration()

fig = plt.figure()
ax = fig.add_subplot(2,1,1)
ax.plot(np.array(scores), 'k')
ax = fig.add_subplot(2,1,2)
ax.plot(np.array(batch_averages), 'k')
plt.show()

g._board.display()

#import time
#start_time = time.time()
#end_time = time.time()
#print(end_time - start_time)
