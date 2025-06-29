# -------------------------------------------------------------------------------
# Create a simulation class.
# This class is responsible for
# 1. creating and managing the grid
# 2. adding and removing particles,
# 3. coordinating the overall simulation
# -------------------------------------------------------------------------------

import pygame, sys, random, colorsys
from grid import Grid
from particle import SandParticle, RockParticle, RainbowSand

class Simulation:
    def __init__(self, w, h, s):
        self.grid = Grid(w, h, s)
        self.cell_size = s
        self.mode = "sand" # initial mode
        self.brush_size = 3
        self.rainbow_seed = 0.0

    def draw(self, window, rainbow_hue_seed):
        self.rainbow_seed = rainbow_hue_seed
        self.grid.draw(window)
        self.draw_brush(window, rainbow_hue_seed)

    def add_particle(self, row, col):
        if self.mode == "sand":
            if random.random() < 0.23: # some sand particles are omitted
                self.grid.add_particle(row, col, SandParticle)
        if self.mode == "rainbow":
            if random.random() < 0.23: # some sand particles are omitted
                self.grid.add_particle(row, col, lambda: RainbowSand(self.rainbow_seed))
        elif self.mode == "rock":
            self.grid.add_particle(row, col, RockParticle)

    def remove_particle(self, row, col):
        self.grid.remove_particle(row, col)

    # -------------------------------------------------------------------------------
    # THE RULES:
    # > check cell below. if empty, move down.
    # > cell below full => move into a bottom left/right cell - at random if both are empty.
    # > else: there is nowhere to go... the sand must stay.
    # -------------------------------------------------------------------------------

    def update(self, rainbow_hue_seed):
        self.rainbow_seed = rainbow_hue_seed
        for row in range(self.grid.rows - 2, -1, -1): # bottom to top search instead.
            # want to check in a snake-like sequence, as to remove directional bias
            if row % 2 == 0:
                column_range = range(self.grid.columns)
            else: column_range = reversed(range(self.grid.columns))
            for col in column_range:
                particle = self.grid.get_cell(row, col)
                if isinstance(particle, SandParticle) or isinstance(particle, RainbowSand):
                    new_pos = particle.update(self.grid, row, col)
                    if new_pos != (row, col):
                        self.grid.set_cell(new_pos[0], new_pos[1], particle)
                        self.grid.remove_particle(row, col)

    def restart(self):
        self.grid.clear()

    # event processing
    def handle_controls(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:
                self.handle_key(ev)

            if ev.type == pygame.MOUSEWHEEL:
                if ev.y > 0:
                    self.brush_size = min(15, self.brush_size + 2)
                    print(f"Brush size +1, radius = {self.brush_size}px")
                elif ev.y < 0:
                    self.brush_size = max(1, self.brush_size - 2)
                    print(f"Brush size -1, radius = {self.brush_size}px")

        self.handle_mouse()

    def handle_key(self, ev):
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                self.restart() # clear grid on spacebar press
            elif ev.key == pygame.K_s:
                self.mode = "sand"
                print("Sand Mode")
            elif ev.key == pygame.K_q:
                self.mode = "rainbow"
                print("Rainbow Sand")
            elif ev.key == pygame.K_r:
                self.mode = "rock"
                print("Rock Mode")
            elif ev.key == pygame.K_e:
                self.mode = "eraser"
                print("Eraser Mode")
            elif ev.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def handle_mouse(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0]: # if LMB pressed,
            pos = pygame.mouse.get_pos()

            # convert to grid co ords...
            row = pos[1] // self.cell_size
            col = pos[0] // self.cell_size

            self.apply_brush(row, col)

    def apply_brush(self, row, col):
        rad = self.brush_size // 2
        for r in range(-rad, rad + 1):
            for c in range(-rad, rad + 1):
                current_row = row + r
                current_col = col + c

                # check whether to erase or add a particle
                if self.mode == "eraser":
                    self.grid.remove_particle(current_row, current_col)
                else: self.add_particle(current_row, current_col)

    def draw_brush(self, window, rainbow_hue_seed):
        self.rainbow_seed = rainbow_hue_seed
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0] // self.cell_size
        row = mouse_pos[1] // self.cell_size

        visual_size = self.brush_size * self.cell_size
        rad = (self.brush_size // 2) * self.cell_size

        colour = (255, 0, 0) # default, red for things going wrong

        if self.mode == "rock":
            colour = (100, 100, 100)
        elif self.mode == "sand":
            colour = (189, 147, 68)
        elif self.mode == "rainbow":
            hsv_color = colorsys.hsv_to_rgb(rainbow_hue_seed, 1, 1)
            colour = tuple(int(c * 255) for c in hsv_color) # the rainbow colour
        elif self.mode == "eraser":
            colour = (255, 140, 190)

        pygame.draw.rect(
            window, 
            colour, 
            (col * self.cell_size - rad, row * self.cell_size - rad, visual_size, visual_size)
        )