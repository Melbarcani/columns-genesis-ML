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
        agent.load(agent_filename)

    for i in range(10):
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
        if i % 100 == 0:
            print("i ", i, "score break", agent.score_break, "score", agent.score)
            print(env.board)
            print("Exploration", exploration)


        agent.update_history()
    agent.save(agent_filename)
    plt.plot(agent.history)
    plt.show()

