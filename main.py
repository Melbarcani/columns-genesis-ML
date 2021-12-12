# import update_board
#
# if __name__ == '__main__':
#     update_board.apply()
import random

import Constants
import calendar
import time

from ColumnsWindow import *
from Model import Environment, Agent

if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)
    window = ColumnsWindow(env)
    window.setup()
    arcade.run()

    seconds = calendar.timegm(time.gmtime())
    for i in range(15):
        agent.reset()
        env.reset()

        while not env.isLost:
            agent.reset()
            env.is_round_ended = False
            agent.column = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
            print(agent.column)
            while not env.is_round_ended and not env.isLost:
                if seconds + 1 < calendar.timegm(time.gmtime()):
                    seconds = calendar.timegm(time.gmtime())
                    env.apply(agent, Constants.DOWN)
                else:
                    action = agent.best_action()
                    env.apply(agent, action)
            print("after \n", env.board)
        print("final score", agent.score)
        print(env.values)
    print(agent.qtable)
