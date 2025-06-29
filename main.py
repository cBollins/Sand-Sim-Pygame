import pygame, sys
from simulation import Simulation

pygame.init()
pygame.mouse.set_visible(False)

# defining variables
WINDOW_WIDTH = pygame.display.Info().current_w 
WINDOW_HEIGHT = pygame.display.Info().current_h
cell_size = 8
fps = 120
background = (25, 25, 25) # pygame handles colours as RGB tuples
rainbow_hue_seed = 0.0 # set initial rainbow hue

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Falling Sand Game")

# -------------------------------------------------------------------------------
# In computer graphics, the window is actually the second quadrant.
# Cartesian x is the same, but y is reflected to -y.
# => top left corner is (0, 0)
# -------------------------------------------------------------------------------

clock = pygame.time.Clock() # tickrate effectively
simulation = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, cell_size)

# Set font for text (this will be used to draw the control instructions)
font = pygame.font.SysFont('Calibri', 18)

# Define the control instructions text
controls_text = [
    "Controls:", "(S), (R), (Q) for Sand, Rock, Rainbow. (E) to erase.",
    "Scroll for brush size, (SPACE) to reset, (ESC) to quit."
]

# Function to render text
def render_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

# -------------------------------------------------------------------------------
# Simulation Loop
# -------------------------------------------------------------------------------

while True: # runs continuously until "break". This while loop happens every single tick
    # quick iteration for the rainbow seed
    rainbow_hue_seed += 0.0025
    rainbow_hue_seed %= 1 # clamp to [0, 1)

    # 1. event handling
    simulation.handle_controls()

    # 2. update game state
    simulation.update(rainbow_hue_seed)

    # 3. drawing
    window.fill(background)
    simulation.draw(window, rainbow_hue_seed)

    y_offset = 10
    for line in controls_text:
        render_text(line, font, (200, 200, 200), 10, y_offset)
        y_offset += 25

    pygame.display.flip()
    clock.tick(fps)