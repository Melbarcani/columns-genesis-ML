import pickle
from decimal import Decimal
from Constant import *
from random import *


def get_key(state):
    return state if type(state) is not list else tuple([item for sublist in state for item in sublist])


class Agent:
    def __init__(self, environment, learning_rate=1, discount_factor=1):
        self.__score_break = 0
        self.__score = 0
        self.__environment = environment
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__column = [0, 0, 0]
        self.__state = ()
        self.__qtable = {}
        self.__position = ()
        self.__history = []
        self.__actions = [0, 0, 0, 0]
        self.__exploration = EXPLORATION
        for s in self.__environment.values:
            self.set_random_action(get_key(s))
        self.reset()

    def update_history(self):
        self.__history.append(self.__score_break)

    @property
    def history(self):
        return self.__history

    def set_new_state(self, new_state):
        key = get_key(new_state)
        if key not in self.__qtable:
            self.set_random_action(key)
        self.__state = new_state

    def update(self, state, action, reward):
        # if reward > 1:
        # print("reward", reward)
        # Q(s, a) <- Q(s, a) + learning_rate *
        #                     [reward + discount_factor * max(Q(state)) - Q(s, a)]
        key = get_key(state)
        if key not in self.__qtable:
            self.set_random_action(key)

        maxQ = max(self.__qtable[key].values())
        self.__qtable[key][action] += self.__learning_rate * (
                reward + self.__discount_factor * maxQ - self.__qtable[key][action])
        self.__state = key

        self.__score += Decimal(reward)

    def set_random_action(self, key):
        self.__qtable[key] = {}
        for a in ACTIONS:
            self.__qtable[key][a] = 1  # random() * 10.0

    def best_action(self):
        best = None
        key = get_key(self.__state)
        if random() < self.__exploration:
            best = choice(list(self.__qtable[key]))  # une action au hasard
            self.__exploration *= 0.999
        else:
            for a in self.__qtable[key]:
                if not best \
                        or self.__qtable[key][a] > self.__qtable[key][best]:
                    best = a
        if best == DOWN:
            self.__actions[0] += 1
        elif best == LEFT:
            self.__actions[1] += 1
        elif best == RIGHT:
            self.__actions[2] += 1
        elif best == CHANGE:
            self.__actions[3] += 1
        return best

    def reset(self):
        self.__score = 0
        self.__score_break = 0
        self.__actions = [0, 0, 0, 0]

    def resetPosition(self):
        self.__position = (0, 4)
        self.__state = self.__environment.start

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.__qtable, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable = pickle.load(file)

    @property
    def qtable(self):
        return self.__qtable

    @property
    def actions(self):
        return self.__actions

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
    def score_break(self):
        return self.__score_break

    @score_break.setter
    def score_break(self, score):
        self.__score_break = score

    @property
    def exploration(self):
        return self.__exploration

    @exploration.setter
    def exploration(self, exploration):
        self.__exploration = exploration

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
