import pygame
import random

class Cube:
    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.color = color

    def draw(self, surface, rows, width):
        dis = width // rows
        i, j = self.pos
        pygame.draw.rect(surface, self.color, (i*dis + 1, j*dis + 1, dis - 2, dis - 2))

class Snake:
    body = []
    turns = {}

    def __init__(self, color, pos, rows, cols):
        self.color = color
        self.head = Cube(pos, color=color)
        self.body = [self.head]
        self.dirnx = 0
        self.dirny = 1
        self.rows = rows
        self.cols = cols

    def handle_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.dirnx != 1:
                self.dirnx = -1
                self.dirny = 0
            elif event.key == pygame.K_RIGHT and self.dirnx != -1:
                self.dirnx = 1
                self.dirny = 0
            elif event.key == pygame.K_UP and self.dirny != 1:
                self.dirnx = 0
                self.dirny = -1
            elif event.key == pygame.K_DOWN and self.dirny != -1:
                self.dirnx = 0
                self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dirnx = -1
                    self.dirny = 0
                elif event.key == pygame.K_RIGHT:
                    self.dirnx = 1
                    self.dirny = 0
                elif event.key == pygame.K_UP:
                    self.dirnx = 0
                    self.dirny = -1
                elif event.key == pygame.K_DOWN:
                    self.dirnx = 0
                    self.dirny = 1

        for i in range(len(self.body)-1, 0, -1):
            self.body[i].pos = self.body[i-1].pos

        self.head.pos = (self.head.pos[0] + self.dirnx, self.head.pos[1] + self.dirny)



    def reset(self, pos):
        self.head = Cube(pos, self.color)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = self.dirnx, self.dirny  # Direction of the snake, not the tail cube

        # Determine the new cube's position based on the snake's direction
        if dx == 1 and dy == 0:  # Moving right
            new_pos = (tail.pos[0] - 1, tail.pos[1])
        elif dx == -1 and dy == 0:  # Moving left
            new_pos = (tail.pos[0] + 1, tail.pos[1])
        elif dx == 0 and dy == 1:  # Moving down
            new_pos = (tail.pos[0], tail.pos[1] - 1)
        elif dx == 0 and dy == -1:  # Moving up
            new_pos = (tail.pos[0], tail.pos[1] + 1)

        # Append a new cube at the calculated position
        self.body.append(Cube(new_pos, self.color))

    def draw(self, surface, rows, width):
        for cube in self.body:
            cube.draw(surface, rows, width)


    def update(self, snack):
        self.move()

        # Check for collision with the snack
        if self.head.pos == snack.pos:
            self.add_cube()
            # Generate and return a new snack position
            return random_snack(self, self.rows)

        # Check for collision with the walls
        if self.head.pos[0] >= self.cols or self.head.pos[0] < 0 or self.head.pos[1] >= self.rows or self.head.pos[
            1] < 0:
            return True  # Game over due to hitting a wall

        # Check for collision with itself
        for segment in self.body[1:]:
            if self.head.pos == segment.pos:
                return True  # Game over due to running into itself

        return False  # Game continues

def random_snack(snake, rows):
        positions = [segment.pos for segment in snake.body]
        while True:
            x, y = random.randrange(rows), random.randrange(rows)
            if (x, y) not in positions:
                return (x, y)

