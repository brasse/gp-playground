from itertools import *

import pyglet
from pyglet.gl import *

class WormWindow(pyglet.window.Window):
    CELL_SIZE = 15
    STEP_TIME = 0.02
    BORDER = 1
    BODY_COLOR = (0.0, 0.0, 1.0)
    HEAD_COLOR = (1.0, 1.0, 1.0)
    STOP_COLOR = (1.0, 0.0, 0.0)
    
    def __init__(self, grid_size, path):
        self.path = path
        self.window_size = self.CELL_SIZE * grid_size
        self.visible_steps = 0
        self.head_color = self.HEAD_COLOR
        pyglet.window.Window.__init__(self,
                                      width=self.window_size,
                                      height=self.window_size,
                                      caption='watchworm')
        self.set_location(300, 300)
        pyglet.clock.schedule_interval(self.step, self.STEP_TIME)
        
    def step(self, dt):
        self.visible_steps += 1
        if self.visible_steps == len(self.path):
            pyglet.clock.unschedule(self.step)
            self.head_color = self.STOP_COLOR
            
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
                    chain([self.head_color], repeat(self.BODY_COLOR)))
        for cell_position, color in reversed(list(worm)):
            self.draw_cell(cell_position, color)

def process(grid_size, path):
    window = WormWindow(grid_size, path)
    pyglet.app.run()

def main():
    process(10, [(0, 0), (0, 1), (1, 1)])

if __name__ == '__main__':
    main()
