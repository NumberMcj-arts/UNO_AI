import pickle, os
import numpy as np
from collections import defaultdict

from gamestate_cards_actions_container import GameState
from gamestate_cards_actions_container import CardActionsPoolContainer

##################################################
# Class for Training Parameters
###################################################
class TrainingParameters:
    def __init__(self, rewardLoseCard=10, rewardGetCard=-10, alpha=0.1, gamma=1):
        self.rewardLoseCard = rewardLoseCard
        self.rewardGetCard = rewardGetCard
        self.alpha = alpha
        self.gamma = gamma

##################################################
# Base Class for Game AI Model
###################################################
class UNOGameAIModel:
    def get_Q(self):
        raise NotImplementedError()
    def get_model_name(self):
        raise NotImplementedError()
    def get_instance_name(self):
        raise NotImplementedError()
    def store_training_results(self):
        raise NotImplementedError()
    def game_state_2_AI_state(self, cards_in_hand, game_state):
        raise NotImplementedError()
    def action_index_main_model_2_AI(self, action_index):
        raise NotImplementedError()
    def action_indices_AI_2_main_model(self, action_index_AI):
        raise NotImplementedError()
    def set_current_state(self, cards_in_hand, game_state):
        raise NotImplementedError()
    def get_rewards(self, possible_action_idxs):
        raise NotImplementedError()
    def update_action_reward(self, chosen_action_idx, nr_of_lost_cards):
        raise NotImplementedError()
    def update_state_from_state_to_reward(self):
        raise NotImplementedError()
    def get_total_nr_of_changed_rewards(self):
        raise NotImplementedError()
    def get_total_nr_of_changed_states(self):
        raise NotImplementedError()
        
##################################################
# Subclass for our first AI Model
###################################################
class UNOGameAIFirstModel(UNOGameAIModel):
    def __init__(self, instance_name,\
                 training_parameters=None):
        self.__name = "First Model"
        self.__instance_name = instance_name
        self.__card_actions_container = \
        CardActionsPoolContainer.get_instance()
        filename = os.path.join("../training_results", \
                                self.__name.replace(' ', '_'), \
                               self.__instance_name  + ".pickle")
        self.__total_nr_of_changed_rewards = 0
        # Actions:
        # ---------
        # take_card(s),
        # play_numbered
        # play_skip
        # play_turn_around
        # play_take_2
        # play_desire --> 4 values for the possible desired colors
        # play_desire_take_4 --> 4 values for the possible desired colors
        # ---------
        # ----> 13 possible actions
        if (os.path.exists(filename)):
            with open(filename, "rb") as file:
                self.__Q = defaultdict(lambda: np.zeros(13).astype(float), pickle.load(file))
            for state in self.__Q.keys():
                for reward in self.__Q[state]:
                    if (reward != 0):
                        self.__total_nr_of_changed_rewards += 1
        else:
            self.__Q = defaultdict(lambda: np.zeros(13).astype(float))
            
        self.__state_from = ""
        self.__state_to = ""
        self.__transition_action = None
        self.__transition_reward = None
        
        if (training_parameters is None):
            self.__training_params = TrainingParameters()
        # customized training parameters
        else:
            self.__training_params = training_parameters
        
    def get_Q(self):
        return self.__Q
    
    def get_model_name(self):
        return self.__name
    
    def get_instance_name(self):
        return self.__instance_name
    
    def store_training_results(self):
        path1 = os.path.join("../training_results", "")
        if not os.path.exists(path1):
            os.makedirs(path1)
        path2 = os.path.join("../training_results", \
                                self.__name.replace(' ', '_'))
        if not os.path.exists(path2):
            os.makedirs(path2)
        filename = os.path.join(path2,\
                               self.__instance_name  + ".pickle")
        with open(filename, "wb") as file:
            pickle.dump(dict(self.__Q), file)
        
    def game_state_2_AI_state(self, cards_in_hand, game_state):
        # State:
        # -----
        # number of cards in hand, values 0-10 and > 10 as 11th value
        # nr_of_taken_cards, values 0,2,4,6,8,10 and > 10 as 7th value
        # nr_of_special_cards (for each kind of special card)
        # in order: skips, turn_arounds, take_2s, color_desires, color_desires_take_4s
        # -
        # percentage of possible number cards
        # compress percentage in 10% intervals
        possible_action_idxs = self.__card_actions_container\
        .determine_possible_action_idxs(game_state,\
                                       cards_in_hand)
        
        nr_of_cards_in_hand = len(cards_in_hand)
        
        colored_special_card_names \
        = self.__card_actions_container.get_colored_special_cards()
        
        uncolored_special_card_names \
        = self.__card_actions_container.get_uncolored_special_cards()
        
        colored_special_card_counts = {}
        for name in colored_special_card_names:
            colored_special_card_counts[name] = 0
            
        uncolored_special_card_counts_tmp = {}
        uncolored_special_card_counts = {}
        for name in uncolored_special_card_names:
            uncolored_special_card_counts_tmp[name] = 0
            uncolored_special_card_counts[name] = 0
            
        possible_numbers_count = 0
        
        only_take_cards = len(possible_action_idxs) == 1
        only_take_cards = only_take_cards \
        and (self.__card_actions_container\
        .get_index_of_action("take:cards:from_stack")
            == possible_action_idxs[0])
        
        if (not only_take_cards):
        
            for possible_action_index in possible_action_idxs:
                action_description = \
                self.__card_actions_container\
                .get_action_on_index(possible_action_index)

                if (action_description != "take:cards:from_stack"):
                
                    if (action_description.split(":")[2] \
                        == "desired_color"):
                        uncolored_special_card_counts_tmp\
                        [action_description.split(":")[1]] += 1
                    else:
                        card_value = action_description\
                        .split(":")[2]

                        if (card_value.isdigit()):
                            possible_numbers_count += 1
                        else:
                            colored_special_card_counts\
                            [card_value] += 1

            for card_index in cards_in_hand:
                card_description = \
                self.__card_actions_container\
                .get_card_on_index(card_index)

                if (card_description.split(":")[1] == "nr"):
                    uncolored_special_card_name\
                    = card_description.split(":")[0]

                    if (uncolored_special_card_counts_tmp\
                        [uncolored_special_card_name] > 0):
                        uncolored_special_card_counts\
                        [uncolored_special_card_name] += 1
                    
        # number of cards in hand, values 0-10 and > 10 as 11th value
        # nr_of_taken_cards, values 0,2,4,6,8,10 and > 10 as 7th value
        # nr_of_special_cards (for each kind of special card)
        # in order: skips, turn_arounds, take_2s, color_desires, color_desires_take_4s
        # -
        # percentage of possible number cards
        # compress percentage in 10% intervals
        percentage_params = []
        percentage_compression_interval = 10
        
        percentage_params.append(possible_numbers_count)
        
        curr_nr_of_taking_cards = game_state.get_number_of_cards_taking()
        
        if (nr_of_cards_in_hand <= 10):
            state = (str(nr_of_cards_in_hand) + "-")
        else:
            state = ("M-")
        
        if (curr_nr_of_taking_cards <= 10):
            state += (str(curr_nr_of_taking_cards) + "-")
        else:
            state += ("M-")
        
        state += (str(colored_special_card_counts["skip"]) + "-")
        state += (str(colored_special_card_counts["turn_around"]) + "-")
        state += (str(colored_special_card_counts["take_2"]) + "-")
        state += (str(uncolored_special_card_counts["color_desire"]) + "-")
        state += (str(uncolored_special_card_counts["take_4"]) + "-")
        
        for param in percentage_params:
            value = int(100. * float(param) / float(nr_of_cards_in_hand))
            value = \
            int(int(value / percentage_compression_interval) \
                * percentage_compression_interval)

            state += (str(value) + "-")
        
        state = state[:len(state)-1]
        
        return state
    
    # Actions:
    # ---------
    # 0: take_card(s),
    # 1: play_numbered
    # 2: play_skip
    # 3: play_turn_around
    # 4: play_take_2
    # 5-8: color_desire --> 4 values for the possible desired colors
    # 9-12: color_desire_take_4 --> 4 values for the possible desired colors
    def action_index_main_model_2_AI(self, action_index):
        action_description = \
        self.__card_actions_container\
        .get_action_on_index(action_index)
        
        if (action_description == "take:cards:from_stack"):
            action_index_AI = 0
        else:
            if (action_description.split(":")[2] == "desired_color"):
                colors = self.__card_actions_container.get_colors()
                desired_color = action_description.split(":")[3]
                desired_color_idx = colors.index(desired_color)
                if (action_description.split(":")[1] == "color_desire"):
                    action_idx_offset = 5
                elif (action_description.split(":")[1] == "take_4"):
                    action_idx_offset = 9
                action_index_AI = action_idx_offset + desired_color_idx
            else:
                card_value = action_description\
                    .split(":")[2]
                
                if (card_value.isdigit()):
                    action_index_AI = 1
                elif (card_value == "skip"):
                    action_index_AI = 2
                elif (card_value == "turn_around"):
                    action_index_AI = 3
                elif (card_value == "take_2"):
                    action_index_AI = 4
                    
        return action_index_AI
                
    def action_indices_AI_2_main_model(self, action_index_AI):
        
        action_indices_main_model = []
        
        colors = self.__card_actions_container.get_colors()
        
        if (action_index_AI == 0):
            action_index_main = \
            self.__card_actions_container\
            .get_index_of_action("take:cards:from_stack")
            
            action_indices_main_model\
            .append(action_index_main)

        elif (action_index_AI == 1):
            for number in range(10):
                value = str(number)
                for color in colors:
                    action_description = "play:"
                    action_description += color + ":"
                    action_description += value
                    
                    action_index_main = \
                    self.__card_actions_container\
                    .get_index_of_action(action_description)

                    action_indices_main_model\
                    .append(action_index_main)
                    
        elif ((action_index_AI >= 2)
             and (action_index_AI <= 4)):
            if (action_index_AI == 2):
                value = "skip"
            elif (action_index_AI == 3):
                value = "turn_around"
            elif (action_index_AI == 4):
                value = "take_2"
            for color in colors:
                action_description = "play:"
                action_description += color + ":"
                action_description += value
                
                action_index_main = \
                self.__card_actions_container\
                .get_index_of_action(action_description)

                action_indices_main_model\
                .append(action_index_main)
        
        elif ((action_index_AI >= 5)
            and (action_index_AI <= 12)):
            if ((action_index_AI >= 5)
             and (action_index_AI <= 8)):
                value = "color_desire"
                color_idx_offset = 5
            elif ((action_index_AI >= 9)
             and (action_index_AI <= 12)):
                value = "take_4"
                color_idx_offset = 9
            
            desired_color = \
            colors\
            [action_index_AI\
                  - color_idx_offset]
            
            action_description = "play:"
            action_description += value + ":desired_color:"
            action_description += desired_color

            action_index_main = \
            self.__card_actions_container\
            .get_index_of_action(action_description)

            action_indices_main_model\
            .append(action_index_main)
        
        return action_indices_main_model
    
    def set_current_state(self, cards_in_hand, game_state):
        self.__state_from = self.__state_to
        self.__state_to = self\
        .game_state_2_AI_state(cards_in_hand,\
                              game_state)
    
    def get_rewards(self, possible_action_idxs):
        rewards = self.__Q[self.__state_to]
        returned_rewards = []
        for possible_action_index in possible_action_idxs:
            possible_action_idx_AI = self\
            .action_index_main_model_2_AI(possible_action_index)
            
            returned_rewards.append(rewards[possible_action_idx_AI])
            
        return returned_rewards
    
    def update_action_reward(self, chosen_action_idx, nr_of_lost_cards):
        self.__transition_action = self.\
        action_index_main_model_2_AI(chosen_action_idx)
        if (nr_of_lost_cards < 0):
            reward = self.__training_params\
            .rewardGetCard * np.abs(nr_of_lost_cards)
        else:
            reward = self.__training_params\
            .rewardLoseCard * np.abs(nr_of_lost_cards)
        self.__transition_reward = reward
        
    def update_state_from_state_to_reward(self):
        if (self.__state_from != ""):
            estimated_reward = self.__Q[self.__state_to]
            
            prev_reward = self.__Q[self.__state_from]
            
            if (prev_reward[self.__transition_action]\
               == 0):
                self.__total_nr_of_changed_rewards += 1
            
            prev_reward[self.__transition_action] = \
            (1 - self.__training_params.alpha) \
            * prev_reward[self.__transition_action] + \
                self.__training_params.alpha \
            * (self.__transition_reward \
               + self.__training_params.gamma * max(estimated_reward))
            self.__Q[self.__state_from] = prev_reward
            
    def get_total_nr_of_changed_rewards(self):
        return self.__total_nr_of_changed_rewards
    def get_total_nr_of_changed_states(self):
        return len(self.__Q.keys())
    
##################################################
# Game AI Model Factory Class
###################################################
class UNOGameAIModelFactory:
    @staticmethod
    def get_instance(ai_model_name, \
                     instance_name,\
                     training_parameters=None):
        if (ai_model_name == "First Model"):
            return UNOGameAIFirstModel(instance_name,\
                                      training_parameters)