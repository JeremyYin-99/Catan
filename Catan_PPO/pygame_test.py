import pygame
import random
# Define the dimensions of the window
window_width = 1200
window_height = 800

# Initialize Pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((window_width, window_height))

# Set the title of the window
pygame.display.set_caption("Settlers of Catan")

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the background color of the window
screen.fill(WHITE)

# Function to draw a hexagon
def draw_hexagon(x, y, size, color):
  points = [(x, y - size),
            (x + size * 0.87, y - size / 2),
            (x + size * 0.87, y + size / 2),
            (x, y + size),
            (x - size * 0.87, y + size / 2),
            (x - size * 0.87, y - size / 2)]
  pygame.draw.polygon(screen, color, points)

# Draw the hexagons on the board
for y in range(5):
  for x in range(5):
    if x == 0 and y == 0:
      continue
    elif x == 4 and y == 0:
      continue
    elif x == 4 and y == 4:
      continue
    elif x == 0 and y == 4:
      continue
    elif y == 2 and x > 1:
      continue
    elif y == 3 and x < 2:
      continue
    else:
      draw_hexagon(x * 200 + 100, y * 170 + 85, 50, BLACK)




# Update the display
pygame.display.flip()

# Define constants for the board dimensions
BOARD_WIDTH = 700
BOARD_HEIGHT = 600

# Define constants for the hexagon dimensions
HEX_WIDTH = 100
HEX_HEIGHT = 86

# Define the vertices of the hexagon
vertices = [
    (HEX_WIDTH / 2, 0),
    (HEX_WIDTH, HEX_HEIGHT / 4),
    (HEX_WIDTH, 3 * HEX_HEIGHT / 4),
    (HEX_WIDTH / 2, HEX_HEIGHT),
    (0, 3 * HEX_HEIGHT / 4),
    (0, HEX_HEIGHT / 4)
]

# Define the colors for the hexagons
colors = [
    "red", "orange", "yellow",
    "green", "blue", "purple"
]

# Initialize Pygame
pygame.init()

# Set the window title
pygame.display.set_caption("Settlers of Catan")

# Set the window size
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

# Set the background color
screen.fill((255, 255, 255))

# Draw the hexagons on the board
for y in range(5):
  for x in range(5):
    if x == 0 and y == 0:
      continue
    elif x == 4 and y == 0:
      continue
    elif x == 4 and y == 4:
      continue
    elif x == 0 and y == 4:
      continue
    elif y == 2 and x > 1:
      continue
    elif y == 3 and x < 2:
      continue
    else:
      # Choose a random color for the hexagon
      color = random.choice(colors)

      # Draw the hexagon
      pygame.draw.polygon(screen, color, [(x * HEX_WIDTH + HEX_WIDTH / 2, y * HEX_HEIGHT + HEX_HEIGHT / 4),
                                         (x * HEX_WIDTH + HEX_WIDTH, y * HEX_HEIGHT + HEX_HEIGHT / 4),
                                         (x * HEX_WIDTH + HEX_WIDTH, y * HEX_HEIGHT + 3 * HEX_HEIGHT / 4),
                                         (x * HEX_WIDTH + HEX_WIDTH / 2, y * HEX_HEIGHT + HEX_HEIGHT),
                                         (x * HEX_WIDTH, y * HEX_HEIGHT + 3 * HEX_HEIGHT / 4),
                                         (x * HEX_WIDTH, y * HEX_HEIGHT + HEX_HEIGHT / 4)])

# Update the display
pygame.display.update()


# Run the game loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

# Quit Pygame
pygame.quit()

