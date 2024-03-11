import pygame
from settings import load_preferences, save_preferences, themes, update_theme
from game_objects import Snake, Cube, random_snack
from utils import redraw_window, settings_menu, draw_game_over_screen


def main():
    pygame.init()
    width, height = 500, 500
    win = pygame.display.set_mode((width, height))
    preferences = load_preferences()
    current_theme = preferences.get("theme", "dark")

    chosen_theme = settings_menu(win, themes)
    if chosen_theme != current_theme:
        current_theme = chosen_theme
        update_theme(chosen_theme)

    clock = pygame.time.Clock()
    running = True
    rows, cols = 20, 25

    s = Snake(themes[current_theme]["snake"], (10, 10), rows, cols)
    snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])

    while running:
        pygame.time.delay(200)
        clock.tick(6)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            s.handle_keys(event)  # Pass the event to handle_keys

        result = s.update(snack)
        if result is True:
            # Game over due to collision.
            running = draw_game_over_screen(win, len(s.body), width, height, themes[current_theme])
            if running:
                # Reset game state for a new game
                s.reset((10, 10))
                snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])
            else:
                break  # Exit the game loop
        elif isinstance(result, tuple):
            # Snake has eaten a snack; generate a new snack.
            snack = Cube(result, color=themes[current_theme]["food"])

        game_over = s.update(snack)
        if game_over:
            running = draw_game_over_screen(win, len(s.body), width, height, themes[current_theme])
            s.reset((10, 10))
            snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])

        redraw_window(win, s, snack, width, themes[current_theme], rows)

    pygame.quit()


if __name__ == "__main__":
    main()
