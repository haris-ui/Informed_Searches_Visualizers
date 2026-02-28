import pygame
import sys
from grid import Grid
from agent import Agent
from search import gbfs

# Constants
WIDTH, HEIGHT = 800, 700
GRID_SIZE = 500
UI_HEIGHT = 150
ROWS, COLS = 20, 20
CELL_SIZE = GRID_SIZE // max(ROWS, COLS)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255) # Path
GREEN = (0, 255, 0) # Start
RED = (255, 0, 0) # Goal
YELLOW = (255, 255, 0) # Agent
BROWN = (139, 69, 19) # Obstacle
LIGHT_GRAY = (245, 245, 245)

class PathfindingApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dynamic Pathfinding Agent (GBFS)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        
        self.rows, self.cols = ROWS, COLS
        self.grid = Grid(self.rows, self.cols)
        self.agent = Agent(self.grid.start, self.grid.goal)
        
        self.dynamic_mode = False
        self.simulation_running = False
        self.obstacle_density = 0.3
        self.spawn_prob = 0.05
        
        self.path = []
        self.visited = set()
        
    def draw_grid(self):
        start_x = (WIDTH - self.cols * CELL_SIZE) // 2
        start_y = 50
        
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(start_x + c * CELL_SIZE, start_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = WHITE
                val = self.grid.get_cell(r, c)
                
                if val == 1: color = BROWN
                elif val == 2: color = GREEN
                elif val == 3: color = RED
                
                if (r, c) == self.agent.pos:
                    color = YELLOW
                elif (r, c) in self.path:
                    color = BLUE
                elif (r, c) in self.visited:
                    color = GRAY
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def draw_ui(self):
        ui_y = HEIGHT - UI_HEIGHT + 20
        texts = [
            f"Grid: {self.rows}x{self.cols} | Density: {self.obstacle_density*100:.0f}%",
            f"Dynamic Mode: {'ON' if self.dynamic_mode else 'OFF'} (Press 'D')",
            f"Controls: 'G' - Generate Maze | 'Space' - Start Pathfinding | 'R' - Reset",
            f"Click on grid to toggle obstacles."
        ]
        for i, text in enumerate(texts):
            img = self.font.render(text, True, BLACK)
            self.screen.blit(img, (50, ui_y + i * 25))

    def run(self):
        while True:
            self.screen.fill(LIGHT_GRAY)
            self.draw_grid()
            self.draw_ui()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.grid.generate_random_maze(self.obstacle_density)
                        self.agent.reset(self.grid.start)
                        self.path = []
                        self.visited = set()
                    elif event.key == pygame.K_d:
                        self.dynamic_mode = not self.dynamic_mode
                    elif event.key == pygame.K_r:
                        self.grid = Grid(self.rows, self.cols)
                        self.agent.reset(self.grid.start)
                        self.path, self.visited = [], set()
                    elif event.key == pygame.K_SPACE:
                        self.path, self.visited = gbfs(self.grid, self.agent.pos, self.grid.goal)
                        if self.path:
                            self.agent.set_path(list(self.path[1:]))
                            self.simulation_running = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    start_x = (WIDTH - self.cols * CELL_SIZE) // 2
                    start_y = 50
                    c = (mx - start_x) // CELL_SIZE
                    r = (my - start_y) // CELL_SIZE
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        self.grid.toggle_wall(r, c)

            if self.simulation_running:
                if self.agent.move():
                    if self.dynamic_mode:
                        # Spawn random obstacle
                        new_obs = self.grid.spawn_obstacle_randomly(self.spawn_prob)
                        if new_obs:
                            # If new obstacle is on the path, replan
                            if self.agent.is_path_obstructed(self.grid):
                                print("Path obstructed! Replanning...")
                                self.agent.replan(self.grid)
                                self.path = self.agent.path
                    pygame.time.delay(100)
                else:
                    self.simulation_running = False
            
            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    app = PathfindingApp()
    app.run()
