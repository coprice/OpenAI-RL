import gym
from learningAgents import QLearningAgent, FrozenLakeQLAgent, RandomAgent
from MDP import FrozenLakeMDP
from valueIterationAgents import FrozenLakeVIAgent

# Actions: left (0), down (1), right (2), up (3)

"""
FrozenLake 4x4 tests
"""

print 'Testing FrozenLake 4x4 Grid...\n'

print 'Testing Q-Learning...\n'

env = gym.make('FrozenLake-v0')
training_iterations = 2000
testing_iterations = 1000
holes = {(2,2), (4,2), (4,3), (1,4)}

# hyperparameters tuned for frozen lake
epsilon = 0.2
gamma = 0.99
alpha = 0.1

ql_agent = QLearningAgent(env, training_iterations, testing_iterations, \
                          epsilon, gamma, alpha)

print 'Training with {} iterations...'.format(training_iterations)

ql_agent.train_agent()
ql_agent.test_frozen_lake(4)


print 'Testing Incentivized Q-Learning...\n'

flql_agent = FrozenLakeQLAgent(env, training_iterations, testing_iterations, \
                               epsilon, gamma, alpha)
flql_agent.train_agent(4, holes)
flql_agent.test_frozen_lake(4)

print 'Testing Value Iteration...\n'

mdp = FrozenLakeMDP(4, holes)
valueAgent = FrozenLakeVIAgent(mdp, testing_iterations)
valueAgent.test_agent(env, 4)

print 'Testing Random Solution...\n'

random_agent = RandomAgent(env, testing_iterations)
random_agent.test_frozen_lake(4)

"""
FrozenLake 8x8 tests
"""

print 'Testing FrozenLake 8x8 Grid...\n'

print 'Testing Q Learning...\n'

env = gym.make('FrozenLake8x8-v0')
holes = {(4,3),(6,4),(4,5),(2,6),(3,6),(7,6),(2,7),(5,7),(7,7),(4,8)}

ql_agent = QLearningAgent(env, training_iterations, testing_iterations, \
                           epsilon, gamma, alpha)

print 'Training with {} iterations...'.format(training_iterations)

ql_agent.train_agent()
ql_agent.test_frozen_lake(8)

print 'Testing Incentivized Q-Learning...\n'

flql_agent = FrozenLakeQLAgent(env, training_iterations, testing_iterations, \
                               epsilon, gamma, alpha)
flql_agent.train_agent(8, holes)
flql_agent.test_frozen_lake(8)

print 'Testing Value Iteration...\n'

mdp = FrozenLakeMDP(8, holes)
valueAgent = FrozenLakeVIAgent(mdp, testing_iterations)
valueAgent.test_agent(env, 8)

print 'Testing Random Solution...\n'

random_agent = RandomAgent(env, testing_iterations)
random_agent.test_frozen_lake(8)
