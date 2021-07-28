import timeit

import pygame
from random import choices
from copy import deepcopy


BLACK = pygame.Color("black")
GREEN = pygame.Color("green")

PROBABILITY = 0.3

WIDTH, HEIGHT = 1360, 768


class GameLife:
    def __init__(self, size) -> None:
        self.width, self.height = size

        population = [1, 0]
        weights = [PROBABILITY, 1 - PROBABILITY]
        self.board = [[choices(population, weights)[0] for _ in range(self.width)] for _ in range(self.height)]
        self.empty = [[0] * self.width for _ in range(self.height)]

    def render(self, screen, cell_size):
        for y, line in enumerate(self.board):
            for x, cell in enumerate(line):
                if cell:
                    pygame.draw.rect(screen, GREEN, (x, y, cell_size, cell_size))

    def next(self):
        board = deepcopy(self.empty)
        for y, line in enumerate(self.board):
            for x, cell in enumerate(line):
                if cell:
                    if self.near(x, y) in (2, 3):
                        board[y][x] = 1
                else:
                    if self.near(x, y) == 3:
                        board[y][x] = 1
        self.board = board

    def near(self, x, y) -> int:
        count = 0

        around = (
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y),                     (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
            )
        for i, j in around:
            try:
                count += self.board[j][i]
            except IndexError:
                pass

        # SLOWER by unexpected reasons
        # for i, j in around:
        #     if 0 <= i <= self.width - 1 and 0 <= j <= self.height - 1:
        #         count += self.board[j][i]

        return count


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    game = GameLife((WIDTH, HEIGHT))

    cell_size = 1

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # time for next frame
        print(f"{round(clock.tick() / 1000, 2)}sec")

        # update objects
        game.next()

        # screen rendering
        screen.fill(BLACK)

        # objects rendering
        game.render(screen, cell_size)

        # update screen
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
