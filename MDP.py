"""
A generic MDP class to inherit from.
"""
class MDP(object):
  def __init__(self):
    pass
  def getStates(self):
    pass
  def getActions(self):
    pass
  def isTerminal(self, state):
    pass
  def getReward(self, state, action, nextState):
    pass
  def getTransitionStatesAndProbs(self, state, action):
    pass

"""
An MDP model designed for the Open AI gym game, FrozenLake. The game comes in
two version: a 4x4 and an 8x8 grid. We model the grid with (x,y) coordinates,
where (1,1) is at the start state (top left) and the goal state is at the bottom
right.
"""
class FrozenLakeMDP(MDP):
  def __init__(self, maxValue, holes):
    self.max = maxValue
    self.holes = holes

  """
  converts a grid number to an (x, y) coordinate
  """
  def getPos(self, i):
    return ((i % self.max) + 1, (i / self.max) + 1)

  def getStates(self):
    return [self.getPos(i) for i in range(self.max * self.max)]

  # FrozenLake has 4 actions: left (0), down (1), right (2), up (3)
  def getActions(self):
    return [i for i in range(4)]

  def isTerminal(self, state):
    return state in self.holes

  def isGoal(self, state):
    return state == (self.max, self.max)

  # This reward system is consistent with the one specified by open AI
  def getReward(self, state, action, nextState):
    if self.isGoal(nextState):
      return 1.0
    else:
      return 0.0

  def getTransitionStatesAndProbs(self, state, action):

    # helper for choosing which [(trans states, probabilities)] given action
    def options(lst1, lst2, lst3, lst4, action):
      if action == 0:
        return lst1
      if action == 1:
        return lst2
      if action == 2:
        return lst3
      if action == 3:
        return lst4

    third, tThird = 1.0/3, 2.0/3
    x, y = state
    left, down, right, up = (x-1,y), (x,y+1), (x+1,y),(x,y-1)

    # TOP LEFT
    if state == (1, 1):
      return options([(state, tThird), (down, third)], \
                     [(down, third), (right, third), (state, third)], \
                     [(right, third), (down, third), (state, third)], \
                     [(state, tThird), (right, third)], action)

    # BOTTOM LEFT
    elif state == (1, self.max):
      return options([(state, tThird), (up, third)], \
                     [(state, tThird), (right, third)], \
                     [(right, third), (up, third), (state, third)], \
                     [(state, third), (right, third), (up, third)], action)

    # TOP RIGHT
    elif state == (self.max, 1):
      return options([(state, third), (down, third), (left, third)], \
                     [(state, third), (left, third), ( down ,third)], \
                     [(state, tThird), (down, third)], \
                     [(state, tThird), (left, third)], action)

    # BOTTOM RIGHT
    elif state == (self.max, self.max):
      return options([(state, third), (left, third), (up, third)], \
                     [(state, tThird), (left, third)], \
                     [(state, tThird), (up, third)], \
                     [(state, third), (up, third), (left, third)], action)

    # LEFT EDGE
    elif x == 1:
      return options([(state, third), (up, third), (down, third)], \
                     [(state, third), (down, third), (right, third)], \
                     [(right, third), (up, third), (down, third)], \
                     [(state, third), (up, third), (right, third)], action)

    # TOP EDGE
    elif y == 1:
      return options([(state, third), (left, third), (down, third)], \
                     [(left, third), (down, third), (right, third)], \
                     [(state, third), (right, third), (down, third)], \
                     [(state, third), (left, third), (right, third)], action)

    # RIGHT EDGE
    elif x == self.max:
      return options([(left, third), (up, third), (down, third)], \
                     [(state, third), (down, third), (left, third)], \
                     [(state, third), (up, third), (down, third)], \
                     [(state, third), (up, third), (left, third)], action)

    # BOTTOM EDGE
    elif y == self.max:
      return options([(state, third), (up, third), (left, third)], \
                     [(state, third), (left, third), (right, third)], \
                     [(state, third), (up, third), (right, third)], \
                     [(up, third), (left, third), (right, third)], action)

    # MIDDLE
    else:
      return options([(left, third), (up, third), (down, third)], \
                     [(down, third), (left, third), (right, third)], \
                     [(right, third), (up, third), (down, third)], \
                     [(up, third), (left, third), (right, third)], action)

"""
An MDP model designed for the Open AI gym game, NChain. The game is
a linear chain of states with two actions 0 (forward) and 1 (backward).
"""

class NChainMDP(object):
  def __init__(self, p, n):
    self.p = p
    self.end = n - 1

  def getStates(self):
    return [i for i in range(5)]

  def getActions(self):
    return [i for i in range(2)]

  # NChain has no terminal states
  def isTerminal(self, state):
    return False

  def getReward(self, state, action, nextState):
    if action == 1: # going backward
      if nextState == 0:
        return 2
      else:
        return 0
    else: # going forward
      if state == self.end and nextState == self.end:
        return 10
      else:
        return 0

  def getTransitionStatesAndProbs(self, state, action):
    p, q = self.p, 1 - self.p

    if action == 1: # going backward
      if state < self.end:
        return ([(0, p), (state+1, q)])
      else:
        return ([(0, p), (state, q)])
    else: # going forward
      if state < self.end:
        return ([(0, q), (state+1, p)])
      else:
        return ([(0, q), (state, p)])
