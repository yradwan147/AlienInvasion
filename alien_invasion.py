import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from game_stats import GameStats


def run_game():
    ''' Initialize game and create a screen object'''
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    #Make A ship
    ship = Ship(ai_settings, screen)

    #Make an Alien
    alien = Alien(ai_settings, screen)

    #Make a Group to store bullets in.
    bullets = Group()

    #Make a Group to store aliens in.
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    stats = GameStats(ai_settings)

    #Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        
run_game()
        
