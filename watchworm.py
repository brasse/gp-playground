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
        if self.visible_steps > len(self.path):
            self.visible_steps = len(self.path)
            
    def set_cell_color(self, position, color):
        x, y = position
        left = x * self.CELL_SIZE + self.BORDER
        lower = y * self.CELL_SIZE + self.BORDER
        side = self.CELL_SIZE - 2 * self.BORDER
        vs = (left, lower, 
              left + side, lower,
              left + side, lower + side,
              left, lower + side)
        glColor3f(*color)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', vs))

    def on_draw(self):
        glClearColor(0.3, 0.3, 0.4, 1.0) # Dark grey
        self.clear()
        # draw body
        for cell in self.path[:self.visible_steps]:
            self.set_cell_color(cell, self.BODY_COLOR)
        # draw head
        if self.visible_steps:
            self.set_cell_color(self.path[self.visible_steps - 1],
                                self.HEAD_COLOR)
            
def process(grid_size, path=None, program=None):
    window = WormWindow(grid_size, [(0, 0), (0, 1), (1, 1)])
    pyglet.app.run()

def main():
    process(10)

if __name__ == '__main__':
    main()
