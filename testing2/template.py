import tensorflow as tf
import numpy as np
import gym

# Define the maze environment
class MazeEnv(gym.Env):
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
        self.goal_state = (4, 4)
        self.current_state = self.start_state
        self.action_space = gym.spaces.Discrete(4)  # 4 possible actions: 0 = up, 1 = down, 2 = left, 3 = right
        self.observation_space = gym.spaces.Discrete(25)  # 25 possible states (5x5 maze)

    def reset(self):
        self.current_state = self.start_state
        return self.current_state

    def step(self, action):
        new_state = self._get_new_state(action) # MODIFIER HITMAN DIRECTEMENT
        reward = self._get_reward(new_state)
        done = self._is_done(new_state)
        self.current_state = new_state
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
        return state == self.goal_state

# Define the Q-Network
class QNetwork(tf.keras.Model):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.dense1 = tf.keras.layers.Dense(24, activation='relu')
        self.dense2 = tf.keras.layers.Dense(24, activation='relu')
        self.output_layer = tf.keras.layers.Dense(action_size, activation=None)

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.output_layer(x)

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.99
epsilon = 0.1
num_episodes = 1000

# Create the maze environment
env = MazeEnv()

# Create the Q-Network
model = QNetwork(env.observation_space.n, env.action_space.n)

# Define the loss function and optimizer
loss_fn = tf.keras.losses.MeanSquaredError()
optimizer = tf.keras.optimizers.Adam(learning_rate)

# Training loop
for episode in range(num_episodes):
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        # Epsilon-greedy exploration
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else:
            state_tensor = tf.convert_to_tensor(state, dtype=tf.float32)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_values = model(state_tensor)
            action = tf.argmax(action_values, axis=1).numpy()[0]

        next_state, reward, done, _ = env.step(action)
        total_reward += reward

        # Update Q-value
        next_state_tensor = tf.convert_to_tensor(next_state, dtype=tf.float32)
        next_state_tensor = tf.expand_dims(next_state_tensor, 0)
        target = reward + discount_factor * tf.reduce_max(model(next_state_tensor), axis=1)

        with tf.GradientTape() as tape:
            state_tensor = tf.convert_to_tensor(state, dtype=tf.float32)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_values = model(state_tensor)
            action_one_hot = tf.one_hot(action, env.action_space.n)
            q_value = tf.reduce_sum(tf.multiply(action_values, action_one_hot), axis=1)
            loss = loss_fn(target, q_value)

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        state = next_state

    print(f"Episode {episode+1}/{num_episodes}, Total Reward: {total_reward}")

# Testing the agent
state = env.reset()
done = False

while not done:
    state_tensor = tf.convert_to_tensor(state, dtype=tf.float32)
    state_tensor = tf.expand_dims(state_tensor, 0)
    action_values = model(state_tensor)
    action = tf.argmax(action_values, axis=1).numpy()[0]
    next_state, reward, done, _ = env.step(action)
    state = next_state

env.render()
