import sys

import pygame
from pygame.locals import *

class WatchWorm(object):

    CELL_SIZE = 15
    
    def __init__(self, grid_size):
        self.grid_size = grid_size

        pygame.display.init()
        self.s = pygame.display.set_mode((grid_size * self.CELL_SIZE,
                                          grid_size * self.CELL_SIZE))

        colors = [(255, 255, 255), (255, 0, 0)]
        i = 0
        for yi in xrange(grid_size):
            for xi in xrange(grid_size):
                self.set_cell_color((xi, yi), colors[i % len(colors)])
                i += 1

        pygame.display.flip()

    def set_cell_color(self, cell, color):
        border = 1
        x, y = cell
        r = pygame.Rect(x * self.CELL_SIZE + border,
                        y * self.CELL_SIZE + border,
                        self.CELL_SIZE - 2 * border,
                        self.CELL_SIZE - 2 * border)
        self.s.fill(color, r)

    def run(self):
        while True: 
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    return
                else: 
                    print event 
    
def main():
    ww = WatchWorm(10)
    ww.run()
    
if __name__ == '__main__':
    main()
