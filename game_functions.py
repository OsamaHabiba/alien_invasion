import sys

import pygame

from bullet import Bullet

from alien import Alien

from time import sleep

""" the functions for reacting to keypresses and mouse movment """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def fire_bullet(ai_settings, screen, ship, bullets):
    """fires a bullete if limit not riched yet"""
    #craete a new bullet and add it to the bullets group
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)


def check_keydown(event, ai_settings, screen, ship, bullets):
    """respond to key presses"""
    if event.key == pygame.K_RIGHT:
        #move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #move the ship to the left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and len(bullets) < ai_settings.bullets_allowed:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()



def check_keyup(event, ship):
    """respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings,screen, stats, play_button, ship, aliens,
                        bullets, mouse_x, mouse_y):
    """start a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        #hide mouse crusor
        pygame.mouse.set_visible(False)
        #reset the game statistics
        stats.reset_stats()
        #start a new game when clicked
        stats.game_active = True

        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """ respond to keypress and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen, stats, play_button, ship, aliens,
                                    bullets, mouse_x, mouse_y)


""" functions for manging aliens """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_number_aliens_x(ai_settings, alien_width):
    """ determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = round(available_space_x / (alien_width + 10))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """determine the number of rows of aliens that fit into the screen"""
    available_space_y = ai_settings.screen_height - (5*alien_height) - ship_height
    number_rows = round(available_space_y / (alien_height + 15))
    return number_rows


def craete_alien(ai_settings, screen, aliens, alien_number, row_number):
    """craete an alien and place it in a row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (alien_number * alien_width + (10*alien_number))
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + (alien.rect.height * row_number + 10 *
    row_number)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """create a full fleet of aliens"""
    #create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
    alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #create an alien and place it in the raw
            craete_alien(ai_settings, screen, aliens, alien_number,
            row_number)


def change_fleet_direction(ai_settings, aliens):
    """drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """respond to ship being hit by an alien"""
    if stats.ship_left > 0:
        #decrement the number of lives left
        stats.ship_left -=1
        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #pause
        sleep(1.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)



def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """ check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat this as if the ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """update the position of aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    """ look for alien and ship collisions"""
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    """look for aliens hitting the bottom of the screen"""
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)




""" functions for updating and redrawing the screen and the objects of the game """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def update_screen(ai_settings, stats, screen, ship, aliens, bullets,
        play_button):


    #redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    #make the most recent screen visible
    pygame.display.flip()

def check_collision(ai_settings, screen, ship, aliens, bullets):

    #check for bullets that hit aliens and get rid of the bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    #repopulating the fleet if all aliens destroyed
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """update the position of bullets and get rid of old bullets"""
    #update bullet's position
    bullets.update()

    #get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_collision(ai_settings, screen, ship, aliens, bullets)
