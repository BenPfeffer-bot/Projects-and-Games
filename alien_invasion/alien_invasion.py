# Important pckgs imports
import sys 
import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """
    Classe globale pour gérer les ressources et le comportement
    du jeu.
    """

    def __init__(self):
        """Initialiser le jeu et créer ses ressources."""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")

        #Définir la couleur d'arrière-plan.
        self.bg_color = (230, 230, 230)
        self.ship = Ship(self)

    def run_game(self):
        """Commencer la boucle principale du jeu."""
        while True:
            #Méthode _check_events()
            self._check_events()
            #Méthode _update_screen()
            self._update_screen()
            self.ship.update()

            # Surveiller les évènements du clavier et la souris. 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Redessiner l'écran à chaque exécution de la boucle.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()


            #Afficher l'écran le plus récemment déssinée.
            pygame.display.flip()

    def _check_events(self):
        """
        Répondre aux évènements de touche enfoncée
        et de la souris.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)    
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self,event):
        """Répondre aux évènements de touche enforcée."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self,event):
        """Répondre aux évènements de touche relachée."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _update_screen(self):
        """
        Mettre à jour les images à l'écran et passer 
        au nouvel écran.
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()




if __name__ == '__main__':
    #Créer une instance du jeu et lancer le jeu.
    ai = AlienInvasion()
    ai.run_game()