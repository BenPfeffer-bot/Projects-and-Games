class GameStats:
    """Suivre les statistiques d'Alien Invasion."""

    def __init__(self, ai_game):
        """Initialiser les stats."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """
        Initialiser les stats qui peuvent changer pdnt le jeu.
        """
        self.ships_left = self.settings.ship_limit
         