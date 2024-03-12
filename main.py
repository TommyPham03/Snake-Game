import pygame
from settings import load_preferences, save_preferences, themes, update_theme
from game_objects import Snake, Cube, random_snack
from utils import redraw_window, settings_menu, draw_game_over_screen

def main_menu(win):
    preferences = load_preferences()
    current_theme = preferences.get("theme", "dark")
    chosen_theme = settings_menu(win, themes)
    if chosen_theme and chosen_theme != current_theme:
        current_theme = chosen_theme
        update_theme(chosen_theme)
    return current_theme

def game_loop(win, current_theme, width, height, rows, cols):
    clock = pygame.time.Clock()
    is_paused = False
    running = True

    s = Snake(themes[current_theme]["snake"], (10, 10), rows, cols)
    snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                else:
                    s.handle_keys(event)

        if not is_paused:
            update_result = s.update(snack)
            if update_result is True:
                game_over_result = draw_game_over_screen(win, len(s.body), width, height, themes[current_theme])
                if game_over_result == 'play_again':
                    s.reset((10, 10))
                    snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])
                elif game_over_result == 'main_menu':
                    return 'main_menu'
            elif isinstance(update_result, tuple):
                snack = Cube(update_result, color=themes[current_theme]["food"])
            redraw_window(win, s, snack, width, themes[current_theme], rows)
        else:
            font = pygame.font.Font(None, 74)
            text = font.render("Paused", 1, (255, 0, 0))
            text_pos = text.get_rect(centerx=win.get_width() / 2, centery=win.get_height() / 2)
            win.blit(text, text_pos)
            pygame.display.update()

        pygame.time.delay(100)
        clock.tick(10)



def main():
    pygame.init()
    width, height = 500, 500
    win = pygame.display.set_mode((width, height))
    preferences = load_preferences()
    current_theme = preferences.get("theme", "dark")

    chosen_theme = settings_menu(win, themes)
    if chosen_theme and chosen_theme != current_theme:
        current_theme = chosen_theme
        update_theme(chosen_theme)

    rows, cols = 20, 20  # Define rows and cols as needed

    game_result = game_loop(win, current_theme, width, height, rows, cols)
    if game_result == 'main_menu':
        # Handle return to main menu logic here if needed
        main()  # For example, you might call main() again to restart


if __name__ == "__main__":
    main()


