import sys

import pygame

from pygame.sprite import Group

from settings import Settings

from ship import Ship

import game_functions as gf

from game_stats import GameStats

from button import Button

def run_game():
    # initializing the game and create a screen object and settings object
    ai_settings = Settings()
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption(ai_settings.screen_caption)

    #make the play button
    play_button = Button(ai_settings, screen, "Play")

    #create an instance to store game statistics
    stats = GameStats(ai_settings)

    #make a Ship
    ship = Ship(ai_settings, screen)

    #make a group to store bullets
    bullets = Group()

    #make a group to store the aliens
    aliens = Group()

    #make a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # start the main loop for the game
    while True:
        # watch for keyboard and mouse events
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens,
                        bullets)
        if stats.game_active:
            #move the ship according to the keypress
            ship.update()
            #update the position of the bullets and get rid of old bullets
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            #moving the alien fleet
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

            # redraw the screen
        gf.update_screen(ai_settings, stats, screen, ship, aliens, bullets,
                        play_button)

run_game()
