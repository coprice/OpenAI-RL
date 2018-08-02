# Reinforcement Learning Analysis in the OpenAI Gym Environments
Final project for CS182 (Harvard College) by Sam Oh, Brandon Hills, and Collin Price.

## Overview
In this project, we calculated optimal solutions for three games (Taxi, Frozen Lakes, N-Chain) and used these solutions as a baseline for testing the effectiveness of Q-learning on these games. We modelled Taxi as a search problem, and used A* search to find the optimal policy. Frozen Lakes and N-Chain were stochastic games, so we modelled them as MDPs and used value iteration to create optimal policies for them.

## Requirements
You need to have python 2.7, as well as have the gym module and scipy installed. Simply run **pip install -r requirements.txt**.

## Specification
All of our learning agents (Q-learning, Incentivized Q-learning, Random agent) can be found in learningAgents.py. Our MDP models for Frozen Lakes and N-Chain can be found in MDP.py, and the corresponding Value Iteration agents for these games in valueIterationAgents.py. Our optimal solution for the taxi game can be found in searchTaxi.py, where we implement A* search. Utils.py contains some helper classes (mainly the Counter and PriorityQueue) that were provided in our problem sets, which can be found [here](http://ai.berkeley.edu/project_overview.html).

## Running
All of our results are compiled in our test files for each game: testTaxi.py, testFrozenLakes.py, and testNChain.py. Running any of these files will compare the results of the Q-learning and incentivized Q-learning agents with the optimal solution for that game. With N-Chain, we just use regular Q-learning.

You can also visualize the agents using the graphics.py file for each game. By default, running the graphics file will display 3 games of the taxi game, where we use the optimal policy. There are 4 parameters that you can change in the command line (which can be seen in parser.py): -g lets you change the game (t for taxi, f4/f8 for frozen lake4x4/8x8, n for nchain). -a lets you change the learning agent (to q for Q-Learning, iq for Incentivized Q-Learning, or r for Random. We use the optimal agent by default). -s lets you change how many game simulations you observe. -i lets you change the training iterations used for the learning agents (it is 2500 by default). If you play the N-Chain game, you cannot use -a=iq because there is not incentivized Q-learning for it. Also, if you use -a=q for N-Chain, you need to specify training iterations of 50 or less.
