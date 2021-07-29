import timeit

import pygame
from random import choices
import numpy

from matrix import copy


BLACK = pygame.Color("black")
GREEN = pygame.Color("green")

PROBABILITY = 0.1

k = 1
WINDOW_SIZE = 1200, 600
SURFACE_SIZE = WINDOW_SIZE[0] // k, WINDOW_SIZE[1] // k
CELL_SIZE = k


class GameLife:
    def __init__(self, size) -> None:
        self.width, self.height = size

        population = [1, 0]
        weights = [PROBABILITY, 1 - PROBABILITY]
        self.board = [[choices(population, weights)[0] for _ in range(self.width)] for _ in range(self.height)]

    def render(self, screen, cell_size):
        for y, line in enumerate(self.board):
            for x, cell in enumerate(line):
                if cell:
                    pygame.draw.rect(screen, GREEN, (x * cell_size, y * cell_size, cell_size, cell_size))

    def next(self):  # 0.7
        board = copy(self.board)

        for y in range(self.height):
            for x in range(self.width):
                if board[y][x]:
                    if not 2 <= self.near(x, y) <= 3:
                        board[y][x] = 0
                else:
                    if self.near(x, y) == 3:
                        board[y][x] = 1

        self.board = board

    def next_v2(self):  # 0.73
        before = copy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                if before[y][x]:
                    if not 2 <= self.near(x, y) <= 3:
                        self.board[y][x] = 0
                elif self.near(x, y) == 3:
                    self.board[y][x] = 1

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

        return count

    def near_v2(self, x, y) -> int:
        matrix = numpy.matrix(self.board)
        index = [y, x]
        num_neighbor = 1

        left = max(0, index[0] - num_neighbor)
        right = max(0, index[0] + num_neighbor + 1)

        bottom = max(0, index[1] - num_neighbor)
        top = max(0, index[1] + num_neighbor + 1)
        sample = matrix[left:right, bottom:top]
        return sample.sum() - self.board[y][x]


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    game = GameLife(SURFACE_SIZE)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # time for next frame
        print(f"{round(clock.tick() / 1000, 2)}sec")
        print(f"{round(clock.get_fps())}FPS")
        # update objects
        start = timeit.default_timer()
        game.next_v2()
        print(f"next {timeit.default_timer() - start}")

        # screen rendering
        screen.fill(BLACK)

        # objects rendering
        game.render(screen, CELL_SIZE)

        # update screen
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
