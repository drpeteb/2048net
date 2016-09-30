import time
import numpy as np
import tensorflow as tf
from board import Direction
from game import IPlayer

EPS = 0.0001
DISCOUNT = 0.9
HIDDEN_NODES = 32
LEARNING_RATE = 0.01

def create_network(sess):
    state = tf.placeholder(tf.float32, shape=[None, 16])
    reward_action = tf.placeholder(tf.float32, shape=[None, 4])

    W1 = tf.Variable(tf.truncated_normal([16, HIDDEN_NODES], stddev=0.1))
    b1 = tf.Variable(tf.constant(0.1, shape=[HIDDEN_NODES]))
    nl1 = tf.nn.elu(tf.matmul(state, W1) + b1)

    W2 = tf.Variable(tf.truncated_normal([HIDDEN_NODES, 4], stddev=0.1))
    b2 = tf.Variable(tf.constant(0.1, shape=[4]))

    confident_action_prob = tf.nn.softmax(tf.matmul(nl1, W2) + b2)
    action_prob = EPS * tf.constant(0.25, shape=[4]) + (1 - EPS) * confident_action_prob

    params = (W1, b1, W2, b2)

    loss = tf.reduce_mean(-tf.reduce_sum(reward_action * tf.log(action_prob), reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss)

    sess.run(tf.initialize_all_variables())
    return state, reward_action, action_prob, train_step, params



class AIPlayer(IPlayer):

    def __init__(self, slow=False):
        self._slow = slow

        self._state_history = []
        self._action_history = []
        self._score_history = []

        self._state_buffer = []
        self._action_buffer = []
        self._reward_buffer = []

        self.sess = tf.InteractiveSession()
        print("Constructing Net")
        self.state, self.reward_action, self.action_prob, self.train_step, self.params = create_network(self.sess)


    def get_move(self, state, score, available):
        if self._slow:
            time.sleep(1)
        self._score_history.append(score)
        self._state_history.append(state)

        prob = self.sess.run(self.action_prob, feed_dict={self.state: state[np.newaxis,:]})

        mask = np.zeros((4), dtype=bool)
        for a in available:
            mask[a] = True
        masked_prob = mask * prob.flatten()
        masked_prob /= np.sum(masked_prob)
        idx = np.random.choice(4, p=masked_prob)

        action = np.zeros((4), dtype=bool)
        action[idx] = True
        self._action_history.append(action)

        return Direction(idx)


    def game_over(self, final_score):
        self._state_buffer.extend(self._state_history)
        self._state_history = []

        self._action_buffer.extend(self._action_history)
        self._action_history = []

        num_moves = len(self._score_history)
        reward = np.zeros(num_moves)
        reward[num_moves-1] = final_score - self._score_history[num_moves-1]
        for ii in reversed(range(num_moves-1)):
            reward[ii] = DISCOUNT * reward[ii+1] + \
                self._score_history[ii+1] - self._score_history[ii]
        self._reward_buffer.extend(reward)
        self._score_history = []

    def training_iteration(self):
        action = np.array(self._action_buffer)
        state = np.array(self._state_buffer, dtype=float)

        reward = np.array(self._reward_buffer)
        reward -= np.mean(reward)
        reward /= np.std(reward)

        reward_action = reward[:,np.newaxis] * action

        self.sess.run(self.train_step, feed_dict={
            self.state: state,
            self.reward_action: reward_action,
        })

        self._state_buffer = []
        self._action_buffer = []
        self._reward_buffer = []
