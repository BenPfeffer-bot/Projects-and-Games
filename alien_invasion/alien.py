import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Classe pour réprésenter un alien."""

    def __init__(self,ai_game):
        """Initialiser l'alien et définir sa position initiale"""
        super().__init__()
        self.screen = ai_game.screen

        #Charger l'image d'alien et définir son attribut rect.
        self.image = pygame.image.load(r"C:\Users\UT3N95\Desktop\Ben_perso\alien_invasion\images\alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Stocker la position horizontale de l'alien.
        self.x = float(self.rect.x)
