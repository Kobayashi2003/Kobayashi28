import argparse
import gym
from argument import dqn_arguments, pg_arguments

import matplotlib.pyplot as plt

def parse():
    parser = argparse.ArgumentParser(description="SYSU_RL_HW2")
    parser.add_argument('--train_pg', default=False, type=bool, help='whether train policy gradient')
    parser.add_argument('--train_dqn', default=False, type=bool, help='whether train DQN')

    parser = dqn_arguments(parser)
    args = parser.parse_args()
    args.train_dqn = True

    return args

def run(args):
    if args.train_pg:
        env_name = args.env_name
        env = gym.make(env_name)
        from agent_dir.agent_pg import AgentPG
        agent = AgentPG(env, args)
        agent.run()

    if args.train_dqn:
        env_name = args.env_name
        env = gym.make(env_name)
        from agent_dir.agent_dqn import AgentDQN
        agent = AgentDQN(env, args)
        agent.run()

    rewards = agent.rewards_smmothed

    plt.plot(rewards)
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.title(f'DQN Training Reward Curve ({args.env_name})')
    plt.style.use('seaborn-darkgrid')
    plt.show()

if __name__ == '__main__':
    args = parse()
    run(args)
