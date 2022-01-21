import pygame


class Ship():

    def __init__(self, ai_settings, screen):
        """ initializing the ship and set its starting position """

        self.screen = screen
        self.ai_settings = ai_settings

        #load the ship images and get its rect
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Start every new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        #movment flags
        self.moving_right = False
        self.moving_left = False



    def update(self):
        #move the ship right or left depending on the flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #update the rect object from self.center attribute
        self.rect.centerx = self.center



    def blitme(self):
        #draw the ship at its current location

        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ center the ship on the screen"""
        self.center = self.screen_rect.centerx
