# zack
# yesssss
# visualization :D

# visualization :D B-)

# methods to use:
# noooooo
# much easier from log data tse tse
# --------------
# 1. onPlayerOnTurnChanged
# 2. onPlayerLoseCard
# 3. onPlayerGetCards
# 4. add_cards_player
# 5. add_players
# 6. onCardOnTop
# 7. onCardsTakenChanged
# 8. onDirectionChanged
# 9. onTurnNumberIncremented
# 10. ----> and call draw cyclic
# no, just read it from the fucking log_data tseeee
# tseeee tseeeee

from PIL import ImageFont, ImageDraw, Image
import numpy as np

from gamestate_cards_actions_container import GameState
from gamestate_cards_actions_container import CardActionsPoolContainer

class UNOVizualizer:
    
    def __init__(self, log_data,\
                 players, players_being_human=[]):
        
        self.__style_images_path = "../ressources/"
        self.__curr_background_file = (self.__style_images_path + "background_robot.jpg")
        
        self.__simulation_file_names_format = "../simulation_frames/round_%04d.jpg"
        
        self.__log_data = log_data
        self.__curr_log_data_index = 0
        self.__card_actions_container = \
        CardActionsPoolContainer.get_instance()
        self.__players = players
        self.__players_being_human = players_being_human
        
        self.__frame_number = 0
    
    def draw_text(self, draw, text, x, y, w, h, color_fill="red"):
        fontsize = 1
        font = ImageFont.truetype("arial.ttf", fontsize)
        while (font.getsize(text)[0] < w) and (font.getsize(text)[1] < h):
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype("arial.ttf", fontsize)
        draw.text((x, y), text, font=font, fill=color_fill) # put the text on the image
    
    def draw_arrow_horizontal(self, draw, x, y, w, h, right_direction, fill=False):
        # draw the arrow lines
        # 7 lines
        # ++++++++
        
        x_vals = []
        y_vals = []
        
        # 1. bottom line
        
        if (right_direction):
            x_vals.append(int(x))
            x_vals.append(int(x))
        else:
            x_vals.append(int(x + w))
            x_vals.append(int(x + w))
        
        y_vals.append(int(y + h / 4))
        y_vals.append(int(y + 3 * h / 4))
        
        # 2. first half-length line
        
        if (right_direction):
            x_vals.append(x)
            x_vals.append(int(x + w / 2))
        else:
            x_vals.append(int(x + w))
            x_vals.append(int(x + w / 2))
        
        y_vals.append(int(y + 3 * h / 4))
        y_vals.append(int(y + 3 * h / 4))
        
        # 3. first half bottom line
        
        y_vals.append(int(y + 3 * h / 4))
        y_vals.append(int(y + h))
        
        x_vals.append(int(x + w / 2))
        x_vals.append(int(x + w / 2))
        
        # 4. first showing direction line
        
        if (right_direction):
            x_vals.append(int(x + w / 2))
            x_vals.append(int(x + w))
        else:
            x_vals.append(int(x + w / 2))
            x_vals.append(int(x))
            
        y_vals.append(int(y + h))
        y_vals.append(int(y + h / 2))
        
        # 5. second showing direction line
        
        if (right_direction):
            x_vals.append(int(x + w))
            x_vals.append(int(x + w / 2))
        else:
            x_vals.append(int(x))
            x_vals.append(int(x + w / 2))
        
        y_vals.append(int(y + h / 2))
        y_vals.append(int(y))
        
        # 6. second half bottom line
        
        y_vals.append(int(y))
        y_vals.append(int(y + h / 4))
        
        x_vals.append(int(x + w / 2))
        x_vals.append(int(x + w / 2))
        
        # 7. second half-length line
        
        if (right_direction):
            x_vals.append(int(x + w / 2))
            x_vals.append(x)
        else:
            x_vals.append(int(x + w / 2))
            x_vals.append(int(x + w))
        
        y_vals.append(int(y + h / 4))
        y_vals.append(int(y + h / 4))
        
        # generate the coordinates in a shape
        # so that PIL can understand it
        
        xy = []
        for i in range(7):
            xy.append((x_vals[2*i], y_vals[2*i]))
            xy.append((x_vals[2*i+1], y_vals[2*i+1]))
        
        if (fill):
            draw.polygon(xy, outline="red", fill="green")
        else:
            draw.polygon(xy, outline="red")
    
    def draw_img_from_file(self, main_image, img_filename, x, y, w, h):
        style_image = Image.open(img_filename)
        style_image = style_image.resize((w, h), Image.BICUBIC)

        style_image = style_image.convert("RGB")
        
        main_image.paste(style_image, (x, y))
    
    
    # score
    # ------------
    # case 0: no interesting events
    # case 1: new added card
    # case -1: deleted card, in next turn it dissepears
    # necessary_color is sometimes needed for desired
    # color, for visualization of card_on_top
    def draw_card(self, main_image, card, x, y, w, h, score=0,\
                 necessary_color=""):
        
        style_image_file = self.__style_images_path + "/cards/"
        # case: uncolored special card
        if (card.split(":")[1] == "nr"):
            value = card.split(":")[0]
            if (necessary_color != ""):
                color = necessary_color
            else:
                color = "none"
        # case: every colored card :D
        else:
            color = card.split(":")[0]
            value = card.split(":")[1]
            
        style_image_file += value + ".png"
        
        style_image = Image.open(style_image_file)
        style_image = style_image.resize((w, h), Image.BICUBIC)

        style_image = style_image.convert("RGB")
        
        # if colored card, then set the drawn color
        # to the appropriate value
        if (color != "none"):
            red_must = 0
            green_must = 0
            blue_must = 0
            if (color == "red"):
                red_must = 255
            elif (color == "green"):
                green_must = 255
            elif (color == "blue"):
                blue_must = 255
            elif (color == "yellow"):
                red_must = 255
                green_must = 255
            for x_style in range(style_image.size[0]):
                for y_style in range(style_image.size[1]):
                    # set appropriate color wherever in the
                    # source style image the color isn't white
                    red_is, green_is, blue_is = style_image.getpixel((x_style, y_style))
                    if ((red_is < 255) or (green_is < 255) or (blue_is < 255)):
                        
                        #intensity = int((red_is + green_is + blue_is) / 3)
                        
                        #if (red_must == 255):
                        #    red_must = intensity
                        #if (green_must == 255):
                        #    green_must = intensity
                        #if (blue_must == 255):
                        #    blue_must = intensity
                        
                        style_image.putpixel((x_style, y_style), (red_must, green_must, blue_must))
        
        draw_card_img = ImageDraw.Draw(style_image)
        delta_size = 5
        
        # we use a black border in every
        # case to see the cards divided
        draw_card_img.rectangle([
            (delta_size, delta_size),
            (style_image.size[0] - 2 * delta_size, style_image.size[1] - 2 * delta_size)
        ], outline="black")
        
        # score
        # ------------
        # case 0: no interesting events --> nothing
        
        # case 1: new added card
        if (score == 1):
            
            # draw many green rectangles with different sizes
            # to create a pattern looking like something new :D
            
            rectangles_distance_x = int(style_image.size[0] / 30)
            rectangles_distance_y = int(style_image.size[1] / 30)
            
            x_current = rectangles_distance_x
            y_current = rectangles_distance_y
            
            width_current = int(style_image.size[0] - 2 * x_current)
            height_current = int(style_image.size[1] - 2 * y_current)
            
            while ((width_current > 0) and (height_current > 0)):
                draw_card_img.rectangle([
                    (x_current, y_current),
                    (width_current, height_current),
                ], outline="green")
                
                x_current += rectangles_distance_x
                y_current += rectangles_distance_y

                width_current = int(style_image.size[0] - 2 * x_current)
                height_current = int(style_image.size[1] - 2 * y_current)
                
        # case -1: deleted card, in next turn it dissepears
        elif (score == -1):
            
            # draw 2 thick red lines to strike out the card
            
            # line 1
            # upper_left -> lower_right
            points = [
                (0, 0),
                (style_image.size[0], style_image.size[1])
            ]
            draw_card_img.line(points, "red", 5)
            
            # line 2
            # upper_right -> lower_left
            points = [
                (style_image.size[0], 0),
                (0, style_image.size[1])
            ]
            draw_card_img.line(points, "red", 5)
        
        
        # and paste the playing card image
        # into the main background image
        main_image.paste(style_image, (x, y))
    
    def get_current_player_and_cards_changes(self):
        current_player = ""
        for player in self.__players:
            if (player + "_after" \
                in self.__log_data[self.__curr_log_data_index].keys()):
                current_player = player
                break
        cards_before = self.__log_data[self.__curr_log_data_index]\
        [current_player + "_before"]
        cards_after = self.__log_data[self.__curr_log_data_index]\
        [current_player + "_after"]
        added_cards = []
        deleted_cards = []
        for card_after in cards_after:
            if (card_after not in cards_before):
                added_cards.append(card_after)
        for card_before in cards_before:
            if (card_before not in cards_after):
                deleted_cards.append(card_before)
        return current_player, added_cards, deleted_cards
    
    def get_current_player_on_turn(self):
        current_player = ""
        for player in self.__players:
            if (player + "_after" \
                in self.__log_data[self.__curr_log_data_index].keys()):
                current_player = player
                break
        return current_player
    
    def draw_player(self, main_image, draw, player_name, x, y, w, h,\
                   is_frame_before_turn):
        
        x_current = x
        y_current = y
        
        width_current = int(w / 4)
        height_current = h
        
        if (is_frame_before_turn):
            current_player = self.get_current_player_on_turn()
            added_cards = []
            deleted_cards = []
        else:
            current_player, added_cards, deleted_cards\
            = self.get_current_player_and_cards_changes()
        
        # player name
        # marked if player is on turn
        if (player_name == current_player):
            draw.rectangle([
                    (x_current, y_current),
                    (x_current + width_current, \
                     y_current + height_current),
                ], fill="yellow")
            self.draw_text(draw, player_name, \
                           x_current, y_current, \
                           width_current, height_current, "green")
        # name is written in default color red
        # if this player isn't on turn now
        else:
            self.draw_text(draw, player_name, \
                           x_current, y_current, \
                           width_current, height_current)
            added_cards = []
            deleted_cards = []
        
        if (player_name + "_before"\
           in self.__log_data\
            [self.__curr_log_data_index]):
        # now draw the cards in hand
        
            if ((not is_frame_before_turn)\
               and (player_name == current_player)):
                cards_in_hand = self.__log_data\
                [self.__curr_log_data_index]\
                [player_name + "_after"]
            else:
                cards_in_hand = self.__log_data\
                [self.__curr_log_data_index]\
                [player_name + "_before"]
        
        # if there are cards
        #if (len(cards_in_hand) > 0):
        
            # width per card
            width_current = int(3 * w / 4 / (len(cards_in_hand) + len(deleted_cards)))
            # current x to iterate over the cards to draw them
            x_current = int(w / 4)

            score = -1
            for deleted_card in deleted_cards:
                # draw the card

                self.draw_card(main_image, deleted_card, \
                               x_current, y_current, \
                               width_current, height_current, score=score)

                x_current += width_current

            for card_in_hand in cards_in_hand:
                score = 0
                if (card_in_hand in added_cards):
                    score = 1

                # draw the card

                self.draw_card(main_image, card_in_hand, \
                               x_current, y_current, \
                               width_current, height_current, score=score)

                x_current += width_current
        # if player has no cards then the player already won :D
        # or if they even don't exist as key in the log_data
        # dictionary anymore hahahahaha :D xD
        else:
            style_image_file = self.__style_images_path + "/party.jpg"
            style_image = Image.open(style_image_file)
            style_image = style_image.resize((w, h), Image.BICUBIC)
            # start with the x at image_width / 4 to see the
            # names
            main_image.paste(style_image, (int(w / 4), y))
    
    
    def draw(self, is_frame_before_turn):
        
        if (self.get_current_player_on_turn()
           in self.__players_being_human):
            self.__curr_background_file = \
            (self.__style_images_path + "background_human.jpg")
        else:
            self.__curr_background_file = \
            (self.__style_images_path + "background_robot.jpg")
        
        image = Image.open(self.__curr_background_file)
        draw = ImageDraw.Draw(image)
        img_width = image.size[0]
        img_height = image.size[1]
        
        x_current = 0
        y_current = 0
        
        width_current = 0
        height_current = 0
        
        # the first 1/4 in height
        # is for status info:
        height_current = int(img_height / 4)
        # ------
        # 1. turn number
        # 2. cards in stack
        # 3. current number of taking cards
        # 4. direction
        width_current = int(img_width / 4)
        
        # 1. turn number
        text = "Turn " + str(self.__curr_log_data_index)
        self.draw_text(draw, text, x_current, y_current, width_current, height_current)
        x_current += width_current
        
        # 2. cards in stack
        #text = str(self.__cards_in_stack) + " cards in stack"
        #self.draw_text(draw, text, x_current, y_current, width_current, height_current)
        #x_current += width_current
        
        curr_log_frame = self.__log_data[self.__curr_log_data_index]
        if (is_frame_before_turn):
            
            direction_changed = False
            
            is_forward_direction = curr_log_frame["state_before"]\
            ["IsForwardPlayingDirection"]
            
            curr_nr_taking_cards = curr_log_frame["state_before"]\
            ["NrOfCardsTaking"]
            
            card_on_top_changed = False
            
            card_on_top = curr_log_frame["card_on_top_before"]
            
            necessary_color = curr_log_frame["state_before"]\
            ["NecessaryColor"]
            
        else:
            direction_changed = \
            (curr_log_frame["state_before"]\
            ["IsForwardPlayingDirection"])\
            != (curr_log_frame["state_after"]\
            ["IsForwardPlayingDirection"])
             
            is_forward_direction = curr_log_frame["state_after"]\
            ["IsForwardPlayingDirection"]
             
            curr_nr_taking_cards = curr_log_frame["state_after"]\
            ["NrOfCardsTaking"]
            
            card_on_top_changed = \
            (curr_log_frame["card_on_top_before"])\
            != (curr_log_frame["card_on_top_after"])
            
            card_on_top = curr_log_frame["card_on_top_after"]
            
            necessary_color = curr_log_frame["state_after"]\
            ["NecessaryColor"]
        
        # 3. current number of taking cards
        text = "+ " + str(curr_nr_taking_cards)
        # visualize the text normal in red if there are taking cards
        if (curr_nr_taking_cards > 0):
            self.draw_text(draw, text, x_current, y_current, width_current, height_current)
        # visualize the text undangerous in green if there aren't taking cards
        else:
            self.draw_text(draw, text, x_current, y_current, width_current, height_current, "green")
        x_current += width_current
        
        # 4. direction
        self.draw_arrow_horizontal(draw, \
                                   x_current, \
                                   y_current, \
                                   width_current, \
                                   height_current, \
                                   is_forward_direction, \
                                   direction_changed)
        
        # draw the card on top
        
        x_current = int(3 * img_width / 4)
        y_current = int(img_height / 4)
        
        width_current = int(img_width / 4)
        height_current = int(3 * img_height / 4)
        
        # if card_on_top is
        # uncolored special
        # then draw it with
        # desired color
        if (card_on_top.split(":")[1]\
           == "nr"):
            self.draw_card(image, \
                   card_on_top, \
                   x_current, y_current, \
                   width_current, height_current,\
                    necessary_color=necessary_color)
        else:
            self.draw_card(image, \
                   card_on_top, \
                   x_current, y_current, \
                   width_current, height_current)
        
        if (card_on_top_changed):
            style_image_file = \
                self.__style_images_path \
                + "/mood_symbol_imgs/star_yeah.png"
            self.draw_img_from_file(image,\
                                   style_image_file,\
                                   x_current, 0,\
                                   width_current, y_current)
                
        # draw players and their cards
        # if we have players
        
        x_current = 0
        y_current = int(img_height / 4)
        
        width_current = int(3 * img_width / 4)
        
        if (len(self.__players) > 0):
        
            # height of one player depends on the number of players
            height_current = int(3 * img_height / 4 / len(self.__players))

            for player_name in self.__players:
                self.draw_player(image, draw, player_name, \
                                 x_current, y_current, \
                                 width_current, height_current,\
                                is_frame_before_turn)
                y_current += height_current
                
        # or visualize a funny way that we're lonely :( :D
        else:
            
            # or if we're lonely then put the lonely picture
            # on the whole height x'D
            height_current = int(3 * img_height / 4)
            
            style_image = Image.open(self.__style_images_path + "/lonely.jpg")
            style_image = style_image.resize((width_current, height_current), Image.BICUBIC)
            image.paste(style_image, (x_current, y_current))
        
        # save the current simulation frame under the appropriate image file
        image.save((self.__simulation_file_names_format % self.__frame_number), quality=80)
        # increment the current frame number
        self.__frame_number += 1
    
    def next_log_frame(self):
        self.__curr_log_data_index += 1
        if (self.__curr_log_data_index\
           == len(self.__log_data)):
            self.__curr_log_data_index -= 1
            return False
        else:
            return True
    
    def get_players(self):
        return self.__players
            
# zack
# yesssss
# visualization :D

# visualization :D B-)

# methods to use:
# noooooo
# much easier from log data tse tse
# --------------
# 1. onPlayerOnTurnChanged
# 2. onPlayerLoseCard
# 3. onPlayerGetCards
# 4. add_cards_player
# 5. add_players
# 6. onCardOnTop
# 7. onCardsTakenChanged
# 8. onDirectionChanged
# 9. onTurnNumberIncremented
# 10. ----> and call draw cyclic
# no, just read it from the fucking log_data tseeee
# tseeee tseeeee