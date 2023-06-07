from gamestate_cards_actions_container import GameState
from gamestate_cards_actions_container import CardActionsPoolContainer

from game_ai_model import *

from unoplayer_unogame import *

from game_session_visualization import UNOVizualizer

import os, pickle

#import matplotlib.pyplot as plt
#import numpy as np

class AbortedSessionWrapper:
    def __init__(self, session_name):
        self.__game = UNOGame()
        self.__log = []
        self.__session_name = session_name
        
    def start_new_session(self, ai_names, human_names, nr_of_cards):
        self.__game.create_session_new_players(ai_names, nr_of_cards, human_player_names=human_names)
        self.__log = []
        self.save_2_log_state_file()
        
    def session_1_round(self):
        self.load_from_log_state_file()
        self.__game.process_turn(self.__log)
        self.save_2_log_state_file()
    
    def get_status(self):
        self.load_from_log_state_file()
        return self.__game.get_status()
    
    def save_2_log_state_file(self):
        data = {}
        
        data['log'] = self.__log
        data['game'] = self.__game.store_current_state()
        
        log_state_file_name = os.path.join("current_log", self.__session_name) + ".pickle"
        with open(log_state_file_name, "wb") as file:
            pickle.dump(data, file)
        log_file_name = os.path.join("log", self.__session_name) + ".pickle"
        with open(log_file_name, "wb") as file:
            pickle.dump(self.__log, file)
        
    def load_from_log_state_file(self):
        log_state_file_name = os.path.join("current_log", self.__session_name) + ".pickle"
        if os.path.exists(log_state_file_name):
            with open(log_state_file_name, "rb") as file:
                data = pickle.load(file)
                
                self.__game.load_current_state(data['game'])
                
                self.__log = data['log']
  
class SessionPlotVisuWrapper:
    def __init__(self, log, ai_names, human_names=[]):
        self.__log = log
        self.__ai_names = ai_names
        self.__human_names = human_names
        
    def plot_nr_of_cards(self):
        nr_of_cards_dict = {}
        all_names = self.__ai_names + self.__human_names
        for player_name in all_names:
            nr_of_cards_dict[player_name] = []
        for one_round in self.__log:
            for player_name in all_names:
                tmp_key_val = player_name + "_before"
                nr_of_cards = 0
                if (tmp_key_val in one_round.keys()):
                    nr_of_cards = \
                    len(one_round[tmp_key_val])
                nr_of_cards_dict[player_name].append(nr_of_cards)
                
        for player_name in nr_of_cards_dict.keys():
            plt.plot(nr_of_cards_dict[player_name])
        plt.legend(labels=nr_of_cards_dict.keys())
        plt.title("Me and my 3 Trained Bots in UNO")
        plt.xlabel("Played Rounds")
        plt.ylabel("Number of Cards in Hand")
        plt.show()
    def plot_nr_of_risk_cards(self):
        nr_taking_cards_vals = []
        for one_round in self.__log:
            value = one_round['state_before']\
            ['NrOfCardsTaking']
            
            nr_taking_cards_vals.append(value)
            
        plt.plot(nr_taking_cards_vals)
        plt.title("Amount of Aggressivity of the Playing Bots and Me")
        plt.xlabel("Played Rounds")
        plt.ylabel("Number of Risk Cards")
        plt.show()
    def plot_current_player_idxs(self):
        player_idx_vals = []
        for one_round in self.__log:
            value = one_round['state_before']\
            ['CurrentPlayerIndex']
            
            player_idx_vals.append(value)

        plt.plot(player_idx_vals)
        plt.title("Amount of Loving Skips and Turn Arounds of the Playing Bots")
        plt.xlabel("Played Rounds")
        plt.ylabel("Index of Current Player")
        plt.show()
    def create_session_simulation_frames(self):
        all_names = self.__ai_names + self.__human_names
        visu = UNOVizualizer(self.__log, all_names, \
             players_being_human=self.__human_names)
        is_continueing = True
        while (is_continueing):
            visu.draw(True)
            visu.draw(False)
            is_continueing = visu.next_log_frame()