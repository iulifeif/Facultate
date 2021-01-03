from collections import deque

import gym
import keras
from keras import layers
import numpy as np
import matplotlib.pyplot as plt
import random

from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.python.keras.optimizer_v2.adam import Adam

MOVE_DOWN = 2
MOVE_UP = 3
STAY = 0
LR = 0.1
BUFFER_SIZE = 50000
EXPLORATION_RATE = 0.99
DECAY = 0.88
BATCH_SIZE = 100
MAX_TRAINING_ITERATIONS = 90000


class DQLN:
    def __init__(self, lr):
        self.lr = lr
        self.memory = deque(maxlen=BUFFER_SIZE)
        self.model = Sequential()
        self.model.add(Dense(units=200, input_dim=80*80, activation="relu"))
        self.model.add(Dense(3, activation="softmax"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LR))
        self.possible_actions = [MOVE_UP, MOVE_DOWN, STAY]

    def move(self, img_input):
        if np.random.rand() < EXPLORATION_RATE:
            return random.choice([0, 1, 2])
        else:
            q = self.model.predict(img_input)[0]
            return np.argmax(q)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        batch[-1] = self.memory[-1]
        if BATCH_SIZE > 1:
            batch[-2] = self.memory[-1]
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                # q_update = (reward + LR * np.amax(self.model.predict(state_next)[0]))
                q_update = (reward + LR)
            q_values = self.model.predict(state)
            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)

def prepro(I):
    # “”” prepro 210 x160x3 frame into 6400(80 x80) 1 D float vector “””
    I = I[35:195]  # crop
    I = I[::2, ::2, 0]  # downsample by factor of 2
    I[I == 144] = 0  # erase background (background type 1)
    I[I == 109] = 0  # erase background (background type 2)
    I[I != 0] = 1  # everything else (paddles, ball) just set to 1
    x = I.astype(np.float).ravel()
    return np.expand_dims(x, axis=1).T


if __name__ == '__main__':
    env = gym.make('Pong-v0')
    env.reset()
    dqln = DQLN(LR)
    observation, reward, done, info = env.step(0)
    iterations = 0
    while iterations < MAX_TRAINING_ITERATIONS:
        obs_preprocessed = prepro(observation)
        choose_move = dqln.move(obs_preprocessed)
        observation, reward, done, info = env.step(dqln.possible_actions[choose_move])
        dqln.remember(obs_preprocessed, choose_move, reward, prepro(observation), done)
        # if not iterations % 100:
            # env.render()
        if done == True:
            env.reset()
            dqln.train()
            EXPLORATION_RATE *= DECAY
            iterations += 1
            dqln.model.save("nn-model")
    env.close()
