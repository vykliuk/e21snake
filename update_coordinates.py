import random
from analogio import AnalogIn

def update_coordinate(snake_head, joystick_values, current_direction):
    """
    Moves the snake's head based on joystick input or keeps it moving in the same direction if joystick is neutral.

    Parameters:
        snake_head (tuple): Current position of the snake's head (x, y).
        joystick_values (tuple): Joystick values (trace1, trace2).
        current_direction (str): Current direction of the snake ('up', 'down', 'left', 'right').

    Returns:
        tuple: New position of the snake's head.
        str: Updated direction of the snake.
    """
    trace1, trace2 = joystick_values

    # Determine direction from joystick values
    if trace1 < 20000:  # Up
        direction = "up"
    elif trace1 > 45000:  # Down
        direction = "down"
    elif trace2 < 20000:  # Left
        direction = "left"
    elif trace2 > 45000:  # Right
        direction = "right"
    else:
        direction = current_direction  # Keep moving in the current direction if joystick is neutral

    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    dx, dy = moves[direction]
    new_x = snake_head[0] + dx
    new_y = snake_head[1] + dy

    # Keep the head within bounds (0-7 grid)
    if 0 <= new_x <= 7 and 0 <= new_y <= 7:
        return (new_x, new_y), direction

    return snake_head, direction  # No change if out of bounds