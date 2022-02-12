if new_position in self.__states:
    self.__round_ended = False
    reward = 0
    if self.__board[new_position] == BORDER:
        reward += REWARD_BORDER
        new_position = position
    elif self.__board[new_position] == GROUND:
        reward, new_position = self.perform_ground_reached(agent, column)
    elif self.__board[new_position] != EMPTY:
        # previous_position_cell_down = self.__states[(agent.state[0] + 1, agent.state[1])][1][0]
        current_column_row_position = agent.position[0]
        if current_column_row_position < 2:
            new_position = agent.position
            reward = REWARD_LOSE
            self.__lost = True
            print("Lost")
        elif action == RIGHT or action == LEFT:
            new_position = agent.position
            reward = REWARD_BORDER
        else:
            new_position = agent.position
            if action == DOWN:
                reward += self.perform_round_ended(column, new_position)
    else:
        if self.__change_counter == 3:  # reset to first order and move by one step to down in order to force IA to not dot it every time
            self.__change_counter = 0
            reward += REWARD_CHANGE
else:
    reward = REWARD_LOSE
# set_Colunm_in_board(self.__board, position, column)
# self.__previous_pos = position
agent.update(self.__states.get(position), action, reward)
self.update_position_and_column__states(self.__board, new_position)
agent.position = new_position
return reward

best_actions = [DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, LEFT, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, RIGHT,
                        DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN,
                        DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN,
                        DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN,
                        DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN,
                        DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN,
                        DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN, DOWN]
        i = 0
        while not env.isLost:
            agent.resetPosition()
            env.is_round_ended = False
            agent.column = [1, 2, 2]
            while not env.is_round_ended:
                action = best_actions[i]
                i += 1
                if action == DOWN:
                    actions[0] += 1
                elif action == LEFT:
                    actions[1] += 1
                elif action == RIGHT:
                    actions[2] += 1
                elif action == CHANGE:
                    actions[3] += 1
                env.apply(agent, action)