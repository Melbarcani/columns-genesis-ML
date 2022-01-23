from Constant import *


def get_key(state):
    return state if type(state) is not list else tuple([item for sublist in state for item in sublist])


class Agent:
    def __init__(self, environment, learning_rate=0.4, discount_factor=0.7):
        self.__score = 0
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__column = [0, 0, 0]
        self.__state = ()
        self.__qtable = {}
        self.__position = ()
        for s in self.__environment.values:
            self.__qtable[get_key(s)] = {}
            for a in ACTIONS:
                self.__qtable[get_key(s)][a] = 0.0
        self.reset()

    def update(self, state, action, reward):
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]
        key = get_key(state)
        if key not in self.__qtable:
            self.__qtable[key] = {}
            for a in ACTIONS:
                self.__qtable[key][a] = 0.0

        maxQ = max(self.__qtable[key].values())
        self.__qtable[key][action] += self.__learning_rate * (
                reward + self.__discount_factor * maxQ - self.__qtable[key][action])
        self.__state = key
        self.__score += reward

    def best_action(self):
        best = None
        key = get_key(self.__state)
        if key not in self.__qtable:
            best = CHANGE
        else:
            for a in self.__qtable[key]:
                if not best \
                        or self.__qtable[key][a] > self.__qtable[key][best]:
                    best = a
        return best

    def reset(self):
        self.__position = (0, 4)
        self.__state = self.__environment.start
        self.__score = 0

    @property
    def qtable(self):
        return self.__qtable

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score

    @property
    def column(self):
        return self.__column

    @column.setter
    def column(self, column):
        self.__column = column

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position
