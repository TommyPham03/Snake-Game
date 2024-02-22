import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox

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
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
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

    # def move(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #         keys = pygame.key.get_pressed()
    #
    #         for key in keys:
    #             if keys[pygame.K_LEFT]:
    #                 self.dirnx = -1
    #                 self.dirny = 0
    #                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
    #             elif keys[pygame.K_RIGHT]:
    #                 self.dirnx = 1
    #                 self.dirny = 0
    #                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
    #             elif keys[pygame.K_UP]:
    #                 self.dirny = -1
    #                 self.dirnx = 0
    #                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
    #             elif keys[pygame.K_DOWN]:
    #                 self.dirny = 1
    #                 self.dirnx = 0
    #                 self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
    #
    #     for i, c in enumerate(self.body):
    #         p = c.pos[:]
    #         if p in self.turns:
    #             turn = self.turns[p]
    #             c.move(turn[0], turn[1])
    #             if i == len(self.body) - 1:
    #                 self.turns.pop(p)
    #         else:
    #             c.move(c.dirnx, c.dirny)

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


def redrawWindow():
    global win
    win.fill((0, 0, 0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass


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
def drawGameOverScreen(score):
    win.fill((0, 0, 0))  # Clear the screen
    font = pygame.font.SysFont("arial", 48)
    gameOverText = font.render("Game Over", True, (255, 255, 255))
    playAgainText = font.render("Play Again", True, (255, 255, 255))
    scoreText = font.render("Score: " + str(score), True, (255, 255, 255))

    gameOverRect = gameOverText.get_rect(center=(width/2, height/4))
    playAgainRect = playAgainText.get_rect(center=(width/2, height/2))
    scoreRect = scoreText.get_rect(center=(width/2, height/4*3))

    win.blit(gameOverText, gameOverRect)
    win.blit(playAgainText, playAgainRect)
    win.blit(scoreText, scoreRect)

    pygame.display.update()
    return playAgainRect  # Return the "Play Again" button rectangle for click detection

def main():
    global s, snack, win

    pause = False  # Initialize pause state
    show_text = True  # Initially, we want to show the text
    blink_counter = 0  # Counter to control blinking effect

    pygame.init()
    win = pygame.display.set_mode((width, height))
    s = snake((255, 0, 0), (10, 10))
    s.addCube()
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
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
            s.move()
            headPos = s.head.pos
            if headPos[0] >= rows or headPos[0] < 0 or headPos[1] >= rows or headPos[1] < 0 or s.body[0].pos in list(map(lambda z: z.pos, s.body[1:])):
                playAgainRect = drawGameOverScreen(len(s.body))
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if playAgainRect.collidepoint(mouse_pos):
                            s.reset((10, 10))
                            snack = cube(randomSnack(rows, s), color=(0, 255, 0))
                            break
            else:
                if s.body[0].pos == snack.pos:
                    s.addCube()
                    snack = cube(randomSnack(rows, s), color=(0, 255, 0))

            redrawWindow()
        else:
            font = pygame.font.SysFont("arial", 48)
            paused_text = font.render("Paused", True, (255, 255, 255))
            text_rect = paused_text.get_rect(center=(width/2, height/2))
            win.blit(paused_text, text_rect)
            pygame.display.update()

        #linking "Press P to pause" text
        if not pause:
            #blink_counter = (blink_counter + 1) % 30  # Adjust for blinking speed
            if blink_counter == 10000000:
                show_text = not show_text
            if show_text:
                font = pygame.font.SysFont("arial", 24)
                pause_text = font.render("Press P to pause", True, (255, 255, 255))
                win.blit(pause_text, (5, height - 30))
            pygame.display.update()

main()