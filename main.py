from Constant import DOWN
from Environment import Environment
from Agent import Agent
import calendar
import time
import random

if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)


    for i in range(3):
        agent.reset()
        agent.score = 0
        env.reset()
        seconds = calendar.timegm(time.gmtime())
        while not env.isLost:
            agent.reset()
            env.is_round_ended = False
            agent.column = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
            while not env.is_round_ended and not env.isLost:
                if seconds + 0.0001 < calendar.timegm(time.gmtime()):
                    seconds = calendar.timegm(time.gmtime())
                    env.apply(agent, DOWN)
                else:
                     action = agent.best_action()
                     print("Action", action)
                     env.apply(agent, action)
                print(env.board)
            if i == 900000:
                print("i",i)


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
    print(len(env.values))
    print(len(agent.qtable))
    print(agent.qtable)

