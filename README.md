# Neopixel Greedy Snake

This project is the final submission for **E21: Computer Engineering Fundamentals** at Swarthmore College. The team members for this project are:

- **Alina Vykliuk**
- **Howard Wang**
- **Joey Alander**

## Project Overview
This project implements a Snake game using an 8x8 NeoPixel board as the game grid. The primary features and design elements are outlined below:

### Features
- **Grid**: An 8x8 NeoPixel LED board serves as the game grid, where each LED represents a single cell.
- **Snake**:
  - The snake's **head** is displayed in green.
  - The snake's **body** is displayed in blue.
- **Food**:
  - A single red LED indicates the food’s position.
- **Movement**:
  - LEDs update dynamically to show the snake's new position.
  - LEDs behind the snake's tail turn off as it moves.
- **Controls**:
  - Players can change the snake's direction using buttons or a joystick.
- **Collisions**:
  - The game detects collisions with walls or the snake's own body.
  - On collision, the game resets.
- **Growth**:
  - Eating food increases the snake's length.
  - The score updates accordingly.

---

Playthrough: https://www.youtube.com/shorts/JnNA7JFOAME.
