from hitman_simplified import *

import tensorflow as tf
import numpy as np
import gym

# Define the maze environment
class MazeEnv(gym.Env, HitmanReferee):
    def __init__(self):
        # REPLACE WITH HIDDEN MAZE STATE AND ACTUAL MAZE STATE
        self.maze = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ])  # 0 represents an empty cell, 1 represents a wall
        self.start_state = (0, 0) # CHANGE TO PARAMETER
        self.current_state = self.start_state
        self.action_space = gym.spaces.Discrete(4)  # 4 possible actions: 0 = up, 1 = down, 2 = left, 3 = right
        self.observation_space = gym.spaces.Discrete(25)  # 25 possible states (5x5 maze)

    def reset(self): # DELETE, CREATE NEW ENV INSTEAD
        self.current_state = self.start_state
        return self.current_state

    def step(self, action):
        new_state = self._get_new_state(action) # Modifier HitmanReferee directement
        # renvoie current state
        reward = self._get_reward(new_state) # Fonctions customisées simples
        done = self._is_done(new_state)
        self.current_state = new_state # mise a jour non necessaire
        return new_state, reward, done, {}

    def _get_new_state(self, action):
        x, y = self.current_state
        if action == 0 and x > 0 and self.maze[x-1, y] == 0:  # Up
            return x - 1, y
        elif action == 1 and x < 4 and self.maze[x+1, y] == 0:  # Down
            return x + 1, y
        elif action == 2 and y > 0 and self.maze[x, y-1] == 0:  # Left
            return x, y - 1
        elif action == 3 and y < 4 and self.maze[x, y+1] == 0:  # Right
            return x, y + 1
        else:
            return x, y

    def _get_reward(self, state):
        if state == self.goal_state:
            return 10
        elif self.maze[state] == 1:  # Hit a wall
            return -5
        else:
            return -1

    def _is_done(self, state):
        return state == self.goal_state # TEST IF FULLY DISCOVERED