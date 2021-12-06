import update_board

if __name__ == '__main__':
    update_board.apply()
# import random
#
# import Constants
# import calendar
# import time
#
# from Model import Environment, Agent
#
# if __name__ == '__main__':
#     env = Environment()
#     agent = Agent(env)
#     seconds = calendar.timegm(time.gmtime())
#     for i in range(30):
#         agent.reset()
#         agent.column = [random.randint(1, 4), random.randint(1, 4), random.randint(1, 4)]
#         print("column", agent.column)
#         for j in range(40):
#             print("env.isLost ", env.isLost)
#             if env.isLost:
#                 print(env.values)
#                 agent.reset()
#                 env.reset()
#                 break
#             else:
#                 if seconds + 1 < calendar.timegm(time.gmtime()):
#                     seconds = calendar.timegm(time.gmtime())
#                     env.apply(agent, Constants.DOWN)
#                 action = agent.best_action()
#                 print("best action", action)
#                 env.apply(agent, action)
#         print("ICIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII ", i)
#
#     print(env.values)
#     print(agent.qtable)
