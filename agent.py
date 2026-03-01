from search import gbfs, astar

class Agent:
    def __init__(self, start, goal):
        self.pos = start
        self.goal = goal
        self.path = []
        self.visited = set()
        self.frontier = []
        self.metrics = {
            "nodes_visited": 0,
            "path_cost": 0,
            "execution_time_ms": 0
        }

    def set_path_info(self, path_info):
        """
        Expects path_info dict from search functions.
        """
        self.path = list(path_info["path"]) if path_info["path"] else []
        self.visited = path_info["visited"]
        self.frontier = path_info["frontier"]
        self.metrics = {
            "nodes_visited": path_info["nodes_visited"],
            "path_cost": path_info["path_cost"],
            "execution_time_ms": path_info["execution_time_ms"]
        }
        # If the first element is current pos, pop it
        if self.path and self.path[0] == self.pos:
            self.path.pop(0)

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

    def replan(self, grid_obj, algorithm="A*", heuristic="Manhattan"):
        """
        Re-run search from current position to goal.
        """
        search_func = astar if algorithm == "A*" else gbfs
        path_info = search_func(grid_obj, self.pos, self.goal, heuristic)
        self.set_path_info(path_info)

    def reset(self, start):
        self.pos = start
        self.path = []
        self.visited = set()
        self.frontier = []
        self.metrics = {
            "nodes_visited": 0,
            "path_cost": 0,
            "execution_time_ms": 0
        }
