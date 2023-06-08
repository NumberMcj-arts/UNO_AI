import numpy as np

from gamestate_cards_actions_container import GameState
from gamestate_cards_actions_container import CardActionsPoolContainer
from game_ai_model import *

##################################################
# Class for One UNO Player
###################################################
class UNOPlayer:
    def __init__(self, name,\
                ai_model_name="First Model",\
                is_human=False):
        self.__name = name
        self.__card_actions_container = \
        CardActionsPoolContainer.get_instance()
        self.__initialized = False
        self.__card_idxs_on_hand = []
        if (not is_human):
            self.__ai_model = UNOGameAIModelFactory.get_instance(ai_model_name,\
                                                                name)
            self.__used_onTurn_method = self.onTurn_AI
        else:
            self.__ai_model = None
            self.__used_onTurn_method = self.onTurn_IO
        
        self.__is_human = is_human
    
    def store_current_state(self):
        data = {}
        data['name'] = self.__name
        data['initialized'] = self.__initialized
        data['card_idxs_in_hand'] = self.__card_idxs_on_hand
        if (self.__ai_model is None):
            data['ai_model_name'] = ''
        else:
            data['ai_model_name'] = self.__ai_model.get_model_name()
        
        return data
        
    def load_current_state(self, data):
        self.__card_actions_container = \
        CardActionsPoolContainer.get_instance()
        self.__name = data['name']
        self.__initialized = data['initialized']
        self.__card_idxs_on_hand = data['card_idxs_in_hand']
        ai_model_name = data['ai_model_name']
        
        if (ai_model_name == ''):
            self.__ai_model = None
            self.__is_human = True
            self.__used_onTurn_method = self.onTurn_IO
        else:
            self.__ai_model = UNOGameAIModelFactory.get_instance(ai_model_name,\
                                                                self.__name)
            self.__is_human = False
            self.__used_onTurn_method = self.onTurn_AI
    
    def get_AI_model(self):
        return self.__ai_model
        
    def is_human_player(self):
        return self.__is_human
        
    def initialize(self, card_idxs):
        self.__card_idxs_on_hand = card_idxs
        self.__initialized = True
        
    def is_inilialized(self):
        return self.__initialized
    def get_name(self):
        return self.__name
    def get_card_idxs_on_hand(self):
        return self.__card_idxs_on_hand
    
    def cards_on_hand_to_string(self):
        text = "Player " + self.__name\
        + "\n"
        text += 20 * "-" + "\n"
        for i, card_index \
        in enumerate(self.__card_idxs_on_hand):
            text += str(i + 1)
            text += ".: "
            text += self.__card_actions_container\
            .get_card_on_index(card_index)
            text += "\n"
        text += 20 * "+"
        return text
    
    def cards_on_hand_to_string_list(self):
        text_list = []
        for card_index \
        in self.__card_idxs_on_hand:
            text = self.__card_actions_container\
            .get_card_on_index(card_index)
            text_list.append(text)
        return text_list
    
    def add_card(self, card_index):
        self.__card_idxs_on_hand.append(card_index)
    def remove_card(self, card_index):
        self.__card_idxs_on_hand.remove(card_index)
        
    def has_any_cards_left(self):
        return len(self.__card_idxs_on_hand)\
                > 0
        
    def determine_possible_cards(self, \
                                 chosen_action_idx):
        
        action_2_cards = self.__card_actions_container\
        .get_action_2_cards()
        
        my_possible_cards = []
        for possible_card_idx \
        in action_2_cards[str(chosen_action_idx)]:
            # if I have this possible card
            if (possible_card_idx in self.__card_idxs_on_hand):
                my_possible_cards.append(possible_card_idx)
                
        return my_possible_cards
        
    def choose_randomly(self, values, rewards):
        p_rewards = np.asarray(rewards)
        p_rewards = np.exp(p_rewards) \
                    / np.sum(np.exp(p_rewards))
        chosen_value = np.random.choice(values,\
                                       p=p_rewards)
        return chosen_value
      
    def onTurn(self, state):
        return self.__used_onTurn_method(state)
    
    def get_status(self, state):
    
        possible_action_idxs \
        = self.__card_actions_container\
        .determine_possible_action_idxs(state,\
                                       self.__card_idxs_on_hand)
    
        status = {'possible_actions': [],
            'cards_on_hand': self.cards_on_hand_to_string_list()
        }
        
        if (self.is_human_player()):
            for i, possible_action in enumerate(possible_action_idxs):
                action_name = self.__card_actions_container\
                .get_action_on_index(possible_action) + "\n"
                
                status['possible_actions'].append(action_name)
        #else:
        #    status = "AI muhahah"
            
            
        return status
    
    def onTurn_AI(self, state):
        possible_action_idxs \
        = self.__card_actions_container\
        .determine_possible_action_idxs(state,\
                                       self.__card_idxs_on_hand)
        
        # update state_to of AI model
        self.__ai_model\
        .set_current_state(self.__card_idxs_on_hand, \
                           state)
        # update reward of previous state if this
        # state exists already
        self.__ai_model.update_state_from_state_to_reward()
        # get rewards from AI
        rewards = self.__ai_model.get_rewards(possible_action_idxs)
        # choose randomly
        chosen_action_idx = self.choose_randomly(possible_action_idxs,\
                       rewards)
        # determine possible cards of action
        possible_cards_for_action = self\
        .determine_possible_cards(chosen_action_idx)
        return chosen_action_idx, possible_cards_for_action
    
    def onTurn_IO(self, state):
        possible_action_idxs \
        = self.__card_actions_container\
        .determine_possible_action_idxs(state,\
                                       self.__card_idxs_on_hand)
        
        io_request_message = ""
        for i, possible_action in enumerate(possible_action_idxs):
            io_request_message += "Type " + str(i)
            io_request_message += " for "
            io_request_message += self.__card_actions_container\
            .get_action_on_index(possible_action) + "\n"
        wrong_key = True
        while (wrong_key):
        
            chosen_index = input(io_request_message)
        
            if (chosen_index.isdigit()):
                chosen_index = int(chosen_index)
                if ((chosen_index >= 0)
                   and (chosen_index < len(possible_action_idxs))):
                    wrong_key = False
        chosen_action = possible_action_idxs[chosen_index]
        
        # determine possible cards of action
        possible_cards_for_action = self\
        .determine_possible_cards(chosen_action)
        return chosen_action, possible_cards_for_action
    
    def update_action_reward(self, chosen_action_idx, nr_of_lost_cards):
        if (self.__ai_model is not None):
            self.__ai_model\
            .update_action_reward(chosen_action_idx, nr_of_lost_cards)
            
##################################################
# Class for one UNO Game Session
###################################################
class UNOGame:
    def __init__(self):
        self.__card_actions_container = \
        CardActionsPoolContainer.get_instance()
        self.__cards = \
        np.arange(0,\
                  len(self.__card_actions_container.get_card_pool()))
        np.random.shuffle(self.__cards)
        self.__cards = list(self.__cards)
        self.__players = []
        self.__state = GameState()
        self.__only_AIs = True
    
    def store_current_state(self):
        data = {}
        data['players'] = []
        for player in self.__players:
            players_State = player.store_current_state()
            data['players'].append(players_State)
        data['cards'] = self.__cards
        data['gamestate'] = self.__state
        data['only_AIs'] = self.__only_AIs
        
        return data
    def load_current_state(self, data):
        self.__players = []
        for data_player in data['players']:
            new_player = UNOPlayer("TBD")
            new_player.load_current_state(data_player)
            self.__players.append(new_player)
        self.__cards = data['cards']
        self.__state = data['gamestate']
        self.__only_AIs = data['only_AIs']
    
    def create_session_new_players(self, player_names, nr_of_cards,\
                                  human_player_names=[]):
        for player_name in player_names:
            new_player = UNOPlayer(player_name)
            cards_for_player = []
            for i in range(nr_of_cards):
                cards_for_player.append(self.__cards.pop(0))
            new_player.initialize(cards_for_player)
            self.__players.append(new_player)
        if (human_player_names != []):
            for human_player_name in human_player_names:
                new_player = UNOPlayer(human_player_name,\
                                      is_human=True)
                cards_for_player = []
                for i in range(nr_of_cards):
                    cards_for_player.append(self.__cards.pop(0))
                new_player.initialize(cards_for_player)
                self.__players.append(new_player)
            
            self.__only_AIs = False
            
        self.__state = \
        self.__card_actions_container\
        .initialize_state_from_card_on_top(self.__cards[0],\
                                          len(self.__players))
    
    def get_status(self):
        
        status = {}
    
        if (len(self.__players) > 0):
        
            curr_player_idx = self.__state.get_curr_player_idx()
            curr_player = self.__players[curr_player_idx]
            
            status['current_player'] = curr_player
            
            status['state_before'] = self.__state.to_dict()
            status['card_on_top'] = \
            self.__card_actions_container\
                .get_card_on_index(self.__cards[0])
            
            if (not self.__only_AIs):
                status.update(self.__state.to_dict())
            
            status['curr_player_state'] = curr_player.get_status(self.__state)
            
        return status
    
    def process_turn(self, log=None, ai_log=None):
        
        if (len(self.__players) > 0):
        
            curr_player_idx = self.__state.get_curr_player_idx()
            curr_player = self.__players[curr_player_idx]
            
            turn_information = {}
            turn_information['state_before'] = self.__state.to_dict()
            turn_information['card_on_top_before'] = \
            self.__card_actions_container\
                .get_card_on_index(self.__cards[0])
            
            if (not self.__only_AIs):
                print(self.__state.to_string_compact())
                print("Card on Top: " + turn_information['card_on_top_before'])
                print(20 * "-")
            
            for player in self.__players:
                cards = player.cards_on_hand_to_string_list()
                if (not self.__only_AIs):
                    if (curr_player.get_name() == player.get_name()):
                        print("->")
                    print("Player " + player.get_name() + ": " + str(len(cards)) + " cards")
                    if (player.is_human_player()):
                        print(player.cards_on_hand_to_string())
                turn_information[player.get_name() + "_before"]\
                = cards
            
            if (curr_player.is_human_player()):
                chosen_action_idx, possible_cards_for_action\
                = curr_player.onTurn_IO(self.__state)
            else:
                chosen_action_idx, possible_cards_for_action\
                = curr_player.onTurn(self.__state)
            
            turn_information['used_action'] = \
            self.__card_actions_container\
                  .get_action_on_index(chosen_action_idx)

            if (not self.__only_AIs):
                print(curr_player.get_name() + " uses " + turn_information['used_action'])
            
            # losing :p
            if (self.__card_actions_container.\
               get_index_of_action("take:cards:from_stack")\
               == chosen_action_idx):
                nr_of_cards_taking = \
                self.__state.get_number_of_cards_taking()

                if (nr_of_cards_taking == 0):
                    nr_of_cards_taking = 1

                for i in range(nr_of_cards_taking):
                    curr_player.add_card(self.__cards.pop(-1))

                reward = - nr_of_cards_taking
            # winning :D
            else:
                choosed_card_for_action =\
                np.random.choice(possible_cards_for_action)

                self.__cards.insert(0, choosed_card_for_action)
                curr_player.remove_card(choosed_card_for_action)

                reward = 1

            last_player_idx = curr_player_idx

            turn_information['reward'] = reward
            tmp_key_val = self.__players[last_player_idx]\
            .get_name() + "_after"
            
            if (ai_log is not None):
                if (ai_log == {}):
                    for player in self.__players:
                        log_player = {"nr_changed_states": [],
                                     "nr_changed_rewards": []}
                        ai_log[player.get_name()] = log_player
                
                ai_log_player = self.__players[last_player_idx]
                
                ai_model = ai_log_player.get_AI_model()
                
                nr_of_changed_rewards = \
                ai_model.get_total_nr_of_changed_rewards()
                nr_of_changed_states = \
                ai_model.get_total_nr_of_changed_states()
                
                player_name = ai_log_player.get_name()
                
                ai_log[player_name]["nr_changed_states"]\
                .append(nr_of_changed_states)
                
                ai_log[player_name]["nr_changed_rewards"]\
                .append(nr_of_changed_rewards)
            
            turn_information[tmp_key_val] = self\
            .__players[last_player_idx]\
            .cards_on_hand_to_string_list()
            
            curr_player.update_action_reward(chosen_action_idx,
                                            reward)
            self.__state = \
            self.__card_actions_container\
            .determine_new_state_after_action(self.__state,\
                                             chosen_action_idx,\
                                             len(self.__players))
            # if last player won
            if (not self.__players[last_player_idx].has_any_cards_left()):
                self.__players[last_player_idx]\
                .get_AI_model().store_training_results()
                del self.__players[last_player_idx]
                # shift index if necessary
                if (self.__state.get_curr_player_idx()\
                   > last_player_idx):
                    self.__state.decrease_curr_player_index()
                # if just one player is left then the
                # game is finished
                if (len(self.__players) == 1):
                    self.__players = []
            
            turn_information['state_after'] = self.__state.to_dict()
            turn_information['card_on_top_after'] = \
            self.__card_actions_container\
                .get_card_on_index(self.__cards[0])
            
            if (log is not None):
                log.append(turn_information)
            
        else:
            print("Game finished")
        
    def get_curr_player(self):
        curr_player_idx = self.__state.get_curr_player_idx()
        return self.__players[curr_player_idx]
    
    def is_game_finished(self):
        return (len(self.__players) == 0)