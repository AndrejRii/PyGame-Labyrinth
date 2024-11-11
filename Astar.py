import heapq


def heuristic(pos, goal):
    # Heuristic function: Manhattan distance to the goal
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def astar(labyrinth, start, goal):
    visited = set()  # Set of visited nodes
    full_path = []  # List to record every single move for visualization
    optimal_path = []  # List to record the optimal path without dead-ends

    # Priority queue (open list), storing (f, g, position, path_taken)
    # f = g + h where g is the cost from start, h is the heuristic (estimated cost to goal)
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start, [start]))  # (f, g, pos, path)

    # Cost map to store the g values (cost to reach each node)
    g_costs = {start: 0}

    while open_list:
        _, g, current, path_taken = heapq.heappop(open_list)

        # Add the current position to the visualization path
        full_path.append(current)

        # Check if the goal has been reached
        if current == goal:
            optimal_path = path_taken  # Record the optimal path (straight path from start to goal)
            break  # Exit the loop once the goal is found

        # Mark the current node as visited
        visited.add(current)

        # Explore neighbors in the order (up, down, left, right)
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (current[0] + dx, current[1] + dy)
            if (0 <= new_pos[0] < len(labyrinth) and
                    0 <= new_pos[1] < len(labyrinth[0]) and
                    labyrinth[new_pos[0]][new_pos[1]] != "█" and
                    new_pos not in visited):
                new_g = g + 1  # Cost to reach the neighbor (g value)
                new_h = heuristic(new_pos, goal)  # Heuristic value (h)
                f = new_g + new_h  # Total cost (f)
                neighbors.append((f, new_g, new_pos, path_taken + [new_pos]))

        # Add neighbors to the open list, sorted by f (lowest first)
        for neighbor in neighbors:
            f, new_g, new_pos, new_path = neighbor
            if new_pos not in g_costs or new_g < g_costs[new_pos]:
                heapq.heappush(open_list, (f, new_g, new_pos, new_path))
                g_costs[new_pos] = new_g  # Update the g value for the neighbor

    return full_path, optimal_path  # Return both the complete path and the optimal path
