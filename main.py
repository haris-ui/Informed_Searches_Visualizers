import pygame
import sys
from grid import Grid
from agent import Agent
from search import gbfs, astar

# Constants
WIDTH, HEIGHT = 900, 750
GRID_SIZE = 600
UI_HEIGHT = 150
ROWS, COLS = 20, 20
CELL_SIZE = GRID_SIZE // max(ROWS, COLS)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255) # Visited
GREEN = (0, 255, 0) # Final Path
YELLOW = (255, 255, 0) # Frontier
RED = (255, 0, 0) # Goal
BROWN = (139, 69, 19) # Obstacle
LIGHT_GRAY = (245, 245, 245)
BOLD_GREEN = (0, 200, 0) # Start
AGENT_COLOR = (0, 0, 150)

class PathfindingApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("INFORMED SEARCH VISUALIZER")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.bold_font = pygame.font.SysFont("Arial", 18, bold=True)
        
        self.rows, self.cols = ROWS, COLS
        self.grid = Grid(self.rows, self.cols)
        self.agent = Agent(self.grid.start, self.grid.goal)
        
        self.dynamic_mode = False
        self.simulation_running = False
        self.obstacle_density = 0.3
        self.spawn_prob = 0.05
        
        self.algorithm = "A*"
        self.heuristic = "Manhattan"
        
        # Search state for visualization
        self.path = []
        self.visited = set()
        self.frontier = []
        
    def draw_grid(self):
        start_x = 50
        start_y = 50
        
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(start_x + c * CELL_SIZE, start_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = WHITE
                val = self.grid.get_cell(r, c)
                
                # Base grid value
                if val == 1: color = BROWN
                elif val == 2: color = BOLD_GREEN # Start
                elif val == 3: color = RED # Goal
                
                # Overlay Search Info (if simulation is active or just finished)
                if (r, c) in self.path:
                    if (r, c) != self.grid.start and (r, c) != self.grid.goal:
                        color = GREEN
                elif (r, c) in self.frontier:
                    if (r, c) != self.grid.start and (r, c) != self.grid.goal:
                        color = YELLOW
                elif (r, c) in self.visited:
                    if (r, c) != self.grid.start and (r, c) != self.grid.goal:
                        color = BLUE
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

                # Agent is drawn separately to ensure it is always visible
                if (r, c) == self.agent.pos:
                    center = (start_x + c * CELL_SIZE + CELL_SIZE // 2, start_y + r * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.circle(self.screen, AGENT_COLOR, center, CELL_SIZE // 3)

    def draw_ui(self):
        # Dashboard on the right
        dash_x = 700
        dash_y = 50
        
        # Metrics Box
        pygame.draw.rect(self.screen, GRAY, (dash_x - 10, dash_y - 10, 190, 180))
        pygame.draw.rect(self.screen, BLACK, (dash_x - 10, dash_y - 10, 190, 180), 2)
        
        self.screen.blit(self.bold_font.render("METRICS", True, BLACK), (dash_x, dash_y))
        
        metrics = [
            f"Nodes Visited: {self.agent.metrics['nodes_visited']}",
            f"Path Cost: {self.agent.metrics['path_cost']:.1f}",
            f"Time: {self.agent.metrics['execution_time_ms']:.2f} ms"
        ]
        for i, text in enumerate(metrics):
            img = self.font.render(text, True, BLACK)
            self.screen.blit(img, (dash_x, dash_y + 35 + i * 30))

        # Config Box
        cfg_y = dash_y + 200
        pygame.draw.rect(self.screen, GRAY, (dash_x - 10, cfg_y - 10, 190, 180))
        pygame.draw.rect(self.screen, BLACK, (dash_x - 10, cfg_y - 10, 190, 180), 2)
        
        self.screen.blit(self.bold_font.render("CONFIGURATION", True, BLACK), (dash_x, cfg_y))
        
        configs = [
            f"Algo: {self.algorithm} (1:A*/2:GBFS)",
            f"Heur: {self.heuristic} (H:Man/J:Euc)",
            f"Dynamic: {'ON' if self.dynamic_mode else 'OFF'} (D)"
        ]
        for i, text in enumerate(configs):
            img = self.font.render(text, True, BLACK)
            self.screen.blit(img, (dash_x, cfg_y + 35 + i * 30))

        # Instructions Footer
        ui_y = HEIGHT - UI_HEIGHT + 30
        instructions = [
            "G: Random Maze | Space: Find & Start | R: Reset Grid",
            "Left Click: Place Wall | Right Click: Remove Wall",
            "Colors: Brown=Wall | Bold Green=Start | Red=Goal | Blue=Visited | Yellow=Frontier | Green=Path"
        ]
        for i, text in enumerate(instructions):
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
                        self.path, self.visited, self.frontier = [], set(), []
                    elif event.key == pygame.K_d:
                        self.dynamic_mode = not self.dynamic_mode
                    elif event.key == pygame.K_r:
                        self.grid = Grid(self.rows, self.cols)
                        self.agent.reset(self.grid.start)
                        self.path, self.visited, self.frontier = [], set(), []
                    elif event.key == pygame.K_1: self.algorithm = "A*"
                    elif event.key == pygame.K_2: self.algorithm = "GBFS"
                    elif event.key == pygame.K_h: self.heuristic = "Manhattan"
                    elif event.key == pygame.K_j: self.heuristic = "Euclidean"
                    elif event.key == pygame.K_SPACE:
                        search_func = astar if self.algorithm == "A*" else gbfs
                        path_info = search_func(self.grid, self.agent.pos, self.grid.goal, self.heuristic)
                        self.agent.set_path_info(path_info)
                        self.path = self.agent.path
                        self.visited = self.agent.visited
                        self.frontier = self.agent.frontier
                        if self.path:
                            self.simulation_running = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    start_x, start_y = 50, 50
                    c = (mx - start_x) // CELL_SIZE
                    r = (my - start_y) // CELL_SIZE
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        if event.button == 1: # Left click
                            self.grid.set_cell(r, c, 1)
                        elif event.button == 3: # Right click
                            self.grid.set_cell(r, c, 0)

            if self.simulation_running:
                if self.agent.move():
                    self.path = self.agent.path
                    if self.dynamic_mode:
                        if self.grid.spawn_obstacle_randomly(self.spawn_prob):
                            if self.agent.is_path_obstructed(self.grid):
                                self.agent.replan(self.grid, self.algorithm, self.heuristic)
                                self.path = self.agent.path
                                self.visited = self.agent.visited
                                self.frontier = self.agent.frontier
                    pygame.time.delay(100)
                else:
                    self.simulation_running = False
            
            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    app = PathfindingApp()
    app.run()
