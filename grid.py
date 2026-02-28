import random

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)
        self.grid[self.start[0]][self.start[1]] = 2 # Start
        self.grid[self.goal[0]][self.goal[1]] = 3 # Goal

    def set_cell(self, r, c, val):
        if (r, c) == self.start or (r, c) == self.goal:
            return
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = val

    def get_cell(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def is_obstacle(self, r, c):
        return self.get_cell(r, c) == 1

    def generate_random_maze(self, density):
        # Reset grid but keep start/goal
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) != self.start and (r, c) != self.goal:
                    if random.random() < density:
                        self.grid[r][c] = 1 # Obstacle
                    else:
                        self.grid[r][c] = 0 # Empty

    def toggle_wall(self, r, c):
        if (r, c) == self.start or (r, c) == self.goal:
            return
        if self.grid[r][c] == 1:
            self.grid[r][c] = 0
        else:
            self.grid[r][c] = 1

    def reset_path(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] in [4, 5]: # Path or Visited
                    self.grid[r][c] = 0

    def spawn_obstacle_randomly(self, prob):
        if random.random() < prob:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) != self.start and (r, c) != self.goal:
                self.grid[r][c] = 1
                return (r, c)
        return None
