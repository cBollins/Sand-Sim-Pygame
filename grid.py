import pygame
grid_colour = (50, 50, 50)

class Grid:
    def __init__(self, w, h, cell_size):
        self.rows = h // cell_size
        self.columns = w // cell_size
        self.cell_size = cell_size
        
        # The same as making a np.fill() array with shape (w, h) full of "None"
        self.cells = [[None for _ in range(self.columns)] for _ in range(self.rows)]

    def draw(self, window):
        for row in range(self.rows):
            for col in range(self.columns):
                particle = self.cells[row][col]
                if particle is not None:
                    pygame.draw.rect(
                        window, particle.colour, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                    )

    def add_particle(self, row, col, particle_type):
        if 0 <= row < self.rows and 0 <= col < self.columns and self.is_empty(row, col):
            self.cells[row][col] = particle_type()

    def remove_particle(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.cells[row][col] = None

    def is_empty(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            if self.cells[row][col] is None:
                return True
        return False
    
    def set_cell(self, row, col, particle):
        if not(0 <= row < self.rows and 0 <= col < self.columns):
            return # not in grid
        self.cells[row][col] = particle

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.cells[row][col]
        return None
    
    def clear(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.remove_particle(row, col)