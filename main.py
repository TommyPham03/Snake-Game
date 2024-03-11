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
    is_paused = False

    chosen_theme = settings_menu(win, themes)
    if chosen_theme != current_theme:
        current_theme = chosen_theme
        update_theme(chosen_theme)

    clock = pygame.time.Clock()
    running = True
    rows, cols = 20, 20

    s = Snake(themes[current_theme]["snake"], (10, 10), rows, cols)
    snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused
                else:
                    s.handle_keys(event)

        if not is_paused:
            update_result = s.update(snack)
            if update_result is True:
                # Game over due to collision with wall or self.
                running = draw_game_over_screen(win, len(s.body), width, height, themes[current_theme])
                if running:
                    # Reset game state for a new game
                    s.reset((10, 10))
                    snack = Cube(random_snack(s, rows), color=themes[current_theme]["food"])
            elif isinstance(update_result, tuple):
                # Snake has eaten a snack; generate a new snack.
                snack = Cube(update_result, color=themes[current_theme]["food"])
            # If not game over, continue and redraw window
            redraw_window(win, s, snack, width, themes[current_theme], rows)
        else:
            # Game is paused. Draw a paused screen overlay or message
            font = pygame.font.Font(None, 74)
            text = font.render("Paused", 1, (255, 0, 0))
            text_pos = text.get_rect(centerx=win.get_width() / 2, centery=win.get_height() / 2)
            win.blit(text, text_pos)
            pygame.display.update()

        pygame.time.delay(100)  # Control game speed
        clock.tick(10)  # FPS

    pygame.quit()

if __name__ == "__main__":
    main()
