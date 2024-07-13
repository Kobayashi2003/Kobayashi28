def dqn_arguments(parser):
    """
    Add your arguments here if needed. The TAs will run test.py to load
    your default arguments.

    For example:
        parser.add_argument('--batch_size', type=int, default=32, help='batch size for training')
        parser.add_argument('--learning_rate', type=float, default=0.01, help='learning rate for training')
    """
    parser.add_argument('--env_name', default="CartPole-v0", help='environment name')

    parser.add_argument("--seed", default=11037, type=int, help='random seed')
    parser.add_argument("--hidden_size", default=16, type=int, help='hidden layer size')

    parser.add_argument("--test", default=False, type=bool, help='set to True if you are in test mode')
    parser.add_argument("--use_cuda", default=True, type=bool, help='set to True if you want to use GPU')
    parser.add_argument("--n_frames", default=int(30000), type=int, help='the number of frames you want to store in the buffer')

    parser.add_argument("--episodes", default=300, type=int, help='the number of episodes to train the agent')
    parser.add_argument("--batch_size", default=128, type=int, help='the number of transitions sampled from replay buffer')
    parser.add_argument("--lr", default=0.02, type=float, help='learning rate')
    parser.add_argument("--gamma", default=0.99, type=float, help='discount factor')
    parser.add_argument("--grad_norm_clip", default=10, type=float, help='gradient norm clipping')
    parser.add_argument("--reward_clipping", default=1.0, type=float, help='reward clipping')
    parser.add_argument("--epsilon", default=1.0, type=float, help='the probability for exploration')
    parser.add_argument("--epsilon_min", default=0.01, type=float, help='the minimum value of epsilon')
    parser.add_argument("--epsilon_decay", default=0.995, type=float, help='the decay factor for updating epsilon')

    parser.add_argument("--target_update_freq", default=10, type=int, help='the frequency for updating the target network')

    return parser


def pg_arguments(parser):
    """
    Add your arguments here if needed. The TAs will run test.py to load
    your default arguments.

    For example:
        parser.add_argument('--batch_size', type=int, default=32, help='batch size for training')
        parser.add_argument('--learning_rate', type=float, default=0.01, help='learning rate for training')
    """
    parser.add_argument('--env_name', default="CartPole-v0", help='environment name')

    parser.add_argument("--seed", default=11037, type=int)
    parser.add_argument("--hidden_size", default=16, type=int)
    parser.add_argument("--lr", default=0.02, type=float)
    parser.add_argument("--gamma", default=0.99, type=float)
    parser.add_argument("--grad_norm_clip", default=10, type=float)

    parser.add_argument("--test", default=False, type=bool)
    parser.add_argument("--use_cuda", default=True, type=bool)
    parser.add_argument("--n_frames", default=int(30000), type=int)

    return parser
