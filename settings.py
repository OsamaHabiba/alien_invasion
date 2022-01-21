""" this is a file containing all the settings requaired to run
 alien invasion"""

class Settings():
    """A class to store the settings"""
    def __init__(self):
         # initializing the game Settings


         #screen settings
         self.screen_width = 1200
         self.screen_height = 700
         self.bg_color = (0,0,0)
         self.screen_caption = "Alien Invasion"


         #Ship Settings
         self.ship_speed_factor = 1.5
         self.ship_limit = 2


         #bullet Settings
         self.bullet_speed_factor = 2
         self.bullet_width = 3
         self.bullet_height = 15
         self.bullet_color = 100, 100, 100
         self.bullets_allowed = 7


         #alien settings
         self.alien_speed_factor = 4
         self.fleet_drop_speed = 10
         self.fleet_direction = 1 #1 is right and -1 is leftinvasion
