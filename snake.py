import random
from analogio import AnalogIn

def read_joystick():
    # TODO
    return (0, 0)

def update_head(snake_head, joystick_values, current_direction):
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
    direction = current_direction
    # Determine direction from joystick values
    if trace1 < 20000:  # Up
        if current_direction != (1,0): # currently down
            direction = "up"
    elif trace1 > 45000:  # Down
        if current_direction != (1,0): # currently up
            direction = "down"
    elif trace2 < 20000:  # Left
        if current_direction != (0,-1): # currently right
            direction = "left"
    elif trace2 > 45000:
        if current_direction != (0,1): # currently left
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

def eat_apple(tail_arr, apple, head):
    """
    in the case head encountered an apple:
    inserts old head at the beginning of the tail array,
    returns modified tail array and a newly generated apple
    """
    tail_arr.insert(0, head)
    #head[0] = apple[0]
    #head[1] = apple[1]
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    apple = (x,y)
    # TODO: play sound
    while apple in tail_arr or apple == head:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        apple = (x,y)
    return tail_arr, apple
 
def main():
    apple = (2, 5) #default value
    head = (4,3)
    current_direction = (0,1)
    tail_arr = [] # descending order from head
    while True:
        joystick_values = read_joystick()
        new_head, new_direction = update_head(head, joystick_values, current_direction)
        current_direction = new_direction
        if new_head in tail_arr or new_head == head:
            break # collision: game over
        elif new_head ==  apple: # head ate apple
            tail_arr, apple = eat_apple(tail_arr, apple, head)
        else:
            tail_arr.pop() # remove last element in the tail
