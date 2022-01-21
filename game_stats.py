class GameStats():
    """track statistics for alien invasion"""

    def __init__(self, ai_settings):
        """initializing statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #start the game in an inactive state
        self.game_active = False

    def reset_stats(self):
        """initializing statistics that can change during the game"""
        self.ship_left = self.ai_settings.ship_limit
