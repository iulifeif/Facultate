import os
from collections import deque

import gym
import keras
from keras import layers
import numpy as np
import matplotlib.pyplot as plt
import random

from tensorflow.python.feature_column.feature_column import InputLayer
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, Conv2D
from tensorflow.python.keras.models import model_from_json
from tensorflow.python.keras.optimizer_v2.adam import Adam

MOVE_DOWN = 2
MOVE_UP = 3
STAY = 0
LR = 0.1
BUFFER_SIZE = 50000
EXPLORATION_RATE = 0.99
DECAY = 0.8
BATCH_SIZE = 400
MAX_TRAINING_ITERATIONS = 90000


class DQLN:
    def __init__(self, lr):
        self.lr = lr
        self.memory = deque(maxlen=BUFFER_SIZE)
        if os.path.exists("model.json"):
            with open("model.json", "r") as json_file:
                self.model = model_from_json(json_file.read())
            self.model.load_weights("model.h5")
        else:
            self.model = Sequential()
            self.model.add(InputLayer(input_shape=(80, 80, 1)))
            self.model.add(Conv2D(16, 8, 4, activation="relu"))
            self.model.add(Conv2D(32, 4, 2, activation="relu"))
            self.model.add(Flatten())
            self.model.add(Dense(units=200, activation="relu"))
            self.model.add(Dense(units=50, activation="relu"))
            self.model.add(Dense(3, activation="softmax"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LR))
        self.model.summary()
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
        inputs = []
        labels = []
        next_states = []
        states = []
        for state, _, _, state_next, _ in batch:
            next_states.append(state_next[0])
            states.append(state[0])
        q_predictions = self.model.predict(np.array(next_states))
        q_values_predictions = self.model.predict(np.array(states))
        for index in range(len(batch)):
            state, action, reward, _, terminal = batch[index]
            state_next = q_predictions[index]
            q_update = reward
            if not terminal:
                q_update = (reward + 0.9 * np.amax(state_next))
            q_values = q_values_predictions[index]
            q_values[action] = q_update
            inputs.append(state)
            labels.append(q_values)
        self.model.fit(np.array(inputs), np.array(labels), verbose=1)


def prepro(I):
    # “”” prepro 210 x160x3 frame into 6400(80 x80) 1 D float vector “””
    I = I[35:195]  # crop
    I = I[::2, ::2, 0]  # downsample by factor of 2
    I[I == 144] = 0  # erase background (background type 1)
    I[I == 109] = 0  # erase background (background type 2)
    I[I != 0] = 1  # everything else (paddles, ball) just set to 1
    x = I.astype(np.float).ravel()
    return np.array(np.split(x, 80)).reshape(1, 80, 80, 1)


if __name__ == '__main__':
    env = gym.make('Pong-v0')
    env.reset()
    dqln = DQLN(LR)
    observation, reward, done, info = env.step(0)
    iterations = 0
    dry_run = False
    if dry_run:
        EXPLORATION_RATE = 0
    while iterations < MAX_TRAINING_ITERATIONS:
        obs_preprocessed = prepro(observation)
        choose_move = dqln.move(obs_preprocessed)
        observation, reward, done, info = env.step(dqln.possible_actions[choose_move])
        if not dry_run:
            dqln.remember(obs_preprocessed, choose_move, reward, prepro(observation), done)
        if dry_run or not iterations % 5:
            env.render()
        if done == True:
            env.reset()
            if not dry_run:
                dqln.train()
            EXPLORATION_RATE *= DECAY
            iterations += 1
            dqln.model.save_weights("model.h5")
            with open("model.json", "w") as json_file:
                json_file.write(dqln.model.to_json())
            print("eps:", EXPLORATION_RATE, "epoch:", iterations, "memory:", len(dqln.memory))
    env.close()
