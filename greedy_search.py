def heuristic(pos, goal):
    # Heuristic function: Manhattan distance to the goal
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def greedy_search(labyrinth, start, goal):
    visited = set()
    full_path = []  # List to record every single move for visualization
    optimal_path = []  # List to record the optimal path without dead-ends
    stack = [(heuristic(start, goal), start, [start])]  # Priority queue as (heuristic, position, path_taken)

    while stack:
        # Sort stack to always explore the lowest heuristic first
        stack.sort(reverse=True)
        _, current, path_taken = stack.pop()

        # Add the current position to the visualization path (full path)
        full_path.append(current)

        # Check if the goal has been reached
        if current == goal:
            # Record the optimal path (straight path from start to goal)
            optimal_path = path_taken
            break  # Exit the loop once the goal is found

        # Mark the current node as visited
        visited.add(current)

        # Explore neighbors in the order (up, down, left, right) sorted by heuristic
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (current[0] + dx, current[1] + dy)
            if (0 <= new_pos[0] < len(labyrinth) and
                0 <= new_pos[1] < len(labyrinth[0]) and
                labyrinth[new_pos[0]][new_pos[1]] != "█" and
                new_pos not in visited):
                neighbors.append((heuristic(new_pos, goal), new_pos, path_taken + [new_pos]))

        # If there are valid neighbors, continue exploring
        if neighbors:
            stack.extend(neighbors)
        # If no valid neighbors, just continue exploring the next available paths in the stack

    return full_path, optimal_path  # Return both the complete path and the optimal path
