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
        #agent.load(agent_filename)
        pass

    for i in range(15):
        exploration = agent.exploration
        agent.reset()
        agent.exploration = exploration
        env.reset()
        seconds = calendar.timegm(time.gmtime())
        board = env.board

        while not env.isLost:
            agent.resetPosition()
            env.is_round_ended = False
            agent.column = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
            old_action = DOWN
            counter = 0
            while not env.is_round_ended:
                if counter > 3 and old_action != DOWN:  # every 3 actions column must get down
                    env.apply(agent, DOWN)
                    old_action = DOWN
                    counter = 0
                else:
                    action = agent.best_action()
                    counter = (counter + 1) if action != DOWN else 0
                    old_action = action
                    env.apply(agent, action)
                    # print("action", action)
        #print(env.board)
        #print(agent.score_break)

        agent.update_history()
        print("score de l'agent", agent.score)
        # print("Exploration", exploration)
        # print(env.board)
        # print("number", actionsNumber)
    #agent.save(agent_filename)
    #print(agent.qtable, len(agent.qtable))
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
    # print(len(agent.qtable))
    # print(agent.qtable)
