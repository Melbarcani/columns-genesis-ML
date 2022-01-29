from Constant import DOWN
from Environment import Environment
from Agent import Agent
import calendar
import time
import random
import matplotlib.pyplot as plt

if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)
    # window = ColumnsWindow(env)
    # window.setup()
    # arcade.run()

    for i in range(5000):
        agent.reset()
        env.reset()
        seconds = calendar.timegm(time.gmtime())
        while not env.isLost:
            agent.resetPosition()
            env.is_round_ended = False
            agent.column = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3)]
            while not env.is_round_ended and not env.isLost:
                if seconds + 1 < calendar.timegm(time.gmtime()):
                    seconds = calendar.timegm(time.gmtime())
                    env.apply(agent, DOWN)
                else:
                    action = agent.best_action()
                    env.apply(agent, action)
        agent.update_history()
        print("score de l'agent",agent.score)

    print(agent.qtable)
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
    print(len(env.values))
    print(len(agent.qtable))
    print(agent.qtable)

