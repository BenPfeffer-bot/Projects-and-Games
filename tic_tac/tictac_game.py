"""
We will create a small game very basic tictac game to train my python fluency
"""
import pygame

class TicTacGames:
    """
    Define the game and attribute the corresponding config
    """

    def __init__(self,round):
        """
        Initiate the characteristic
        of the game.
        """
        self.round = round
        self.color_scheme = {
            'background': (0,0,0),
            'player_1' : "#",
            'player_2' : "#"
        }

    def create_gridlines(self):
        """    
        Defines the gridline and set-up 
        the lines for the tic tac games.
        """
        # Open a window on the screen
        screen_width=700
        screen_height=400
        screen=pygame.display.set_mode([screen_width, screen_height])
