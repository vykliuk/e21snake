import board
import neopixel
from analogio import AnalogIn
import random
from time import sleep
from adafruit_circuitplayground.express import cpx

# Setup
pixels = neopixel.NeoPixel(board.A1, 64, brightness=0.1, auto_write=False)
vert = AnalogIn(board.A3)
horiz = AnalogIn(board.A2)

def play_start():
    """game start sound"""
    cpx.play_tone(262, 0.1) 
    sleep(0.05)
    cpx.play_tone(330, 0.1)  
    sleep(0.05)
    cpx.play_tone(392, 0.1)  

def play_game_over():
    """game over sound"""
    cpx.play_tone(392, 0.2) 
    sleep(0.1)
    cpx.play_tone(330, 0.2) 
    sleep(0.1)
    cpx.play_tone(262, 0.3)  

def test_joystick():
    # Up test
    while True:
        if vert.value < 20000:
            for i in range(8):
                pixels[i] = (0, 255, 0)
            pixels.show()
            sleep(0.5)
            break
        pixels.fill((0, 0, 0))
        for i in range(8):
            pixels[i] = (30, 30, 30)
        pixels.show()
        sleep(0.1)
    
    # Down test
    while True:
        if vert.value > 45000:
            for i in range(56, 64):
                pixels[i] = (0, 255, 0)
            pixels.show()
            sleep(0.5)
            break
        pixels.fill((0, 0, 0))
        for i in range(56, 64):
            pixels[i] = (30, 30, 30)
        pixels.show()
        sleep(0.1)
    
    # Left test
    while True:
        if horiz.value < 20000:
            for i in range(0, 64, 8):
                pixels[i] = (0, 255, 0)
            pixels.show()
            sleep(0.5)
            break
        pixels.fill((0, 0, 0))
        for i in range(0, 64, 8):
            pixels[i] = (30, 30, 30)
        pixels.show()
        sleep(0.1)
    
    # Right test
    while True:
        if horiz.value > 45000:
            for i in range(7, 64, 8):
                pixels[i] = (0, 255, 0)
            pixels.show()
            sleep(0.5)
            break
        pixels.fill((0, 0, 0))
        for i in range(7, 64, 8):
            pixels[i] = (30, 30, 30)
        pixels.show()
        sleep(0.1)

def read_joystick():
    return (vert.value, horiz.value)

def update_head(head, joystick_values, direction):
    v, h = joystick_values
    
    # Update direction based on joystick
    if v < 20000 and direction != "down":  # Up
        direction = "up"
    elif v > 45000 and direction != "up":  # Down
        direction = "down"
    elif h < 20000 and direction != "right":  # Left
        direction = "left"
    elif h > 45000 and direction != "left":  # Right
        direction = "right"
    
    x, y = head
    if direction == "up":
        x = (x - 1) % 8
    elif direction == "down":
        x = (x + 1) % 8
    elif direction == "left":
        y = (y - 1) % 8
    else:  # right
        y = (y + 1) % 8
        
    return (x, y), direction

def main():
    test_joystick()
    play_start() 
    
    head = (4, 3)
    direction = "right"
    tail = []
    
    # Random initial apple
    x = random.randint(0, 7)
    y = random.randint(0, 7)
    apple = (x, y)
    while apple == head:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        apple = (x, y)
    
    while True:
        new_head, new_direction = update_head(head, read_joystick(), direction)
        
        if new_head in tail:
            play_game_over()  # Play game over sound
            break
            
        if new_head == apple:
            tail.append(head)
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            apple = (x, y)
            while apple == new_head or apple in tail:
                x = random.randint(0, 7)
                y = random.randint(0, 7)
                apple = (x, y)
        elif tail:
            tail.append(head)
            tail.pop(0)
        elif new_head != head:
            tail.append(head)
        
        head = new_head
        direction = new_direction
        
        # Draw
        pixels.fill((0, 0, 0))
        pixels[apple[0] * 8 + apple[1]] = (255, 0, 0)  # Apple
        pixels[head[0] * 8 + head[1]] = (0, 255, 0)    # Head
        for tx, ty in tail:
            pixels[tx * 8 + ty] = (0, 0, 255)          # Tail
        pixels.show()
        
        sleep(0.3)
    
    # Game over
    pixels.fill((255, 0, 0))
    pixels.show()
    sleep(1)
    main()

main()
