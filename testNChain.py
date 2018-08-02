import gym
from learningAgents import QLearningAgent, RandomAgent
from valueIterationAgents import NChainVIAgent
from MDP import NChainMDP

# ACTIONS: 0 forward, 1 backwards

print 'Testing Q-Learning...\n'

env = gym.make('NChain-v0')
training_iterations = 1
testing_iterations = 1000

# hyperparameters tuned for NChain
epsilon = 1
gamma = 0.9
alpha = 0.1

# this agent will default to going backwards (we know optimal policy is forward)
ql_agent = QLearningAgent(env, training_iterations, testing_iterations, \
                          epsilon, gamma, alpha)

print 'Training with {} iterations...'.format(training_iterations)

ql_agent.train_agent()
ql_agent.test_nchain()

print 'Testing Random Solution...\n'

random_agent = RandomAgent(env, testing_iterations)
random_agent.test_nchain()

print 'Testing Value Iteration...\n'

# env has a chain of length 5 and probability of executing desired action of 0.8
p, n = 0.8, 5
mdp = NChainMDP(p, n)
valueAgent = NChainVIAgent(mdp, testing_iterations)
valueAgent.test_agent(env, n)








