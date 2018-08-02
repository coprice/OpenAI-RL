import gym
import random
import utils
from searchTaxi import *

"""
General class to inherit for other learning algo classes
"""
class LearningAgent:
    def __init__(self, env, testing_iterations):
        self.env = env
        self.testing = testing_iterations

    def getPolicy(self, obs):
        pass

    def train_agent(self):
        pass

    def test_frozen_lake(self, maxValue):
        rewards = 0
        for _ in range(self.testing):
            obs, done = self.env.reset(), False
            while not done:
                action = self.getPolicy(obs)
                obs, reward, done, info = self.env.step(action)
                rewards += reward
        print "Percent success rate was {}%\n".format(rewards*100.0/self.testing)
        policy = []
        for i in range(maxValue*maxValue):
            policy.append(self.getPolicy(i))
        print "Learned Policy: {}\n".format(policy)

    def test_taxi(self):
        passed = 0
        for _ in range(self.testing):
            obs, done, actions = self.env.reset(), False, []
            optimalActions = solveTaxi(obs)
            while not done:
                action = self.getPolicy(obs)
                actions.append(action)
                obs, _, done, _ = self.env.step(action)
                if len(actions) > len(optimalActions):
                    break
            if done:
                if len(actions) == len(optimalActions):
                    passed += 1
                if len(actions) < len(optimalActions):
                    print "This is impossible!"
        print 'Optimal performance rate was {}%\n'.format(passed*100.0/self.testing)

    def test_nchain(self):
        rewards, policy = 0, []
        for i in range(5):
            policy.append(self.getPolicy(i))
        for _ in range(self.testing):
            obs, done = self.env.reset(), False
            while not done:
                action = policy[obs]
                obs, reward, done, _ = self.env.step(action)
                rewards += reward
        print 'Average rewards gained:', rewards/float(self.testing)
        print 'Learned Policy:', policy
        print 'Optimal Policy: {}\n'.format([0]*5)

"""
Random Agent to compare with
"""
class RandomAgent(LearningAgent):
    def __init__(self, env, testing_iterations):
        LearningAgent.__init__(self, env, testing_iterations)

    def getPolicy(self, obs):
        return self.env.action_space.sample()

"""
Agent for Tabular Q-Learning
"""
class QLearningAgent(LearningAgent):
    def __init__(self, env, training_iterations, testing_iterations, epsilon, gamma, alpha):
        self.env = env
        self.training = training_iterations
        self.testing = testing_iterations
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.QValues = utils.Counter()
        self.actions = [i for i in range(self.env.action_space.n)]

    def getQValue(self, state, action):
        return self.QValues[state, action]

    def getValue(self, state):
        maxQValue = None
        for action in self.actions:
          QValue = self.getQValue(state, action)
          if maxQValue < QValue:
            maxQValue = QValue
        return 0 if maxQValue is None else maxQValue

    # we break ties randomly
    def getPolicy(self, state):
        maxQValue, maxActions = None, []
        for action in self.actions:
          QValue = self.getQValue(state, action)
          if maxQValue < QValue:
            maxQValue = QValue
            maxActions = [action]
          elif maxQValue == QValue:
            maxActions.append(action)
        return random.choice(maxActions)

    def epsilonGreedyAction(self, state):
        return random.choice(self.actions) if utils.flipCoin(self.epsilon) else self.getPolicy(state)

    def updateQValues(self, state, action, nextState, reward):
        self.QValues[state, action] = (1 - self.alpha) * self.QValues[state, action] + \
          self.alpha * (reward + self.gamma * self.getValue(nextState))

    def train_agent(self):
        for episode in range(self.training):
            done, prevObs = False, self.env.reset()
            while not done:
                action = self.epsilonGreedyAction(prevObs)
                obs, reward, done, _ = self.env.step(action)
                self.updateQValues(prevObs, action, obs, reward)
                prevObs = obs

"""
QLearning with extra incentives for taxi
"""
class TaxiQLAgent(QLearningAgent):
    def __init__(self, env, training_iterations, testing_iterations, epsilon, gamma, alpha):
        QLearningAgent.__init__(self, env, training_iterations, testing_iterations, epsilon, gamma, alpha)

    def train_agent(self):
        for episode in range(self.training):
            done, prevObs = False, self.env.reset()
            pickup, dropoff = findPickupDropoff(prevObs)

            while not done:
                action = self.epsilonGreedyAction(prevObs)
                obs, reward, done, _ = self.env.step(action)

                pos, prevPos = getPosition(obs), getPosition(prevObs)
                if isPickingUp(obs):
                    dist, prevDist = manhattanDistance(pos, pickup), manhattanDistance(prevPos, pickup)
                    if dist < prevDist:
                        reward += 1
                    if dist > prevDist:
                        reward -= 1
                else:
                    dist, prevDist = manhattanDistance(pos, dropoff), manhattanDistance(prevPos, dropoff)
                    if dist < prevDist:
                        reward += 1
                    if dist > prevDist:
                        reward -= 1

                self.updateQValues(prevObs, action, obs, reward)
                prevObs = obs

"""
QLearning with extra incentives for FrozenLake
"""
class FrozenLakeQLAgent(QLearningAgent):
    def __init__(self, env, training_iterations, testing_iterations, epsilon, gamma, alpha):
        QLearningAgent.__init__(self, env, training_iterations, testing_iterations, epsilon, gamma, alpha)

    def train_agent(self, maxValue, holes):
        for episode in range(self.training):
            done, prevObs = False, self.env.reset()
            while not done:
                action = self.epsilonGreedyAction(prevObs)
                obs, reward, done, _ = self.env.step(action)

                # reward getting closer to the goal
                if ((obs % maxValue) > (prevObs % maxValue) or \
                (obs / maxValue) > (prevObs / maxValue)):
                    reward += 0.01

                # punish going backwards or dying
                if ((obs % maxValue) < (prevObs % maxValue) or \
                (obs / maxValue) < (prevObs / maxValue)) or obs in holes:
                    reward -= 0.01

                self.updateQValues(prevObs, action, obs, reward)
                prevObs = obs
