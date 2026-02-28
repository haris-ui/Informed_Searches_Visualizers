import heapq

def h(p1, p2):
    # Manhattan distance
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def gbfs(grid_obj, start, goal):
    """
    Greedy Best-First Search
    f(n) = h(n)
    """
    rows, cols = grid_obj.rows, grid_obj.cols
    open_set = []
    heapq.heappush(open_set, (h(start, goal), start))
    
    came_from = {}
    visited = set()
    visited.add(start)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current), visited

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dr, current[1] + dc)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if neighbor not in visited and not grid_obj.is_obstacle(neighbor[0], neighbor[1]):
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (h(neighbor, goal), neighbor))

    return None, visited

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]
