from Tkinter import *
from time import sleep
import gym

from MDP import *
from learningAgents import *
from valueIterationAgents import *
from parser import Parser
from searchTaxi import solveTaxi, getPosition, findPickupDropoff


"""
Displays performance of a specified agent in the Taxi game. The optimal
policy is used if there is no agent provided. We repeat for a specified number
of games provided. We repeat for a specified number of games provided, and
cancel a game iteration if we take more steps than specified (in maxSteps).
"""
def displayTaxi(environment, games, maxSteps, agent=None):
    global env
    global obs
    global done
    global simulations
    global steps

    if games > 1:
        print '{} Simulations Remaining...'.format(games)
    else:
        print '{} Simulation Remaining...'.format(games)

    # these globals don't get refreshed
    env, simulations = environment, games

    # globals that get refreshed
    obs, done, steps = None, None, None

    # displaying the optimal taxi solution
    if not agent:
        global actions
        global currentAction
        actions, currentAction = None, None # these get refreshed

    cw, ch = 500, 500 # window dimensions
    root = Tk()
    root.title('Taxi Simulator')

    # position window in middle of the screen
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    window_x = screen_w/2 - cw/2
    window_y = screen_h/2 - ch/2
    root.geometry('{}x{}+{}+{}'.format(cw,ch,window_x,window_y))
    root.resizable(width=FALSE, height=FALSE)

    C = Canvas(root, width=cw, height=ch)
    C.pack()

    background = PhotoImage(file='img/taxi/background.gif')
    taxi = PhotoImage(file='img/taxi/taxi.gif')
    pickup = PhotoImage(file='img/taxi/pickup.gif')
    dropoff = PhotoImage(file='img/taxi/dropoff.gif')

    # draws the game with given observation
    def draw(obs):
        C.delete('all')
        C.create_image(cw/2, ch/2, image=background)

        pick, drop = findPickupDropoff(obs)
        pos = getPosition(obs)

        if pick:
            C.create_image((pick[0]-1)*cw/5 + cw/10, (6 - pick[1])*ch/5 - ch/10, image=pickup)

        C.create_image((drop[0]-1)*cw/5 + cw/10, (6 - drop[1])*ch/5 - ch/10, image=dropoff)
        C.create_image((pos[0]-1)*cw/5 + cw/10, (6 - pos[1])*ch/5 - ch/10, image=taxi)

    # updates game and calls draw
    def update(event):
        global obs
        global done

        if not agent:
            global currentAction
            global actions
            obs, _, done, _ = env.step(actions[currentAction])
            currentAction += 1
        else:
            obs, _, done, _ = env.step(agent.getPolicy(obs))

        draw(obs)

    root.bind('<<update>>', update)

    # while simulating, updates game every 0.2s
    def updater():
        global done
        global simulations
        global steps

        if not done and steps <= maxSteps: # only allow 20 steps
            steps += 1
            root.event_generate('<<update>>')
            root.after(200, updater)
        else:
            sleep(0.25)
            simulations -= 1
            if simulations == 0:
                print 'Simulation Terminated.'
                root.destroy()
            else:
                if simulations > 1:
                    print '{} Simulations Remaining...'.format(simulations)
                else:
                    print '{} Simulation Remaining...'.format(simulations)
                C.delete('all')
                root.event_generate('<<refresh>>')

    # restarts a game simulation
    def refresh(event):
        global env
        global obs
        global done
        global steps
        obs = env.reset()
        done = False
        steps = 0

        if not agent:
            global actions
            global currentAction
            actions = solveTaxi(obs)
            currentAction = 0

        draw(obs)
        root.after(500, updater)

    root.bind('<<refresh>>', refresh)
    root.event_generate('<<refresh>>')
    root.attributes("-topmost", True)
    root.mainloop()


"""
Displays performance of a specified agent in either of the Frozen Lakes games.
The optimal policy is used if there is no agent provided. We repeat for a
specified number of games provided, and cancel a game iteration if we take more
steps than specified (in maxSteps). default is a boolean that is true if we
are using the optimal policy (value iteration), else false.
"""
def displayFrozenLake(environment, games, agent, s, maxSteps, default):
    global env
    global obs
    global done
    global simulations
    global steps

    if games > 1:
        print '{} Simulations Remaining...'.format(games)
    else:
        print '{} Simulation Remaining...'.format(games)

    # these globals don't get refreshed
    env, simulations = environment, games

    # globals that get refreshed
    obs, done, steps = None, None, None

    cw, ch = 100*s, 100*s # window dimensions
    root = Tk()
    root.title('Frozen Lake Simulator')

    # position window in middle of the screen
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    window_x = screen_w/2 - cw/2
    window_y = screen_h/2 - ch/2
    root.geometry('{}x{}+{}+{}'.format(cw,ch,window_x,window_y))
    root.resizable(width=FALSE, height=FALSE)

    C = Canvas(root, width=cw, height=ch)
    C.pack()

    if s == 4:
        background = PhotoImage(file='img/frozenlake/background4x4.gif')
    else:
        background = PhotoImage(file='img/frozenlake/background8x8.gif')

    player = PhotoImage(file='img/frozenlake/player.gif')

    # draws the game with given observation
    def draw(obs):
        C.delete('all')
        C.create_image(cw/2, ch/2, image=background)
        C.create_image((obs % s)*cw/s + cw/(2*s), ((obs / s)+1)*ch/s - ch/(2*s), image=player)

    # updates game and calls draw
    def update(event):
        global obs
        global done
        global currentAction
        global actions

        if default:
            obs, _, done, _ = env.step(agent.getPolicy(((obs % s) + 1, (obs / s) + 1)))
        else:
            obs, _, done, _ = env.step(agent.getPolicy(obs))
        draw(obs)

    root.bind('<<update>>', update)

    # while simulating, updates game every 0.2s
    def updater():
        global done
        global simulations
        global steps

        if not done and steps <= maxSteps:
            steps += 1
            root.event_generate('<<update>>')
            root.after(50, updater)
        else:
            sleep(1)
            simulations -= 1
            if simulations == 0:
                print 'Simulation Terminated.'
                root.destroy()
            else:
                if simulations > 1:
                    print '{} Simulations Remaining...'.format(simulations)
                else:
                    print '{} Simulation Remaining...'.format(simulations)
                C.delete('all')
                root.event_generate('<<refresh>>')

    # restarts a game simulation
    def refresh(event):
        global env
        global obs
        global done
        global steps
        obs = env.reset()
        done = False
        steps = 0
        draw(obs)
        root.after(500, updater)

    root.bind('<<refresh>>', refresh)
    root.event_generate('<<refresh>>')
    root.attributes("-topmost", True)
    root.mainloop()


def displayNChain(environment, games, agent):
    global env
    global obs
    global done
    global simulations
    global rewards

    if games > 1:
        print '{} Simulations Remaining...'.format(games)
    else:
        print '{} Simulation Remaining...'.format(games)

    # these globals don't get refreshed
    env, simulations = environment, games

    # globals that get refreshed
    obs, done, rewards = None, None, None

    cw, ch = 500, 300 # window dimensions
    root = Tk()
    root.title('N-Chain Simulator')

    # position window in middle of the screen
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    window_x = screen_w/2 - cw/2
    window_y = screen_h/2 - ch/2
    root.geometry('{}x{}+{}+{}'.format(cw,ch,window_x,window_y))
    root.resizable(width=FALSE, height=FALSE)

    C = Canvas(root, width=cw, height=ch)
    C.pack()

    background = PhotoImage(file='img/nchain/background.gif')
    player = PhotoImage(file='img/nchain/player.gif')

    # draws the game with given observation
    def draw(obs, rewards):
        C.delete('all')
        C.create_image(cw/2, ch/2, image=background)
        C.create_image((obs + 1) * cw/5 - cw/10, ch/2, image=player)
        C.create_text(cw/2, 20, text='Rewards: ' + str(rewards), fill='black', \
                                    font=('futura', 24))

    # updates game and calls draw
    def update(event):
        global obs
        global done
        global currentAction
        global actions
        global rewards

        obs, reward, done, _ = env.step(agent.getPolicy(obs))
        rewards += reward
        draw(obs, rewards)

    root.bind('<<update>>', update)

    # while simulating, updates game every 0.2s
    def updater():
        global done
        global simulations

        if not done:
            root.event_generate('<<update>>')
            root.after(10, updater)
        else:
            sleep(1)
            simulations -= 1
            if simulations == 0:
                root.destroy()
                print 'Simulation Terminated.'
            else:
                if simulations > 1:
                    print '{} Simulations Remaining...'.format(simulations)
                else:
                    print '{} Simulation Remaining...'.format(simulations)
                C.delete('all')
                root.event_generate('<<refresh>>')

    # restarts a game simulation
    def refresh(event):
        global env
        global obs
        global done
        global rewards
        obs = env.reset()
        done = False
        rewards = 0
        draw(obs, rewards)
        root.after(500, updater)

    root.bind('<<refresh>>', refresh)
    root.event_generate('<<refresh>>')
    root.attributes("-topmost", True)
    root.mainloop()


if __name__ == '__main__':
    parser = Parser()
    args = parser.args
    env = None

    # get game environment
    if args.g == 't':
        env = gym.make('Taxi-v2')
    elif args.g == 'f4':
        env = gym.make('FrozenLake-v0')
    elif args.g == 'f8':
        env = gym.make('FrozenLake8x8-v0')
    else:
        env = gym.make('NChain-v0')

    training_iterations = args.i
    simulations = args.s

    # set up game playing agents
    agent, agentType, default = None, None, None
    holes4 = {(2,2), (4,2), (4,3), (1,4)}
    holes8 = {(4,3),(6,4),(4,5),(2,6),(3,6),(7,6),(2,7),(5,7),(7,7),(4,8)}

    if args.a == 'q':
        agentType = 'Q-Learning Agent'
        print 'Using Q-Learning Agent...'

        # use properly tuned hyperparameters
        if args.g == 't':
            agent = QLearningAgent(env, training_iterations, None, 0.15, 0.9, 0.1)
        elif args.g == 'n':
            agent = QLearningAgent(env, training_iterations, None, 1, 0.9, 0.1)
        else:
            agent = QLearningAgent(env, training_iterations, None, 0.2, 0.99, 0.1)

        print 'Training Agent with {} Iterations...'.format(training_iterations)
        agent.train_agent()

    elif args.a == 'iq':
        agentType = 'Incentivized Q-Learning Agent'
        print 'Using Incentivized Q-Learning Agent...'
        if args.g == 't':
            agent = TaxiQLAgent(env, training_iterations, None, 0.15, 0.9, 0.1)
            agent.train_agent()
        else:
            agent = FrozenLakeQLAgent(env, training_iterations, None, 0.2, 0.99, 0.1)
            if args.g == 'f4':
                agent.train_agent(4, holes4)
            else:
                agent.train_agent(8, holes8)
        print 'Training Agent with {} Iterations...'.format(training_iterations)

    elif args.a == 'r':
        agentType = 'Random Agent'
        print 'Using Random Agent...'
        agent = RandomAgent(env, None)

    else:
        agentType = 'Optimal Policy'
        default = True

        # value iteration agents
        if args.g == 'f4':
            mdp = FrozenLakeMDP(4, holes4)
            agent = FrozenLakeVIAgent(mdp, None)
        elif args.g == 'f8':
            mdp = FrozenLakeMDP(8, holes8)
            agent = FrozenLakeVIAgent(mdp, None)
        elif args.g == 'n':
            mdp = NChainMDP(0.8, 5)
            agent = NChainVIAgent(mdp, None)

    # display GUI
    if args.g == 't':
        print '\n---Simulating {} Taxi Games with {}---\n'.format(simulations, agentType)
        displayTaxi(env, simulations, 20, agent)
    elif args.g == 'f4':
        print '\n---Simulating {} FrozenLake4x4 Games with {}---\n'.format(simulations, agentType)
        displayFrozenLake(env, simulations, agent, 4, 50, default)
    elif args.g == 'f8':
        print '\n---Simulating {} FrozenLake8x8 Games with {}---\n'.format(simulations, agentType)
        displayFrozenLake(env, simulations, agent, 8, 100, default)
    else:
        print '\n---Simulating {} N-Chain Games with {}---\n'.format(simulations, agentType)
        displayNChain(env, simulations, agent)
