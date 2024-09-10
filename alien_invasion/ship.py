import pygame
from settings import Settings

class Ship:
    """Classe pour générer la fusée."""

    def __init__(self, ai_game):
        """ Initialiser la fusée et définir sa position initiale. """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        # Charger l'image de fusée et obtenir son rect.
        self.image = pygame.image.load(r"C:\Users\UT3N95\Desktop\Ben_perso\alien_invasion\images\ship.bmp")
        self.rect = self.image.get_rect()

        #Placer chaque nouvelle fuséee au centre et en bas de l'écran
        self.rect.midbottom = self.screen_rect.midbottom

        #Stocker une valeur décimale correspondant
        # à la position horizontale de la fusée.
        self.x = float(self.rect.x)

        #Drapeau de déplacement
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Center la fusée à l'écran."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """
        Mettre à jour la position de la fusée en fct du drapeau de déplacement. 
        """
        #Mettre la valeur de x de la fusée, pas le rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
        #Droite
            self.x += self.settings.ship_speed
        #Gauche
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Mettre à jour l'objet rect en fct de self.x.
        self.rect.x = self.x


    def blitme(self):
        """Dessiner la fusée à son emplacement actuel."""
        self.screen.blit(self.image, self.rect)

