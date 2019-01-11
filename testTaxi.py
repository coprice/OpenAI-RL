import gym
from learningAgents import QLearningAgent, TaxiQLAgent, RandomAgent


# ACTIONS: 3 LEFT, 2 RIGHT, 1 UP, 0 DOWN


env = gym.make('Taxi-v2')
training_iterations = 2000
testing_iterations = 1000

# hyperparameters tuned for taxi
epsilon = 0.15
gamma = 0.9
alpha = 0.1

print 'Testing Q-Learning...\n'

ql_agent = QLearningAgent(env, training_iterations, testing_iterations, epsilon, gamma, alpha)

print 'Training with {} iterations...'.format(training_iterations)

ql_agent.train_agent()
ql_agent.test_taxi()

print 'Testing Incentivized Q-Learning...\n'

tql_agent = TaxiQLAgent(env, training_iterations, testing_iterations, epsilon, gamma, alpha)

print 'Training with {} iterations...'.format(training_iterations)

tql_agent.train_agent()
tql_agent.test_taxi()

print 'Testing Random Agent...\n'

random_agent = RandomAgent(env, testing_iterations)
random_agent.test_taxi()
