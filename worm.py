import gp
import watchworm

import functools
import itertools
import random

TURN_LEFT = 0
TURN_RIGHT = 1
MOVE_FORWARD = 2

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def turn(heading, turn_right):
    '''
    Return the new heading after making a turn left or right.

    >>> turn(0, True)
    1
    >>> turn(3, True)
    0
    >>> turn(3, False)
    2
    >>> turn(0, False)
    3
    '''

    return (heading + (1 if turn_right else -1)) % 4

def move(position, heading, grid_size, harsh):
    '''
    Move one step forward and return the new position. If the now position
    is outside the grid, return the old position.

    >>> move((1, 0), SOUTH, 3)
    (1, 0)
    >>> move((1, 2), NORTH, 3)
    (1, 2)
    >>> move((2, 1), EAST, 3)
    (2, 1)
    >>> move((0, 1), WEST, 3)
    (0, 1)
    >>> move((1, 1), NORTH, 3)
    (1, 2)
    >>> move((1, 1), EAST, 3)
    (2, 1)
    >>> move((1, 1), SOUTH, 3)
    (1, 0)
    >>> move((1, 1), WEST, 3)
    (0, 1)
    '''
    DELTA = {NORTH : (0, 1), EAST : (1, 0),
             SOUTH : (0, -1), WEST : (-1, 0)}

    def add(a, b):
        return a[0] + b[0], a[1] +  b[1]

    np = add(position, DELTA[heading])
    if np[0] < 0 or np[1] < 0 or np[0] >= grid_size or np[1] >= grid_size:
        if harsh:
            raise Exception('Worm left the grid and died.')
        else:
            return position
    else:
        return np
    
def step(program, instruction_index, position, heading, grid_size, harsh):
    instruction = program[instruction_index % len(program)]
    if instruction == TURN_LEFT or instruction == TURN_RIGHT:
        return (instruction_index + 1, 
                position,
                turn(heading, instruction == TURN_RIGHT))
    else:
        return (instruction_index + 1, 
                move(position, heading, grid_size, harsh),
                heading)

def run(program, position, heading, grid_size, max_steps, harsh=False):
    '''
    Run the program for max_steps number of steps and return the path
    that the worm travelled. The same position may appear in sequence
    if it spent more than one step in that position (i.e. made a turn).

    >>> run([MOVE_FORWARD], (0, 0), EAST, 3, 3)
    [(0, 0), (1, 0), (2, 0), (2, 0)]
    >>> run([MOVE_FORWARD, TURN_LEFT, MOVE_FORWARD, MOVE_FORWARD],
    ...     (1, 1), EAST, 3, 4)
    [(1, 1), (2, 1), (2, 1), (2, 2), (2, 2)]
    >>> run([MOVE_FORWARD, TURN_RIGHT], (1, 1), EAST, 3, 5)
    [(1, 1), (2, 1), (2, 1), (2, 0), (2, 0), (1, 0)]
    '''

    path = [position]
    instruction_index = 0
    for _ in xrange(max_steps):
        instruction_index, position, heading = \
            step(program, instruction_index, position, heading, grid_size,
                 harsh)
        path.append(position)
    return path

def random_program(length):
    return [random.choice((TURN_LEFT, TURN_RIGHT, MOVE_FORWARD))
            for _ in xrange(length)]

def fitness(position, heading, grid_size, max_steps, alfa, harsh):
    def f(program):
        try:
            path = run(program, position, heading, grid_size, max_steps, harsh)
            return len(set(path)) - alfa * len(program)
        except:
            return 0
    return f

def test():
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    population = [random_program(5) for _ in xrange(100)]
    keep = 15
    start_position = (0, 0)
    start_heading = NORTH
    grid_size = 10
    max_steps = pow(grid_size, 2) * 2
    alfa = 0.2
    harsh = False
    fitness_function = fitness(start_position, start_heading,
                               grid_size, max_steps, alfa, harsh)
    selection_function = gp.truncation_selection(keep)
    operations = [(0.10, gp.mutate(functools.partial(random_program, 5))),
                  (0.70, gp.crossover)]

    step_seq = itertools.chain(itertools.repeat(5, 5),
                               itertools.repeat(100, 5),
                               itertools.repeat(1000))
    g = 0
    while True:
        steps = step_seq.next()
        termination_condition = lambda ep, g: g == steps
        population = gp.gp(population, fitness_function,
                           selection_function, operations,
                           termination_condition)
        g += steps
        path = run(population[0], start_position, start_heading,
                   grid_size, max_steps, harsh)
        print 'generation: %d' % g
        fitness = fitness_function(population[0])
        print 'fitness:    %d (%.2f)' % (fitness,
                                         len(set(path)) / pow(grid_size, 2.0)) 
        print 'length:     %d' % len(population[0])
        print
        watchworm.process(grid_size, path)
