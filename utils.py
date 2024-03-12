import pygame
from settings import themes, save_preferences

def redraw_window(surface, snake, snack, width, theme, rows):
    surface.fill(theme["background"])
    snake.draw(surface, rows, width)
    snack.draw(surface, rows, width)
    pygame.display.update()

def settings_menu(surface, themes):
    run = True
    sfont = pygame.font.SysFont("ariel", 54)
    ifont = pygame.font.SysFont("ariel", 24)
    font = pygame.font.SysFont("ariel", 34)
    while run:
        surface.fill(themes["light"]["background"])  # Default background for settings
        snake_main_text = sfont.render('Snake Game', True, (80, 10, 18))
        infoText = ifont.render('Choose Mode:', True, (80, 10, 180))
        light_mode_text = font.render('Light Mode', True, (180, 180, 180))
        dark_mode_text = font.render('Dark Mode', True, (70, 70, 70))

        start_rect = snake_main_text.get_rect(center=(250, 140))
        info_rect = infoText.get_rect(center=(250, 200))
        light_rect = light_mode_text.get_rect(center=(250, 250))
        dark_rect = dark_mode_text.get_rect(center=(250, 300))

        surface.blit(snake_main_text, start_rect)
        surface.blit(infoText, info_rect)
        surface.blit(light_mode_text, light_rect)
        surface.blit(dark_mode_text, dark_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if light_rect.collidepoint(event.pos):
                    return "light"
                elif dark_rect.collidepoint(event.pos):
                    return "dark"
        pygame.display.update()


def draw_game_over_screen(surface, score, width, height, theme):
    pygame.font.init()  # Initialize font module
    sfont = pygame.font.SysFont("ariel", 74)
    font = pygame.font.SysFont('Arial', 35)
    gameOverText = sfont.render('Game Over', True, theme['snake'])
    scoreText = font.render(f'Score: {score}', True, theme['snake'])
    playAgainText = font.render('Play Again', True, theme['snake'])
    exitText = font.render('Exit', True, theme['snake'])
    mainMenuText = font.render('Main Menu', True, theme['snake'])


    # Centering the text on the screen
    gameOverRect = gameOverText.get_rect(center=(width // 2, height // 2 - 90))
    scoreRect = scoreText.get_rect(center=(width // 2, height // 2))
    playAgainRect = playAgainText.get_rect(center=(width // 2, height // 2 + 55))
    mainMenuRect = mainMenuText.get_rect(center=(width // 2, height // 2 + 100))
    exitRect = exitText.get_rect(center=(width // 2, height // 2 + 160))

    # Game over loop
    while True:
        surface.fill(theme['background'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'quit'  # Exits the game completely
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if playAgainRect.collidepoint(mouse_pos):
                    return 'play_again'  # Indicates the player wants to play again
                if mainMenuRect.collidepoint(event.pos):
                    return 'main_menu'
                if exitRect.collidepoint(mouse_pos):
                    pygame.quit()
                    return 'quit'  # Exits the game completely

        surface.blit(gameOverText, gameOverRect)
        surface.blit(scoreText, scoreRect)
        surface.blit(playAgainText, playAgainRect)
        surface.blit(mainMenuText, mainMenuRect)
        surface.blit(exitText, exitRect)

        pygame.display.update()

    pygame.font.quit()
