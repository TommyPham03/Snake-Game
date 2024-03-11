import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox


import json

# Define color themes
themes = {
    "light": {"background": (240, 240, 240), "snake": (0, 0, 0), "food": (0, 255, 0)},
    "dark": {"background": (20, 20, 20), "snake": (255, 255, 255), "food": (255, 165, 0)},
}
current_theme = "dark"  # Default theme

def load_preferences():
    try:
        with open("user_preferences.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"theme": "dark"}

preferences = load_preferences()
current_theme = preferences.get("theme", "dark")


width = 500
height = 500

cols = 25
rows = 20


class cube():
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny  # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        global current_theme  # Make sure this is declared at the top
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        color = self.color if self.color else themes[current_theme]["snake"]
        pygame.draw.rect(surface, color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake():
    body = []
    turns = {}

    def __init__(self, color, pos):
        # pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        # Check if there's a direction change queued
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow(win):
    win.fill(themes[current_theme]["background"])
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


#method added for game over screen
def drawGameOverScreen(win, score):
    win.fill(themes[current_theme]["background"])
    gameOverFont = pygame.font.SysFont("arial", 80)
    font = pygame.font.SysFont("arial", 48)
    gameOverText = gameOverFont.render("Game Over", True, (25, 65, 155))
    changeThemeText = font.render("Change Theme", True, (25, 65, 155))
    playAgainText = font.render("Play Again", True, (25, 65, 155))
    scoreText = font.render("Score: " + str(score), True, (25, 65, 155))

    gameOverRect = gameOverText.get_rect(center=(width / 2, height / 4))
    playAgainRect = playAgainText.get_rect(center=(width / 2, height / 2))
    changeThemeRect = changeThemeText.get_rect(center=(width / 2, height * 3 / 4))
    scoreRect = scoreText.get_rect(center=(width / 2, height / 8))

    win.blit(gameOverText, gameOverRect)
    win.blit(playAgainText, playAgainRect)
    win.blit(changeThemeText, changeThemeRect)
    win.blit(scoreText, scoreRect)

    pygame.display.update()
    return playAgainRect, changeThemeRect  # Return rectangles for interaction detection


def settings_menu(win):
    global current_theme
    menu_running = True
    menu_font = pygame.font.SysFont("arial", 32)
    light_mode_text = menu_font.render('Light Mode', True, (255, 255, 255))
    dark_mode_text = menu_font.render('Dark Mode', True, (75, 75, 75))

    light_mode_rect = light_mode_text.get_rect(center=(150, 150))
    dark_mode_rect = dark_mode_text.get_rect(center=(350, 150))

    while menu_running:
        win.fill((0, 0, 0))  # Default background
        win.blit(light_mode_text, light_mode_rect)
        win.blit(dark_mode_text, dark_mode_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if light_mode_rect.collidepoint(pygame.mouse.get_pos()):
                    current_theme = "light"
                    preferences['theme'] = "light"  # Update preferences
                    menu_running = False
                elif dark_mode_rect.collidepoint(pygame.mouse.get_pos()):
                    current_theme = "dark"
                    preferences['theme'] = "dark"  # Update preferences
                    menu_running = False

        pygame.display.update()

    # Save preferences when menu closes
    with open("user_preferences.json", "w") as f:
        json.dump(preferences, f)


def main():
    global s, snack

    # Initialize pygame and set up the window
    pygame.init()
    win = pygame.display.set_mode((width, height))

    # Load the settings menu at the start
    settings_menu(win)

    # Game Initialization
    running = True
    while running:
        # Reinitialize game entities and state
        pause = False
        s = snake(themes[current_theme]["snake"], (10, 10))
        s.addCube()
        snack = cube(randomSnack(rows, s), color=themes[current_theme]["food"])
        clock = pygame.time.Clock()

        # Main game loop
        game_over = False
        while not game_over:
            pygame.time.delay(50)
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    # Handle key presses
                    if event.key == pygame.K_LEFT:
                        s.dirnx = -1
                        s.dirny = 0
                        s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
                    elif event.key == pygame.K_RIGHT:
                        s.dirnx = 1
                        s.dirny = 0
                        s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
                    elif event.key == pygame.K_UP:
                        s.dirny = -1
                        s.dirnx = 0
                        s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
                    elif event.key == pygame.K_DOWN:
                        s.dirny = 1
                        s.dirnx = 0
                        s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
                    elif event.key == pygame.K_p:
                        pause = not pause

            if not pause:
                # Move the snake
                s.move()

                # Check for collisions
                if s.head.pos == snack.pos:
                    s.addCube()
                    snack = cube(randomSnack(rows, s), color=themes[current_theme]["food"])

                # Check game over condition
                if s.head.pos[0] >= cols or s.head.pos[0] < 0 or s.head.pos[1] >= rows or s.head.pos[1] < 0:
                    game_over = True

                redrawWindow(win)

        # Game Over Screen
        playAgainRect, changeThemeRect = drawGameOverScreen(win, len(s.body))

        waiting_for_input = True
        while waiting_for_input:
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                running = False
                break
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if playAgainRect.collidepoint(mouse_pos):
                    waiting_for_input = False  # Reset the game
                elif changeThemeRect.collidepoint(mouse_pos):
                    settings_menu(win)  # Change theme
                    waiting_for_input = False


main()
