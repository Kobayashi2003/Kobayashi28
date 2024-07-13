import random
import copy
import numpy as np
import torch
from torch import nn, optim
from agent_dir.agent import Agent

from tqdm import tqdm
from collections import namedtuple 
    
Transition = namedtuple('Transition', ['state', 'action', 'reward', 'next_state', 'done'])

class QNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)


class ReplayBuffer:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = []

    def __len__(self):
        return len(self.buffer)

    def push(self, *transition):
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(transition)
        else:
            self.buffer.pop(0)
            self.buffer.append(transition)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def mean(self):
        return np.mean(self.buffer)

    def clean(self):
        self.buffer = []


class AgentDQN(Agent):
    def __init__(self, env, args):

        super(AgentDQN, self).__init__(env)

        for key, value in vars(args).items():
            setattr(self, key, value)

        self.input_size = env.observation_space.shape[0]
        self.output_size = env.action_space.n

    def init_game_setting(self):
        self.q_network = QNetwork(self.input_size, self.hidden_size, self.output_size)  # initialize q network
        self.target_network = copy.deepcopy(self.q_network)                             # initialize target network
        self.replay_buffer = ReplayBuffer(buffer_size=self.n_frames)                    # initialize replay buffer
        self.loss = nn.MSELoss()                                                        # initialize loss function
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.lr)            # initialize optimizer
        self.rewards_record = []
        self.rewards_buffer = ReplayBuffer(buffer_size=100)
        self.rewards_smmothed = []
        random.seed(self.seed)

    def train(self):
        if len(self.replay_buffer) < self.batch_size:
            return

        transitions = self.replay_buffer.sample(self.batch_size)
        batch = Transition(*zip(*transitions))

        state_batch = torch.FloatTensor(np.array(batch.state))
        action_batch = torch.LongTensor(batch.action)
        reward_batch = torch.FloatTensor(batch.reward)
        next_state_batch = torch.FloatTensor(np.array(batch.next_state))
        done_batch = torch.FloatTensor(batch.done)

        q_values = self.q_network(state_batch).gather(1, action_batch.unsqueeze(1)).squeeze(1)
        next_q_values = self.target_network(next_state_batch).max(1)[0]
        target_q_values = reward_batch + self.gamma * next_q_values * (1 - done_batch)

        loss = self.loss(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), self.grad_norm_clip)
        self.optimizer.step()
        
    def make_action(self, observation, test=True):
        """
        Return predicted action of your agent
        Input:observation
        Return:action
        """        
        state = torch.FloatTensor(observation).unsqueeze(0)

        if test:
            with torch.no_grad():
                return np.argmax(self.q_network(state).detach().numpy())
        elif random.random() <= self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.q_network(state).detach().numpy())

    def run(self):
        """
        Implement the interaction between agent and environment here
        """
        self.init_game_setting()

        with tqdm(total=self.episodes, position=0, leave=True) as pbar:
            for episode in range(self.episodes):
                state = self.env.reset()
                total_reward = 0
                done = False
                truncated = False

                while not done and not truncated:
                    action = self.make_action(state, test=False)
                    next_state, reward, done, truncated = self.env.step(action)
                    reward = np.clip(reward, -self.reward_clipping, self.reward_clipping)
                    self.replay_buffer.push(state, action, reward, next_state, done)
                    state = next_state
                    total_reward += reward

                    self.train()

                self.rewards_record.append(total_reward)

                self.rewards_buffer.push(total_reward)
                average_reward = self.rewards_buffer.mean()

                self.rewards_smmothed.append(average_reward)

                if episode % self.target_update_freq == 0:
                    self.target_network.load_state_dict(self.q_network.state_dict())

                if self.epsilon > self.epsilon_min:
                    self.epsilon *= self.epsilon_decay

                pbar.set_description(f"Episode: {episode}, Total Reward: {total_reward}, Average Reward: {average_reward}")
                pbar.update(1)

        self.env.close()