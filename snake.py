import pygame
from settings import load_preferences, save_preferences, themes, update_theme, get_high_score, save_high_score
from game_objects import Snake, Cube, random_snack
from utils import redraw_window, settings_menu, draw_game_over_screen, difficulty_menu, load_or_create_profile, save_user_data
from utils import load_or_create_profile, get_user_input, save_user_data

def main_menu(win):
    preferences = load_preferences()
    current_theme = preferences.get("theme", "dark")
    chosen_theme = settings_menu(win, themes)
    if chosen_theme and chosen_theme != current_theme:
        current_theme = chosen_theme
        update_theme(chosen_theme)
    return current_theme

def game_loop(win, current_theme, width, height, rows, cols, difficulty, user_data):
    clock = pygame.time.Clock()
    speed = {'easy': 5, 'medium': 10, 'hard': 15}[difficulty]
    is_paused = False
    running = True
    current_score = 0  # Initialize score
    high_score = get_high_score(user_data)

    s = Snake(themes[current_theme]["snake"], (10, 10), rows, cols)
    snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])

    while running:
        pygame.time.delay(100)
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                else:
                    s.handle_keys(event)

        if not is_paused:
            update_result = s.update(snack)
            if isinstance(update_result, tuple):
                snack = Cube(update_result, color=themes[current_theme]["food"])
                current_score += 1  # Increment score
                if current_score > high_score:
                    high_score = current_score
                    user_data['high_score'] = high_score  # Update high score in user data

            if update_result is True:
                game_over_result = draw_game_over_screen(win, current_score, width, height, themes[current_theme])
                if game_over_result == 'play_again':
                    s.reset((10, 10))
                    current_score = 0  # Reset score
                    snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])
                elif game_over_result == 'main_menu':
                    return 'main_menu'
                elif game_over_result == 'quit':
                    return 'quit'

            redraw_window(win, s, snack, width, themes[current_theme], rows, current_score, high_score)
        else:
            font = pygame.font.Font(None, 74)
            text = font.render("Paused", 1, (255, 0, 0))
            text_pos = text.get_rect(centerx=win.get_width() / 2, centery=win.get_height() / 2)
            win.blit(text, text_pos)
            pygame.display.update()

    return {'score': current_score, 'high_score': high_score}



def main():

    # Initialize Pygame and the display
    pygame.init()
    surface = pygame.display.set_mode((500, 500))
    username = get_user_input(surface, "Enter your username:")
    user_data = load_or_create_profile(username)

    theme = user_data['preferences']['theme']
    difficulty = user_data['preferences']['difficulty']

    width, height = 500, 500
    win = pygame.display.set_mode((width, height))
    rows, cols = 20, 20

    while True:
        current_theme = main_menu(win)
        if not current_theme:
            break
        difficulty = difficulty_menu(win, themes[current_theme])
        if not difficulty:
            break
        game_result = game_loop(win, current_theme, width, height, rows, cols, difficulty, user_data)
        if game_result == 'quit':
            break
    save_user_data(username, user_data)


if __name__ == "__main__":
    main()