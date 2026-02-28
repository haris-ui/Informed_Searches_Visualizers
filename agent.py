from search import gbfs

class Agent:
    def __init__(self, start, goal):
        self.pos = start
        self.goal = goal
        self.path = []
        self.visited = set()

    def set_path(self, path):
        self.path = path

    def move(self):
        if self.path:
            self.pos = self.path.pop(0)
            return True
        return False

    def is_path_obstructed(self, grid_obj):
        """
        Check if any cell in the remaining path becomes an obstacle.
        """
        for r, c in self.path:
            if grid_obj.get_cell(r, c) == 1:
                return True
        return False

    def replan(self, grid_obj):
        """
        Re-run GBFS from current position to goal.
        """
        self.path, self.visited = gbfs(grid_obj, self.pos, self.goal)
        if self.path:
            # The first element is current pos, pop it
            self.path.pop(0)

    def reset(self, start):
        self.pos = start
        self.path = []
        self.visited = set()
