import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
        '''Respond to ship being hit'''
        if stats.ships_left > 0:
                stats.ships_left -= 1
                aliens.empty()
                bullets.empty
                create_fleet(ai_settings, screen, ship, aliens)
                ship.center_ship()
                sleep(0.5)
        else:
                stats.game_active = False


def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets):
        '''Check if any aliens hit the bottom of screen'''
        screen_rect = screen.get_rect()
        for alien in aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
                        break

def get_number_rows(ai_settings, ship_height, alien_height):
        '''Determine the number of rows of aliens that can fit oncreen.'''
        available_height_y = (ai_settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = int(available_height_y / (2 * alien_height))
        return number_rows

def get_number_aliens_x(ai_settings, alien_width):
        '''Determine the number of aliens that fit in a row'''
        available_space_x = ai_settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
        '''Create an alien and add it to the row'''
        alien = Alien(ai_settings, screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
        '''Create a full fleet of aliens.'''
        #Create an alien and find the number of aliens in a row.
        alien = Alien(ai_settings, screen)
        number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
        number_rows = get_number_rows(ai_settings, ship.rect.height,
                                      alien.rect.height)
        #Create the fleet of aliens.
        for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                        create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
        '''Respond appropriately if any aliens reach the edge.'''
        for alien in aliens.sprites():
                if alien.check_edges():
                        change_fleet_direction(ai_settings, aliens)
                        break

def change_fleet_direction(ai_settings, aliens):
        '''Drop the fleet and change its direction.'''
        for alien in aliens.sprites():
                alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleet_direction *= -1

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #Watch for Keyboard and Mouse Inputs
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        if event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
                fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
                sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
        '''Fire a bullet if limit not reached'''
        if len(bullets) < ai_settings.bullets_allowed:
                new_bullet = Bullet(ai_settings, screen, ship)
                bullets.add(new_bullet)
                
def check_keyup_events(event,ship):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        if event.key == pygame.K_LEFT:
            ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
        '''Update position of bullets and get rid of old ones.'''
        bullets.update()
        #Get rid of Bullets that have disappeared.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

        if len(aliens) == 0:
                #Destroy existing bullets and create new fleet.
                bullets.empty()
                create_fleet(ai_settings, screen, ship, aliens)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
        '''Respond to collisions'''
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

def update_screen(ai_settings, screen, ship, aliens, bullets):
    #Screen Color and Redraw Screen
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
            bullet.draw_bullet()

    #Make the screen visible.
    pygame.display.flip()


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
        '''Check to see if the fleet is at an edge,
           Update the positions of all the aliens in the fleet.'''
        check_fleet_edges(ai_settings, aliens)
        aliens.update()
        if pygame.sprite.spritecollideany(ship, aliens):
                ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets)
