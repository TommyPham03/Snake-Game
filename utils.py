import pygame
from settings import themes
import json
import os
from settings import get_text_size, load_preferences
import pygame

def draw_text_input_box(surface, font, input_rect, color_active, color_inactive, active, text=''):
    """ Draw a text input box and handle text input. """
    color = color_active if active else color_inactive
    pygame.draw.rect(surface, color, input_rect, 2)
    text_surface = font.render(text, True, (255, 255, 255))
    surface.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    pygame.display.update()
    return text


def get_user_input(surface, question):
    """ Function to get user input using a simple text box in Pygame. """
    pygame.font.init()
    preferences = load_preferences()  # Load preferences
    text_size = get_text_size(preferences)  # Get dynamic text size

    base_font = pygame.font.Font(None, text_size)  # Use dynamic text size
    title_font = pygame.font.Font(None, text_size + 8)  # Slightly larger for title

    user_text = ''
    input_rect = pygame.Rect(surface.get_width() // 2 - 70, surface.get_height() // 2, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')
    active = False
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        surface.fill((30, 30, 30))
        title_text = title_font.render(question, True, (255, 255, 255))
        surface.blit(title_text, (surface.get_width() // 2 - title_text.get_width() // 2, surface.get_height() // 2 - 50))
        draw_text_input_box(surface, base_font, input_rect, color_active, color_inactive, active, user_text)

    return user_text


def load_user_data(username):
    """ Load user data from a JSON file based on the username. """
    try:
        with open(f'user_data/{username}.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def save_user_data(username, data):
    """ Save user data to a JSON file. """
    os.makedirs('user_data', exist_ok=True)
    # Update the high score in the user data
    data['high_score'] = data.get('high_score', 0)
    with open(f'user_data/{username}.json', 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved for {username}")



def load_or_create_profile(username):
    """ Load an existing profile or create a new one if it doesn't exist. """
    user_data = load_user_data(username)
    if user_data is None:
        print("No existing user data found. Creating new profile...")
        user_data = {
            'username': username,
            'high_score': 0,
            'preferences': {
                'difficulty': 'easy',  # Default settings
                'theme': 'light'
            }
        }
        save_user_data(username, user_data)
    else:
        print(f"Loaded existing data for {username}")
    return user_data



def redraw_window(surface, snake, snack, width, theme, rows, current_score, high_score):
    surface.fill(theme["background"])
    snake.draw(surface, rows, width)
    snack.draw(surface, rows, width)

    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f'Score: {current_score}', True, (255, 0, 0))
    high_score_text = font.render(f'High Score: {high_score}', True, (255, 165, 0))

    surface.blit(score_text, (width - 150, 10))  # Top right corner
    surface.blit(high_score_text, (10, 10))  # Top left corner

    pygame.display.update()


def settings_menu(surface, themes):
    preferences = load_preferences()
    text_size = get_text_size(preferences)

    run = True
    sfont = pygame.font.Font(None, text_size + 20)
    ifont = pygame.font.Font(None, text_size + 8)
    font = pygame.font.Font(None, text_size)
    surface.fill(themes["light"]["background"])  # Assume light theme for settings background

    snake_main_text = sfont.render('Snake Game', True, (80, 10, 18))
    infoText = ifont.render('Choose Mode:', True, (80, 10, 180))
    light_mode_text = font.render('Light Mode', True, (180, 180, 180))
    dark_mode_text = font.render('Dark Mode', True, (70, 70, 70))

    start_rect = snake_main_text.get_rect(center=(250, 100))
    info_rect = infoText.get_rect(center=(250, 160))
    light_rect = light_mode_text.get_rect(center=(250, 220))
    dark_rect = dark_mode_text.get_rect(center=(250, 280))

    surface.blit(snake_main_text, start_rect)
    surface.blit(infoText, info_rect)
    surface.blit(light_mode_text, light_rect)
    surface.blit(dark_mode_text, dark_rect)
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if light_rect.collidepoint(event.pos):
                    return "light"
                elif dark_rect.collidepoint(event.pos):
                    return "dark"

def draw_game_over_screen(surface, score, width, height, theme):
    pygame.font.init()
    preferences = load_preferences()
    text_size = get_text_size(preferences)

    sfont = pygame.font.Font(None, text_size + 20)
    font = pygame.font.Font(None, text_size)
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

def difficulty_menu(surface, theme):
    preferences = load_preferences()
    text_size = get_text_size(preferences)

    run = True
    font = pygame.font.Font(None, text_size)
    surface.fill(theme['background'])  # Fill the background once per setting

    title_text = font.render('Select Difficulty:', True, theme['snake'])
    easy_text = font.render('Easy', True, theme['snake'])
    medium_text = font.render('Medium', True, theme['snake'])
    hard_text = font.render('Hard', True, theme['snake'])

    title_rect = title_text.get_rect(center=(250, 150))
    easy_rect = easy_text.get_rect(center=(250, 200))
    medium_rect = medium_text.get_rect(center=(250, 250))
    hard_rect = hard_text.get_rect(center=(250, 300))

    surface.blit(title_text, title_rect)
    surface.blit(easy_text, easy_rect)
    surface.blit(medium_text, medium_rect)
    surface.blit(hard_text, hard_rect)
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return "easy"
                elif medium_rect.collidepoint(event.pos):
                    return "medium"
                elif hard_rect.collidepoint(event.pos):
                    return "hard"
