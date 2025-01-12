import gc
from board import A1, A2, A3
from neopixel import NeoPixel
from analogio import AnalogIn
from random import randint
from time import sleep
from adafruit_circuitplayground.express import cpx

gc.collect()

pixels = NeoPixel(A1, 64, brightness=0.1, auto_write=False)
vert = AnalogIn(A3)
horiz = AnalogIn(A2)


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

def play_start():
    cpx.play_tone(262, 0.1)
    sleep(0.05)
    cpx.play_tone(330, 0.1)
    sleep(0.05)
    cpx.play_tone(392, 0.1)

def play_game_over():
    cpx.play_tone(392, 0.2)
    sleep(0.1)
    cpx.play_tone(330, 0.2)
    sleep(0.1)
    cpx.play_tone(262, 0.3)

def read_joystick():
    return (vert.value, horiz.value)

def update_head(head, joystick_values, direction):
    v, h = joystick_values
    if v < 20000 and direction != "down":
        direction = "up"
    elif v > 45000 and direction != "up":
        direction = "down"
    elif h < 20000 and direction != "right":
        direction = "left"
    elif h > 45000 and direction != "left":
        direction = "right"

    x, y = head
    if direction == "up":
        x = (x - 1) % 8
    elif direction == "down":
        x = (x + 1) % 8
    elif direction == "left":
        y = (y - 1) % 8
    else:
        y = (y + 1) % 8
    return (x, y), direction

DIGITS = {
    0: [1,1,1,1,0,1,1,0,1,1,0,1,1,1,1],
    1: [0,1,0,1,1,0,0,1,0,0,1,0,1,1,1],
    2: [1,1,1,0,0,1,1,1,1,1,0,0,1,1,1],
    3: [1,1,1,0,0,1,1,1,1,0,0,1,1,1,1],
    4: [1,0,1,1,0,1,1,1,1,0,0,1,0,0,1],
    5: [1,1,1,1,0,0,1,1,1,0,0,1,1,1,1],
    6: [1,1,1,1,0,0,1,1,1,1,0,1,1,1,1],
    7: [1,1,1,0,0,1,0,1,0,0,1,0,0,1,0],
    8: [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1],
    9: [1,1,1,1,0,1,1,1,1,0,0,1,1,1,1],
}

def display_number(num):
    pixels.fill((0,0,0))
    pixels.show()
    if (num // 10) > 0:
        dig = 2
    else:
        dig = 1

    if dig == 1:
        first_dig = 0
    else:
        first_dig = num // 10
    second_dig = num % 10

    index = 0
    for i in range(2, 7):
        for j in range(0, 3):
            if DIGITS[first_dig][index]:
                pixels[(i*8)+j] = (255, 255, 255)
            index += 1

    index = 0
    for i in range(2, 7):
        for j in range(4, 7):
            if DIGITS[second_dig][index]:
                pixels[(i*8)+j] = (255,255,255)
            index += 1
    pixels.show()

def main():
    test_joystick()
    gc.collect()
    play_start()

    x = randint(0, 7)
    y = randint(0, 7)
    head = (x, y)
    direction = "right"
    tail = []

    x = randint(0, 7)
    y = randint(0, 7)
    apple = (x, y)
    while apple == head:
        x = randint(0, 7)
        y = randint(0, 7)
        apple = (x, y)

    gc.collect()
    while True:
        new_head, new_direction = update_head(head, read_joystick(), direction)

        if new_head in tail:
            play_game_over()
            break

        if new_head == apple:
            tail.append(head)
            # If it hits tail or head again, just overwrite anyway
            x = randint(0,7)
            y = randint(0,7)
            apple = (x,y)
            cpx.play_tone(440, 0.05)
            cpx.play_tone(554, 0.05)
        elif tail:
            tail.append(head)
            tail.pop(0)
        else:
            tail.append(head)

        head = new_head
        direction = new_direction

        pixels.fill((0,0,0))
        pixels[apple[0]*8 + apple[1]] = (255,0,0)
        pixels[head[0]*8 + head[1]] = (0,255,0)
        for tx, ty in tail:
            pixels[tx*8 + ty] = (0,0,255)
        pixels.show()

        sleep(0.3)

    score = len(tail) + 1
    print("Your score is " + str(score) + "!")
    pixels.fill((255,0,0))
    pixels.show()
    sleep(1)

    # Display the score in digits
    display_number(score)

main()
