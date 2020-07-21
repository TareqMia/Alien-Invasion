import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def check_keydown_evnets(event, ai_settings, screen, ship, bullets):
    """Respond to key presses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, score_board, play_button, ship, aliens, bullets):
    """Respond to key presses and mouse clicks"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, score_board, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_evnets(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Starts new game when player clicks 'PLAY' """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        # hide cursor
        pygame.mouse.set_visible(False)
        # reset game stats
        stats.reset_stats()
        stats.game_active = True

        # prep
        score_board.prep_level()
        score_board.prep_score()
        score_board.prep_high_score()
        score_board.prep_ships()

        # empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # crate new fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, score_board, ship, aliens, bullets, play_button):
    """Update images on the screen and flip the new screen"""
    # redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    # redraw all bullets behind ship and aliens
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    score_board.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # Make most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, score_board, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    # update bullet position
    bullets.update()

    # get rid of bullets that have gone off the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(
        ai_settings, screen, stats, score_board, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, score_board, ship, aliens, bullets):
    """Respond to bullet alien collision"""
    # check if any bullets have hit an alien
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if collisions:
        stats.score += ai_settings.alien_points
        score_board.prep_score()
        check_high_score(stats, score_board)

    if len(aliens) == 0:
        # destroy all existing bullets and create new fleet and speed up game
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        score_board.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire bullets if limit is not reached"""
    # create new bullet and at it bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine how many aliens fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Create an alien and place it in a row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create fleet of aliens"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    ship_height = ship.rect.height
    number_rows = get_number_rows(ai_settings, ship_height, alien.rect.height)

    # create fleet
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that will fit on the screen"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, screen, score_board, ship, aliens, bullets):
    """Check if the fleet has reached the edge and 
        then update the alien positions"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for collisions between ship and any alien ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats,
                 score_board, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats,
                        score_board, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Check if a fleet has reached the edges"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop entire fleet and change the dirction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, score_board, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # decrement ships left
        stats.ships_left -= 1

        score_board.prep_ships()
        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, score_board):
    """Check to see if there's new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()


def check_aliens_bottom(ai_settings, screen, stats, score_board, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if a ship got hit.
            ship_hit(ai_settings, screen, stats,
                     score_board, ship, aliens, bullets)
            break
