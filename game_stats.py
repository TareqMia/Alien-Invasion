class GameStats():
    """Track statistics for the game"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # start game in an inactive state
        self.game_active = False
        self.score = 0
        self.level = 1

        # high score should not be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize stats that can be changed throughout the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
