"""
Below is a search problem for the open AI game taxi. We use A* search
to compute the optimal path from the start state of the game. The state space
is a 5x5 grid (open AI represents this grid and the states with numbers from
0-499). We convert the number representation to a coordinate system, with (1,1)
at the bottom left, and (5,5) at the top right.
"""

import gym
from utils import PriorityQueue

"""
gets (x, y) position from map number
"""
def getPosition(obs):
  hundreds, tens = (obs - obs % 100) / 100, ((obs % 100) - (obs % 10)) / 10
  return (tens + 2) / 2, 5 - hundreds

"""
returns (resulting point, action used) for a given taxi position
"""
def getSuccessors(pos):
  x, y = pos
  l, r, u, d = ((x-1,y), 3), ((x+1,y), 2), ((x,y+1), 1), ((x,y-1), 0)

  if x == 1:
    if y == 5:
      return [r, d]
    elif y == 1:
      return [u]
    elif y == 2:
      return [d, u]
    else:
      return [r, u, d]
  elif x == 2:
    if y == 5:
      return [l, d]
    elif y == 1:
      return [r, u]
    elif y == 2:
      return [r, u, d]
    else:
      return [l, r, u, d]
  elif x == 3:
    if y == 5:
      return [r, d]
    elif y == 1:
      return [l, u]
    elif y == 2:
      return [l, u, d]
    else:
      return [l, r, u, d]
  elif x == 4:
    if y == 5:
      return [l, r, d]
    elif y == 1:
      return [r, u]
    elif y == 2:
      return [r, u, d]
    else:
      return [l, r, u, d]
  else:
    if y == 5:
      return [l, d]
    elif y == 1:
      return [l, u]
    else:
      return [l, u, d]

"""
heuristic for A* search
"""
def manhattanDistance(p1, p2):
  return (abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]))

"""
A* search for current pos to goal (returns list of actions)
"""
def aStarSearch(pos, goal):
  fringe, visited, best = PriorityQueue(), set(), {}
  fringe.push((pos, [], 0), manhattanDistance(pos, goal))

  while not fringe.isEmpty():

    current_point, actions, total_cost = fringe.pop()

    if current_point in visited or \
    (current_point in best and best[current_point] <= total_cost):
      continue

    visited.add(current_point)
    best[current_point] = total_cost

    # current vertex is a solution
    if current_point == goal:
      return actions

    for (point, action) in getSuccessors(current_point):
      # if node not visited add it to the fringe
      if point not in visited:
        actions_copy = list(actions)
        actions_copy.append(action)
        cost = total_cost + 1
        fringe.push((point, actions_copy, cost), \
          cost + manhattanDistance(point, goal))

  raise Exception('Problem Not Solved')

"""
computes optimal action sequence starting at pos, picking up X1, and
dropping off at X2
"""
def computeActionSequence(X1, X2, pos):
  pickup = aStarSearch(pos, X1)
  pickup.append(4)
  dropoff = aStarSearch(X1, X2)
  dropoff.append(5)
  return pickup + dropoff

def findPickupDropoff(obs):
  tens, ones = ((obs % 100) - (obs % 10)) / 10, obs % 10
  G, B, Y, R, pos = (5, 5), (4, 1), (1, 1), (1, 5), getPosition(obs)
  if (tens % 2) == 1:
    if ones == 1:
      return (Y, B)
    if ones == 2:
      return (B, R)
    if ones == 3:
      return (B, G)
    if ones == 4:
      return (B, Y)
    if ones == 6:
      return (None, R)
    if ones == 7:
      return (None, G)
    if ones == 8:
      return (None, Y)
    if ones == 9:
      return (None, B)
  else:
    if ones == 1:
      return (R, G)
    if ones == 2:
      return (R, Y)
    if ones == 3:
      return (R, B)
    if ones == 4:
      return (G, R)
    if ones == 6:
      return (G, Y)
    if ones == 7:
      return (G, B)
    if ones == 8:
      return (Y, R)
    if ones == 9:
      return (Y, G)

"""
solves taxi game based on initial gamestate observation
"""
def solveTaxi(obs):
  pickup, dropoff = findPickupDropoff(obs)
  pos = getPosition(obs)
  return computeActionSequence(pickup, dropoff, pos)

"""
determines if we need to pick up or drop off (we use this for incentivized QLearning)
"""
def isPickingUp(obs):
  tens, ones = ((obs % 100) - (obs % 10)) / 10, obs % 10
  if (tens % 2) == 1 and ones >= 5:
    return False
  else:
    return True

if __name__ == "__main__":
  env = gym.make('Taxi-v2')
  correct, iterations = 0, 1000
  print "Checking accuracy with {} iterations...".format(iterations)
  for _ in range(iterations):
    obs, rewards = env.reset(), 0
    actions = solveTaxi(obs)
    for action in actions:
      obs, reward, done, _ = env.step(action)
      rewards += reward
    if done and rewards > 0:
      correct += 1
  print '{}% correct'.format(correct*100.0/iterations)
