import os

from Constant import *
from Environment import Environment
from Agent import Agent
import calendar
import time
import random
import matplotlib.pyplot as plt

if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)
    agent_filename = 'agent.dat'
    # window = ColumnsWindow(env)
    # window.setup()
    # arcade.run()
    if os.path.exists(agent_filename):
        # agent.load(agent_filename)
        pass

    for i in range(3000):
        exploration = agent.exploration
        agent.reset()
        agent.exploration = exploration
        env.reset()
        seconds = calendar.timegm(time.gmtime())
        actions = [0, 0, 0, 0]


        while not env.isLost:
            agent.resetPosition()
            env.is_round_ended = False
            agent.column = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
            old_action = DOWN
            counter = 0
            while not env.is_round_ended:
                if old_action != DOWN and counter > 3:
                    env.apply(agent, DOWN)
                    old_action = DOWN
                    counter = 0
                else:
                    counter += 1
                    action = agent.best_action()
                    if action == DOWN:
                        actions[0] += 1
                    elif action == LEFT:
                        actions[1] += 1
                    elif action == RIGHT:
                        actions[2] += 1
                    elif action == CHANGE:
                        actions[3] += 1
                    old_action = action
                    env.apply(agent, action)
            print("counter", counter)

        agent.update_history()
        print("score de l'agent", agent.score)
        print("count left and right", env.borderCount)
        print("actions DLRX", agent.actions)
        print("main actions DLRX", actions)
        print("Exploration", exploration)
        print(env.board)
    print(len(agent.qtable), agent.qtable)
    print(env.tracker)
    # agent.save(agent_filename)
    # print(len(agent.qtable), agent.qtable)
    plt.plot(agent.history)
    plt.show()

    # seconds = calendar.timegm(time.gmtime())
    # for i in range(2):
    #     agent.reset()
    #     agent.score = 0
    #     env.reset()
    #     while not env.isLost:
    #         agent.reset()
    #         env.is_round_ended = False
    #         agent.column = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
    #         # print(agent.column)
    #         while not env.is_round_ended and not env.isLost:
    #             if seconds + 3 < calendar.timegm(time.gmtime()):
    #                 seconds = calendar.timegm(time.gmtime())
    #                 env.apply(agent, DOWN)
    #             else:
    #                 action = agent.best_action()
    #                 env.apply(agent, action)
    #         print("after \n", env.board)
    #     print("final score", agent.score)
    # print(len(env.values))
    print(len(agent.qtable))
    # print(agent.qtable)
