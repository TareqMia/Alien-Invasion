class Settings():
    """A class to all the settings for Alien Invasion"""

    def __init__(self):
        """Initialize static settings"""
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        
        
        # bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        self.fleet_drop_speed = 10
        
        # how quickly the game speeds up
        self.speed_up_scale = 1.1
        # points
        self.alien_points = 50
        
        # score multiplier
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        # ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # alein settings
        self.alien_speed_factor = 1
        # fleet_direction of 1 represents right. -1 represents left
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale
        
        # increase score scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
        
