import sys
import time
from collections import defaultdict
from copy import deepcopy
import pygame
import random
import colorsys

from game_system import GOSPER_GLIDER
from template_grid import Grid, Neighbours

class GameSystem:
    """ This class represents the game system. """
    
    def __init__(self, master):
        """ Initialize attributes of the gamesystem. """
        self.master = master
        self.paused = False
        self.speed = 10  # frames per second
        self.color_scheme = {
            'background': (0, 0, 0),
            'cell': (255, 0, 0),
            'grid': (50, 50, 50),
            'highlight': (0, 255, 0)
        }
        self.brush_size = 1
        self.highlight_cells = set()
        self.generation = 0
        self.mode = "classic"  # classic, heatmap, or trails
        self.cell_age = defaultdict(int)
        self.trail_length = 5
        self.patterns = {
            'glider': [(0, 0), (1, 1), (2, 1), (0, 2), (1, 2)],
            'blinker': [(0, 0), (1, 0), (2, 0)],
            'pulsar': [(2,0),(3,0),(4,0),(8,0),(9,0),(10,0),(0,2),(5,2),(7,2),(12,2),(0,3),(5,3),(7,3),(12,3),(0,4),(5,4),(7,4),(12,4),(2,5),(3,5),(4,5),(8,5),(9,5),(10,5),(2,7),(3,7),(4,7),(8,7),(9,7),(10,7),(0,8),(5,8),(7,8),(12,8),(0,9),(5,9),(7,9),(12,9),(0,10),(5,10),(7,10),(12,10),(2,12),(3,12),(4,12),(8,12),(9,12),(10,12)],
            'spaceship': [(1,0),(4,0),(0,1),(0,2),(4,2),(0,3),(1,3),(2,3),(3,3)],
            'pentadecathlon': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9)]
        }
    
    @staticmethod
    def get_neighbours(grid: Grid, x: int, y: int) -> Neighbours:
        """ Gets the neighbour states for a cell in (x, y) on the grid. """
        offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        possible_neighbours = {((x + x_add) % grid.dim.width, (y + y_add) % grid.dim.height) for x_add, y_add in offsets}
        alive = {pos for pos in possible_neighbours if pos in grid.cells}
        return Neighbours(alive, possible_neighbours - alive)
    
    def update_grid(self, grid: Grid) -> Grid:
        """ Returns the next iteration of the game of life. """
        new_cells = set()
        undead = defaultdict(int)
        new_cell_age = defaultdict(int)
        
        for x in range(grid.dim.width):
            for y in range(grid.dim.height):
                alive_neighbours, dead_neighbours = self.get_neighbours(grid, x, y)
                if (x, y) in grid.cells:
                    if len(alive_neighbours) in [2, 3]:
                        new_cells.add((x, y))
                        new_cell_age[(x, y)] = self.cell_age[(x, y)] + 1
                else:
                    undead[(x, y)] = len(alive_neighbours)
        
        for pos, count in undead.items():
            if count == 3:
                new_cells.add(pos)
                new_cell_age[pos] = 0
        
        self.cell_age = new_cell_age
        return Grid(grid.dim, new_cells)
    
    def draw_grid(self, screen: pygame.Surface, grid: Grid) -> None:
        """ Draws the game of life on the pygame.Surface object. """
        cell_width = screen.get_width() / grid.dim.width
        cell_height = screen.get_height() / grid.dim.height
        
        # Draw grid lines
        for x in range(grid.dim.width + 1):
            pygame.draw.line(screen, self.color_scheme['grid'], (x * cell_width, 0), (x * cell_width, screen.get_height()))
        for y in range(grid.dim.height + 1):
            pygame.draw.line(screen, self.color_scheme['grid'], (0, y * cell_height), (screen.get_width(), y * cell_height))
        
        # Draw cells
        for x, y in grid.cells:
            if self.mode == "classic":
                color = self.color_scheme['highlight'] if (x, y) in self.highlight_cells else self.color_scheme['cell']
            elif self.mode == "heatmap":
                hue = min(self.cell_age[(x, y)] / 100, 1)  # Max age of 100 generations
                color = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1, 1)]
            elif self.mode == "trails":
                age = min(self.cell_age[(x, y)], self.trail_length)
                color = [int(c * (self.trail_length - age) / self.trail_length) for c in self.color_scheme['cell']]
            
            pygame.draw.rect(
                screen,
                color,
                (x * cell_width + 1, y * cell_height + 1, cell_width - 1, cell_height - 1)
            )

    def add_pattern(self, grid: Grid, pattern: str, x: int, y: int) -> Grid:
        """ Adds a predefined pattern to the grid at the specified position. """
        new_cells = grid.cells.copy()
        for dx, dy in self.patterns.get(pattern, []):
            new_x = (x + dx) % grid.dim.width
            new_y = (y + dy) % grid.dim.height
            new_cells.add((new_x, new_y))
        return Grid(grid.dim, new_cells)

    def randomize_grid(self, grid: Grid, density: float) -> Grid:
        """ Randomizes the grid with the given density of live cells. """
        new_cells = set()
        for x in range(grid.dim.width):
            for y in range(grid.dim.height):
                if random.random() < density:
                    new_cells.add((x, y))
        return Grid(grid.dim, new_cells)

def main():
    """ Main entry point. """
    grid = GOSPER_GLIDER
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Advanced Game of Life")
    
    game_system = GameSystem(None)
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 24)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_system.paused = not game_system.paused
                elif event.key == pygame.K_UP:
                    game_system.speed = min(60, game_system.speed + 5)
                elif event.key == pygame.K_DOWN:
                    game_system.speed = max(1, game_system.speed - 5)
                elif event.key == pygame.K_r:
                    grid = Grid(grid.dim, set())  # Reset to empty grid
                    game_system.cell_age.clear()
                elif event.key == pygame.K_g:
                    grid = GOSPER_GLIDER  # Reset to Gosper Glider
                    game_system.cell_age.clear()
                elif event.key == pygame.K_1:
                    game_system.brush_size = 1
                elif event.key == pygame.K_2:
                    game_system.brush_size = 2
                elif event.key == pygame.K_3:
                    game_system.brush_size = 3
                elif event.key == pygame.K_l:
                    x, y = pygame.mouse.get_pos()
                    cell_x = x // (screen.get_width() // grid.dim.width)
                    cell_y = y // (screen.get_height() // grid.dim.height)
                    grid = game_system.add_pattern(grid, 'glider', cell_x, cell_y)
                elif event.key == pygame.K_b:
                    x, y = pygame.mouse.get_pos()
                    cell_x = x // (screen.get_width() // grid.dim.width)
                    cell_y = y // (screen.get_height() // grid.dim.height)
                    grid = game_system.add_pattern(grid, 'blinker', cell_x, cell_y)
                elif event.key == pygame.K_p:
                    x, y = pygame.mouse.get_pos()
                    cell_x = x // (screen.get_width() // grid.dim.width)
                    cell_y = y // (screen.get_height() // grid.dim.height)
                    grid = game_system.add_pattern(grid, 'pulsar', cell_x, cell_y)
                elif event.key == pygame.K_s:
                    x, y = pygame.mouse.get_pos()
                    cell_x = x // (screen.get_width() // grid.dim.width)
                    cell_y = y // (screen.get_height() // grid.dim.height)
                    grid = game_system.add_pattern(grid, 'spaceship', cell_x, cell_y)
                elif event.key == pygame.K_d:
                    x, y = pygame.mouse.get_pos()
                    cell_x = x // (screen.get_width() // grid.dim.width)
                    cell_y = y // (screen.get_height() // grid.dim.height)
                    grid = game_system.add_pattern(grid, 'pentadecathlon', cell_x, cell_y)
                elif event.key == pygame.K_m:
                    grid = game_system.randomize_grid(grid, 0.3)  # 30% density
                    game_system.cell_age.clear()
                elif event.key == pygame.K_c:
                    game_system.mode = "classic"
                elif event.key == pygame.K_h:
                    game_system.mode = "heatmap"
                elif event.key == pygame.K_t:
                    game_system.mode = "trails"
            elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and event.buttons[0]):
                x, y = pygame.mouse.get_pos()
                cell_x = x // (screen.get_width() // grid.dim.width)
                cell_y = y // (screen.get_height() // grid.dim.height)
                for dx in range(-game_system.brush_size + 1, game_system.brush_size):
                    for dy in range(-game_system.brush_size + 1, game_system.brush_size):
                        new_x = (cell_x + dx) % grid.dim.width
                        new_y = (cell_y + dy) % grid.dim.height
                        if event.button == 1 or event.buttons[0]:  # Left click/drag
                            grid.cells.add((new_x, new_y))
                            game_system.cell_age[(new_x, new_y)] = 0
                        elif event.button == 3:  # Right click
                            grid.cells.discard((new_x, new_y))
                            game_system.cell_age.pop((new_x, new_y), None)
        
        screen.fill(game_system.color_scheme['background'])
        
        # Update highlight cells
        game_system.highlight_cells = set()
        if game_system.paused:
            x, y = pygame.mouse.get_pos()
            cell_x = x // (screen.get_width() // grid.dim.width)
            cell_y = y // (screen.get_height() // grid.dim.height)
            for dx in range(-game_system.brush_size + 1, game_system.brush_size):
                for dy in range(-game_system.brush_size + 1, game_system.brush_size):
                    new_x = (cell_x + dx) % grid.dim.width
                    new_y = (cell_y + dy) % grid.dim.height
                    game_system.highlight_cells.add((new_x, new_y))
        
        game_system.draw_grid(screen, grid)
        
        if not game_system.paused:
            grid = game_system.update_grid(grid)
            game_system.generation += 1
        
        # Display game information
        info_text = [
            f"FPS: {game_system.speed}",
            f"Cells: {len(grid.cells)}",
            f"Generation: {game_system.generation}",
            f"{'Paused' if game_system.paused else 'Running'}",
            f"Brush: {game_system.brush_size}x{game_system.brush_size}",
            f"Mode: {game_system.mode}"
        ]
        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 30))
        
        pygame.display.flip()
        clock.tick(game_system.speed)

if __name__ == "__main__":
    main()