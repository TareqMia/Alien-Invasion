import pygame
from settings import Settings
import game_functions as gf
from ship import Ship
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    screen.fill(ai_settings.bg_color)

    # create play button
    play_button = Button(ai_settings, screen, "PLAY")

    stats = GameStats(ai_settings)
    score_board = ScoreBoard(ai_settings, screen, stats)

    # make a ship, a group of aliens and a group of bullets
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()

    # create fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # main game loop
    while True:
        gf.check_events(ai_settings, screen, stats, score_board,
                        play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings, screen, stats,
                              score_board, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen,
                             score_board, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, score_board,
                         ship, aliens, bullets, play_button)


run_game()
