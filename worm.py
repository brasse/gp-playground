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

def move(position, heading, grid_size):
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
        return position
    else:
        return np
    
def step(program, instruction_index, position, heading, grid_size):
    instruction = program[instruction_index % len(program)]
    if instruction == TURN_LEFT or instruction == TURN_RIGHT:
        return (instruction_index + 1, position,
                turn(heading, instruction == TURN_RIGHT))
    else:
        return (instruction_index + 1, move(position, heading, grid_size),
                heading)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
