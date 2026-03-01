import heapq
import time
import math

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_heuristic(name):
    if name == "Manhattan":
        return manhattan_distance
    return euclidean_distance

def gbfs(grid_obj, start, goal, heuristic_name="Manhattan"):
    """
    Greedy Best-First Search
    f(n) = h(n)
    """
    h_func = get_heuristic(heuristic_name)
    rows, cols = grid_obj.rows, grid_obj.cols
    start_time = time.perf_counter()
    
    open_set = []
    heapq.heappush(open_set, (h_func(start, goal), start))
    
    came_from = {}
    visited = set()
    nodes_visited = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
        
        nodes_visited += 1
        visited.add(current)

        if current == goal:
            end_time = time.perf_counter()
            path = reconstruct_path(came_from, current)
            return {
                "path": path,
                "visited": visited,
                "frontier": [item[1] for item in open_set],
                "nodes_visited": nodes_visited,
                "path_cost": len(path) - 1,
                "execution_time_ms": (end_time - start_time) * 1000
            }

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dr, current[1] + dc)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if neighbor not in visited and not grid_obj.is_obstacle(neighbor[0], neighbor[1]):
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (h_func(neighbor, goal), neighbor))

    end_time = time.perf_counter()
    return {
        "path": None,
        "visited": visited,
        "frontier": [item[1] for item in open_set],
        "nodes_visited": nodes_visited,
        "path_cost": 0,
        "execution_time_ms": (end_time - start_time) * 1000
    }

def astar(grid_obj, start, goal, heuristic_name="Manhattan"):
    """
    A* Search
    f(n) = g(n) + h(n)
    """
    h_func = get_heuristic(heuristic_name)
    rows, cols = grid_obj.rows, grid_obj.cols
    start_time = time.perf_counter()
    
    open_set = []
    # (f_score, pos)
    heapq.heappush(open_set, (h_func(start, goal), start))
    
    came_from = {}
    g_score = {start: 0}
    visited = set()
    nodes_visited = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
            
        nodes_visited += 1
        visited.add(current)

        if current == goal:
            end_time = time.perf_counter()
            path = reconstruct_path(came_from, current)
            return {
                "path": path,
                "visited": visited,
                "frontier": [item[1] for item in open_set],
                "nodes_visited": nodes_visited,
                "path_cost": g_score[goal],
                "execution_time_ms": (end_time - start_time) * 1000
            }

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dr, current[1] + dc)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if not grid_obj.is_obstacle(neighbor[0], neighbor[1]):
                    tentative_g_score = g_score[current] + 1
                    
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + h_func(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))

    end_time = time.perf_counter()
    return {
        "path": None,
        "visited": visited,
        "frontier": [item[1] for item in open_set],
        "nodes_visited": nodes_visited,
        "path_cost": 0,
        "execution_time_ms": (end_time - start_time) * 1000
    }

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]
