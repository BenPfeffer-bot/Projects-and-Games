import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Classe pour réprésenter un alien."""

    def __init__(self,ai_game):
        """Initialiser l'alien et définir sa position initiale"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings  = ai_game.settings
        #Charger l'image d'alien et définir son attribut rect.
        self.image = pygame.image.load(r"C:\Users\UT3N95\Desktop\Ben_perso\alien_invasion\images\alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Stocker la position horizontale de l'alien.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Renvoyer True si l'ailien est au bord de l'écran."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """
        Déplacer l'alien vers la droite ou la gauche.
        """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x 


