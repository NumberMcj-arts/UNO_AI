import numpy as np

##################################################
# GameState Class
###################################################
class GameState:
    def __init__(self,\
                necessary_value="",\
                necessary_color="",\
                number_of_cards_taking=0,\
                is_direction_forward=True,\
                curr_player_index=0):
        self.__necessary_value = necessary_value
        self.__necessary_color = necessary_color
        self.__number_of_cards_taking = number_of_cards_taking
        self.__is_direction_forward = is_direction_forward
        self.__curr_player_index = curr_player_index
    
    def set_values_of_other_state(self, other):
        self.__necessary_value = other.get_necessary_value()
        self.__necessary_color = other.get_necessary_color()
        self.__number_of_cards_taking = other.get_number_of_cards_taking()
        self.__is_direction_forward = other.is_direction_forward()
        self.__curr_player_index = other.get_curr_player_idx()
    
    def get_necessary_value(self):
        return self.__necessary_value
    def get_necessary_color(self):
        return self.__necessary_color
    def get_number_of_cards_taking(self):
        return self.__number_of_cards_taking
    def is_direction_forward(self):
        return self.__is_direction_forward
    def get_curr_player_idx(self):
        return self.__curr_player_index
    
    def decrease_curr_player_index(self):
        self.__curr_player_index -= 1
    
    def increase_nr_of_cards_taking(self, value):
        self.__number_of_cards_taking += value
    def reset_nr_of_cards_taking(self):
        self.__number_of_cards_taking = 0
        
    def set_value_color(self, value, color):
        self.__necessary_value = value
        self.__necessary_color = color
        
    def invert_playing_direction(self):
        self.__is_direction_forward = \
        not self.__is_direction_forward
        
    def next_player(self, nr_of_players, skip=False):
        diff = 1
        if (skip):
            diff *= 2
        if (not self.__is_direction_forward):
            diff = - diff
        self.__curr_player_index = \
        (self.__curr_player_index + diff) \
        % nr_of_players
        
    def to_string(self):
        text = "Current Player Index: "\
        + str(self.__curr_player_index)\
        + "\n"
        
        text += "Necessary Value: "\
        + self.__necessary_value\
        + "\n"
        
        text += "Necessary Color: "\
        + self.__necessary_color\
        + "\n"
        
        text += "Number of Cards Taking: "\
        + str(self.__number_of_cards_taking)\
        + "\n"
        
        if (self.__is_direction_forward):
            text += "Forward"
        else:
            text += "Backward"
        text += " Playing Direction"
        
        return text
    
    def to_dict(self):
        
        dict_params = {
            "CurrentPlayerIndex":self.__curr_player_index,
            "NecessaryValue":self.__necessary_value,
            "NecessaryColor":self.__necessary_color,
            "NrOfCardsTaking":self.__number_of_cards_taking,
            "IsForwardPlayingDirection":self.__is_direction_forward
        }
        
        return dict_params
    
    def to_string_compact(self):
        text = "to_match: "
        text += self.__necessary_value
        text += " in " + self.__necessary_color
        text += "\n"
        text += "Cards +" + str(self.__number_of_cards_taking)
        text += ";"
        if (self.__is_direction_forward):
            text += "-->"
        else:
            text += "<--"
        return text
    
    def is_equal_to(self, other):
        
        is_equal = \
        (self.__necessary_value == other.get_necessary_value())
        
        is_equal = is_equal and \
        (self.__necessary_color == other.get_necessary_color())
        
        is_equal = is_equal and \
        (self.__number_of_cards_taking == other.get_number_of_cards_taking())
        
        is_equal = is_equal and \
        (self.__is_direction_forward == other.is_direction_forward())
        
        is_equal = is_equal and \
        (self.__curr_player_index == other.get_curr_player_idx())
        
        return is_equal

# implemented as singleton
# so now no other class needs
# a reference to an object
# of this class anymore
# hurrraaaaaaaaay :D
# paaaaaaaartyyyyyy :D

##################################################
# CardActionsPoolContainer Class
###################################################
class CardActionsPoolContainer:
    
    instance = None
    
    def __init__(self):
        self.__colors = ["yellow", "blue", "green", "red"]
        self.__colored_special_cards = ["skip", "take_2", "turn_around"]
        self.__uncolored_special_cards = ["color_desire", "take_4"]

        self.__card_pool = []
        self.__actions_pool = []
        self.__action_2_cards = {}
        for color in self.__colors:
            for i in range(10):
                self.__card_pool.append(color + ":" + str(i))
                self.__actions_pool.append("play:" + color + ":" + str(i))
                inserted_list_idx = len(self.__actions_pool) - 1
                self.__action_2_cards[str(inserted_list_idx)] = [inserted_list_idx]
            for colored_special_card in self.__colored_special_cards:
                self.__card_pool.append(color + ":" + colored_special_card)
                self.__actions_pool.append("play:" + color + ":" + colored_special_card)
                inserted_list_idx = len(self.__actions_pool) - 1
                self.__action_2_cards[str(inserted_list_idx)] = [inserted_list_idx]
        for uncolored_special_card in self.__uncolored_special_cards:
            indices = []
            for i in range(len(self.__colors)):
                self.__card_pool.append(uncolored_special_card + ":nr:" + str(i + 1))
                self.__actions_pool\
                .append("play:" + uncolored_special_card \
                        + ":desired_color:" \
                        + self.__colors[i])
                inserted_list_idx = len(self.__actions_pool) - 1
                indices.append(inserted_list_idx)
            for index in indices:
                action_index_keyval = str(index)
                self.__action_2_cards[action_index_keyval]\
                = indices[:]
        self.__actions_pool.append("take:cards:from_stack")
        inserted_list_idx = len(self.__actions_pool) - 1
        self.__action_2_cards[str(inserted_list_idx)] = []
      
    # this is the method to call
    @staticmethod
    def get_instance():
        if (CardActionsPoolContainer.instance is None):
            CardActionsPoolContainer.instance =\
            CardActionsPoolContainer()
        return CardActionsPoolContainer.instance
    
    def get_colors(self):
        return self.__colors
    def get_colored_special_cards(self):
        return self.__colored_special_cards
    def get_uncolored_special_cards(self):
        return self.__uncolored_special_cards
    def get_card_on_index(self, index):
        return self.__card_pool[index]
    def get_index_of_card(self, card):
        return self.__card_pool.index(card)
    def get_action_on_index(self, index):
        return self.__actions_pool[index]
    def get_index_of_action(self, action):
        return self.__actions_pool.index(action)
    
    def get_card_pool(self):
        return self.__card_pool
    def get_actions_pool(self):
        return self.__actions_pool
        
    def get_action_2_cards(self):
        return self.__action_2_cards
        
    def print_action_2_cards(self):
        for action_idx in self.__action_2_cards.keys():
            print("Action " \
                  + self.get_action_on_index(int(action_idx)))
            print(20 * "-")
            for card_idx in self.__action_2_cards[str(action_idx)]:
                print("Card " + self.get_card_on_index(card_idx))
            print(20 * "+")
        
    def determine_possible_action_idxs(self, state, card_idxs_on_hand):
        possible_action_idxs = []
        for card_index_on_hand in card_idxs_on_hand:
            # case take_4
            if ("take_4" in self.get_card_on_index(card_index_on_hand)):
                for color in self.__colors:
                    action_name = "play:take_4:desired_color:" + color
                    action_index = self.get_index_of_action(action_name)
                    if not action_index in possible_action_idxs:
                        possible_action_idxs.append(action_index)
            # case color_desire
            if ("color_desire" in self.get_card_on_index(card_index_on_hand)):
                if ((state.get_number_of_cards_taking() < 1)):
                    for color in self.__colors:
                        action_name = "play:color_desire:desired_color:" + color
                        action_index = self.get_index_of_action(action_name)
                        if not action_index in possible_action_idxs:
                            possible_action_idxs.append(action_index)
            # case take_2
            if ("take_2" in self.get_card_on_index(card_index_on_hand)):
                card_color = self.get_card_on_index(card_index_on_hand)\
                .split(":take_2")[0]
                if ((state.get_necessary_color() == card_color)
                   or (state.get_necessary_value() == "take_2")):
                    action_name = "play:"\
                    + card_color + ":take_2"
                    action_index = self.get_index_of_action(action_name)
                    possible_action_idxs.append(action_index)
            # other cases: if nr_of_cards_taking < 1
            elif (state.get_number_of_cards_taking() < 1):
                full_card_name = self.get_card_on_index(card_index_on_hand)
                card_value = full_card_name.split(":")[1]
                card_color = full_card_name.split(":")[0]
                if ((state.get_necessary_value() == card_value)
                   or (state.get_necessary_color() == card_color)):
                    action_name = "play:" + card_color + ":" + card_value
                    action_index = self.get_index_of_action(action_name)
                    possible_action_idxs.append(action_index)
        possible_action_idxs.append(self.get_index_of_action('take:cards:from_stack'))
        return possible_action_idxs
    
    def determine_new_state_after_action(self, prev_state, chosen_action, nr_of_players):
        new_state = GameState()
        new_state.set_values_of_other_state(prev_state)
        
        skip = False
        
        # case card(s) taken
        if (chosen_action == self.get_index_of_action('take:cards:from_stack')):
            new_state.reset_nr_of_cards_taking()
        # case play take 4
        elif ("take_4" in self.get_action_on_index(chosen_action)):
            value = "take_4"
            color = self.get_action_on_index(chosen_action)\
            .split(":")[3]
            new_state.set_value_color(value, color)
            new_state.increase_nr_of_cards_taking(4)
        # case play color desire
        elif ("color_desire" in self.get_action_on_index(chosen_action)):
            value = "color_desire"
            color = self.get_action_on_index(chosen_action)\
            .split(":")[3]
            new_state.set_value_color(value, color)
        # case play colored card
        else:
            action_description = self.get_action_on_index(chosen_action)
            
            value = action_description.split(":")[2]
            color = action_description.split(":")[1]
            
            new_state.set_value_color(value, color)
            
            if (value == "take_2"):
                new_state.increase_nr_of_cards_taking(2)
            elif (value == "skip"):
                skip = True
            elif (value == "turn_around"):
                new_state.invert_playing_direction()
        
        new_state.next_player(nr_of_players, skip=skip)
        
        return new_state
    
    def initialize_state_from_card_on_top(self, card_on_top, nr_of_players):
        new_state = GameState()
        
        # case take 4
        if ("take_4" in self.get_card_on_index(card_on_top)):
            value = "take_4"
            color = np.random.choice(self.__colors)
            new_state.set_value_color(value, color)
            new_state.increase_nr_of_cards_taking(4)
        # case color desire
        elif ("color_desire" in self.get_card_on_index(card_on_top)):
            value = "color_desire"
            color = np.random.choice(self.__colors)
            new_state.set_value_color(value, color)
        # case colored card
        else:
            card_description = self.get_card_on_index(card_on_top)
            
            value = card_description.split(":")[1]
            color = card_description.split(":")[0]
            
            new_state.set_value_color(value, color)
            
            if (value == "take_2"):
                new_state.increase_nr_of_cards_taking(2)
            elif (value == "skip"):
                new_state.next_player(nr_of_players)
            elif (value == "turn_around"):
                new_state.invert_playing_direction()
        
        return new_state