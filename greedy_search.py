import pygame
import time

def heuristic(pos, goal):
    if goal is None:
        return 0
    # Heuristic function: Manhattan distance to the goal
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

CELL_SIZE = 20

def greedy_search(labyrinth, start, goal, screen):
    visited = set()
    optimal_path = []  # List to record the optimal path without dead-ends
    full_path = []
    stack = [(heuristic(start, goal), start, [start])]  # Priority queue as (heuristic, position, path_taken)
    steps_taken = 0

    while stack:
        # Sort stack to always explore the lowest heuristic first
        stack.sort(reverse=True)
        _, current, path_taken = stack.pop()

        # Visualize the visited nodes (like BFS)
        y, x = current
        full_path.append(current)
        pygame.draw.circle(screen, (200, 200, 100), (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        pygame.display.flip()
        time.sleep(0.05)  # Small delay to visualize each visit
        steps_taken += 1

        # Check if the goal has been reached
        if goal and current == goal:
            optimal_path = path_taken  # Record the optimal path (straight path from start to goal)
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

    # after the search, visualize the optimal path (in blue like bfs)
    if optimal_path:
        for step in optimal_path:
            y, x = step
            if screen:
                pygame.draw.circle(screen, (0, 0, 255),
                                   (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        pygame.display.flip()
        print(f"Total steps taken: {steps_taken}")
        print(f"Optimal path steps taken: {len(optimal_path)}")
        return optimal_path  # Return the optimal path

    if full_path:
        for step in full_path:
            y, x = step
            if screen:
                pygame.draw.circle(screen, (255, 0, 0),
                                   (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        pygame.display.flip()
    print("No path found (goal not found or unreachable).")
    return None  # No path found
