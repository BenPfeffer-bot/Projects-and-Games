class Settings:
    """Classe pour stocker les paramètres d'Alien Invasion. """

    def __init__(self):
        """Initialiser les paramètres du jeu."""
        # Paramètres de l'écran
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230) #couleur de l'arrière-plan
        #Paramètres de la fusée
        self.ship_speed = 1.5

        #Ajouter les paramètres des balles

        self.bullet_speed = 1.0
        self.bullet_width  = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        

    
