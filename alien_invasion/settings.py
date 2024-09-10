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
        
        #Paramètres des aliens
        self.alien_speed = 1.0
        self.ship_limit = 3
        self.fleet_drop_speed = 10
        # fleet_direction = 1 correspond à la droite ; -1 à la gauche.
        self.fleet_direction = 1

        #Ajouter les paramètres des balles
        self.bullet_speed = 2
        self.bullet_width  = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3
        


    
