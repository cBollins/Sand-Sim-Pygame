# create a sand particle
import random
import colorsys

class SandParticle:
    def __init__(self):
        self.colour = randomcolour((0.11, 0.13), (0.6, 0.75), (0.7, 0.9)) # generic, sandy colour

    def update(self, grid, row, col):
        if grid.is_empty(row + 1, col): # remember conventions
            return row + 1, col
        else:
            offsets = [-1, 1] # bottom left and right
            random.shuffle(offsets)
            for offset in offsets:
                new_col = col + offset
                if grid.is_empty(row + 1, new_col):
                    return row + 1, new_col
        return row, col
    
class RockParticle:
    def __init__(self):
        self.colour = randomcolour((0, 0.1), (0.1, 0.3), (0.3, 0.5))

class RainbowSand:
    def __init__(self, rainbow_seed):
        # rainbow seed between (0, 1)
        self.colour = randomcolour((rainbow_seed, rainbow_seed), (0.5, 0.9), (0.7, 1.0))

    def update(self, grid, row, col):
        if grid.is_empty(row + 1, col): # remember conventions
            return row + 1, col
        else:
            offsets = [-1, 1] # bottom left and right
            random.shuffle(offsets)
            for offset in offsets:
                new_col = col + offset
                if grid.is_empty(row + 1, new_col):
                    return row + 1, new_col
        return row, col

def randomcolour(hue_range, saturation_range, value_range):
    # want to make somewhat realistic colours, using the HSV model.
    # -> hue, saturation, value.
    hue = random.uniform(*hue_range)
    saturation = random.uniform(*saturation_range)
    value = random.uniform(*value_range)
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value) # convert to rgb values as floats
    return int(r * 255), int(g * 255), int(b * 255) # rgb values as 0-255 ints