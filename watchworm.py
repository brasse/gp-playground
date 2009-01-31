from itertools import *

import pyglet
from pyglet.gl import *

class WormWindow(pyglet.window.Window):
    CELL_SIZE = 15
    STEP_TIME = 1
    BORDER = 1
    BODY_COLOR = (0.0, 0.0, 1.0)
    HEAD_COLOR = (1.0, 1.0, 1.0)
    
    def __init__(self, grid_size, path):
        self.path = path
        self.window_size = self.CELL_SIZE * grid_size
        self.visible_steps = 0
        pyglet.window.Window.__init__(self,
                                      width=self.window_size,
                                      height=self.window_size,
                                      caption='watchworm')
        pyglet.clock.schedule_interval(self.step, self.STEP_TIME)

    def step(self, dt):
        self.visible_steps += 1
        if self.visible_steps == len(self.path):
            pyglet.clock.unschedule(self.step)
            
    def draw_cell(self, position, color):
        x, y = position
        left = x * self.CELL_SIZE + self.BORDER
        lower = y * self.CELL_SIZE + self.BORDER
        side = self.CELL_SIZE - 1 - 2 * self.BORDER
        glColor3f(*color)
        glRecti(left, lower, left + side, lower + side)
        
    def on_draw(self):
        glClearColor(0.3, 0.3, 0.4, 1.0)
        self.clear()
        # Create the visible part of the worm, the head is first in the list.
        worm = izip(reversed(self.path[:self.visible_steps]),
                    chain([self.HEAD_COLOR], repeat(self.BODY_COLOR)))
        for cell_position, color in worm:
            self.draw_cell(cell_position, color)
        
            
def process(grid_size, path=None, program=None):
    window = WormWindow(grid_size, [(0, 0), (0, 1), (1, 1)])
    pyglet.app.run()

def main():
    process(10)

if __name__ == '__main__':
    main()
