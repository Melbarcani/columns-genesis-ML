from Constants import *
class Agent:
    def __init__(self, environment, learning_rate=0.4, discount_factor=0.5):
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__column = [0, 0, 0]
        self.__state = []
        self.__qtable = {}
        for s in self.__environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0
        self.reset()

    def reset(self):
        self.__state = self.__environment.start
        self.__score = 0

    def update(self, state, action, reward):
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]

        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * (
                reward + self.__discount_factor * maxQ - self.__qtable[self.__state][action])
        self.__state = state
        self.__score += reward

    @property
    def qtable(self):
        return self.__qtable

    def best_action(self):
        best = None
        for a in self.__qtable[self.__state]:
            if not best \
                    or self.__qtable[self.__state][a] > self.__qtable[self.__state][best]:
                best = a
        return best

    @property
    def state(self):
        return self.__state

    @property
    def column(self):
        return self.__column

    @column.setter
    def column(self, column):
        self.__column = column

    @property
    def score(self):
        return self.__score