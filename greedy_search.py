import pygame
import time
import tracemalloc

def heuristic(pos, goal):
    if goal is None:
        return 0
    # Heuristic function: Manhattan distance to the goal
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

pygame.init()

CELL_SIZE = 20
OFFSET_Y = 50
DELAY = 0.1
FONT2 = pygame.font.Font(None, 25)

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
        steps_taken += 1

        pygame.draw.rect(screen, (20, 20, 30), (0, 0, 1000, 50))

        mode_text = FONT2.render(f"Mode: Greedy", True, (200, 200, 200))
        algo_steps_text = FONT2.render(f"Algo steps: {steps_taken}", True, (200, 200, 200))
        steps_taken_text = FONT2.render(f"Steps taken: 0", True, (200, 200, 200))

        screen.blit(mode_text, (10, 15))
        screen.blit(algo_steps_text, (135, 15))
        screen.blit(steps_taken_text, (275, 15))

        pygame.draw.circle(screen, (200, 200, 100), (x * CELL_SIZE + CELL_SIZE // 2, (y * CELL_SIZE + CELL_SIZE // 2) + OFFSET_Y), CELL_SIZE // 4)
        pygame.display.flip()
        time.sleep(DELAY)  # Small delay to visualize each visit


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
                                   (x * CELL_SIZE + CELL_SIZE // 2, (y * CELL_SIZE + CELL_SIZE // 2) + OFFSET_Y), CELL_SIZE // 4)
        pygame.display.flip()
        print(f"Total steps taken: {steps_taken}")
        print(f"Optimal path steps taken: {len(optimal_path)}")
        return optimal_path, steps_taken  # Return the optimal path

    if full_path:
        for step in full_path:
            y, x = step
            if screen:
                pygame.draw.circle(screen, (255, 0, 0),
                                   (x * CELL_SIZE + CELL_SIZE // 2, (y * CELL_SIZE + CELL_SIZE // 2) + OFFSET_Y), CELL_SIZE // 4)
        pygame.display.flip()
    print("No path found (goal not found or unreachable).")
    return None, None  # No path found


def greedy_search_no_visual(labyrinth, start, goal):
    visited = set()
    optimal_path = []  # List to record the optimal path without dead-ends
    stack = [(heuristic(start, goal), start, [start])]  # Priority queue as (heuristic, position, path_taken)
    memory_snapshots = []
    tracemalloc.start()

    while stack:
        # Sort stack to always explore the lowest heuristic first
        stack.sort(reverse=True)
        _, current, path_taken = stack.pop()

        current_memory, _ = tracemalloc.get_traced_memory()
        memory_snapshots.append(current_memory)

        # Check if the goal has been reached
        if goal and current == goal:
            optimal_path = path_taken  # Record the optimal path (straight path from start to goal)

            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            average_memory = sum(memory_snapshots) / len(memory_snapshots)

            print(f"Peak Memory Usage: {peak_memory / 1024:.2f} KB")
            print(f"Average Memory Usage: {average_memory / 1024:.2f} KB")

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

    # Return results
    if optimal_path:
        return optimal_path, len(visited)  # Optimal path and steps taken

    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    average_memory = sum(memory_snapshots) / len(memory_snapshots) if memory_snapshots else 0

    print(f"Peak Memory Usage: {peak_memory / 1024:.2f} KB")
    print(f"Average Memory Usage: {average_memory / 1024:.2f} KB")

    return None, None  # No path found

# Load map function
def load_map(filename):
    with open(filename, "r", encoding="utf-8") as file:
        labyrinth = []
        player_pos = None
        goal_pos = None
        for y, line in enumerate(file):
            row = []
            for x, char in enumerate(line.strip()):
                row.append(char)
                if char == "P":
                    player_pos = (y, x)
                elif char == "G":
                    goal_pos = (y, x)
            labyrinth.append(row)
        return labyrinth, player_pos, goal_pos

def main():
    # Load map from file
    labyrinth, start, goal = load_map("maps/Map5.txt")

    # Measure execution time
    start_time = time.perf_counter()
    optimal_path, steps_taken = greedy_search_no_visual(labyrinth, start, goal)
    end_time = time.perf_counter()

    # Print results
    if optimal_path:
        print(f"Solution found in {steps_taken} steps.")
        print(f"Optimal path length: {len(optimal_path)}")
        print(f"Execution time: {end_time - start_time:.4f} seconds")
    else:
        print("No solution found.")
        print(f"Execution time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
