from collections import deque

import pygame
from time import sleep
import time
import tracemalloc

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (y, x) position
        self.parent = parent  # Parent node (None for start node)

pygame.init()

OFFSET_Y = 50
CELL_SIZE = 20
DELAY = 0.1
FONT2 = pygame.font.Font(None, 25)

def bfs(labyrinth, start, goal, screen):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([Node(start)])
    visited = {start}
    shortest_path = []
    full_path = []
    steps_taken = 0

    while queue:
        current = queue.popleft()

        # Visualize the visited nodes
        y, x = current.position
        full_path.append(current.position)
        steps_taken += 1

        pygame.draw.rect(screen, (20, 20, 30), (0, 0, 1000, 50))

        mode_text = FONT2.render(f"Mode: BFS", True, (200, 200, 200))
        algo_steps_text = FONT2.render(f"Algo steps: {steps_taken}", True, (200, 200, 200))
        steps_taken_text = FONT2.render(f"Steps taken: 0", True, (200, 200, 200))

        screen.blit(mode_text, (10, 15))
        screen.blit(algo_steps_text, (135, 15))
        screen.blit(steps_taken_text, (275, 15))

        pygame.draw.circle(screen, (200, 200, 100), (x * CELL_SIZE + CELL_SIZE // 2, (y * CELL_SIZE + CELL_SIZE // 2) + OFFSET_Y), CELL_SIZE // 4)
        pygame.display.flip()
        sleep(DELAY)  # Small delay to visualize each visit

        # Check if reached the goal
        if goal and current.position == goal:
            while current:
                shortest_path.append(current.position)
                current = current.parent

            # Change color of shortest path to blue
            for step in shortest_path:
                y, x = step
                pygame.draw.circle(screen, (0, 0, 255), (x * CELL_SIZE + CELL_SIZE // 2, (y * CELL_SIZE + CELL_SIZE // 2) + OFFSET_Y), CELL_SIZE // 4)
            pygame.display.flip()
            print(f"Shortest path: {shortest_path[::-1]}")
            print(f"Shortest path length: {len(shortest_path)}")
            print(f"Steps taken (nodes visited): {steps_taken}")

            return shortest_path[::-1], steps_taken  # Return the reversed path to start -> goal

        for new_y, new_x in directions:
            new_position = (current.position[0] + new_y, current.position[1] + new_x)

            if 0 <= new_position[0] < len(labyrinth) and 0 <= new_position[1] < len(labyrinth[0]) and labyrinth[new_position[0]][new_position[1]] != "█":
                if new_position not in visited:
                    visited.add(new_position)
                    queue.append(Node(new_position, current))

    if full_path:
        for step in full_path:
            y, x = step
            if screen:
                pygame.draw.circle(screen, (255, 0, 0),
                                   (x * CELL_SIZE + CELL_SIZE // 2, (y * CELL_SIZE + CELL_SIZE // 2) + OFFSET_Y), CELL_SIZE // 4)
        pygame.display.flip()
    print("No path found (goal not found or unreachable).")
    return None, None  # No path found


def bfs_no_visual(labyrinth, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([Node(start)])
    visited = {start}
    shortest_path = []
    full_path = []
    steps_taken = 0
    memory_snapshots = []
    tracemalloc.start()

    while queue:
        current = queue.popleft()

        y, x = current.position
        full_path.append(current.position)
        steps_taken += 1

        current_memory, _ = tracemalloc.get_traced_memory()
        memory_snapshots.append(current_memory)

        # Check if reached the goal
        if goal and current.position == goal:
            while current:
                shortest_path.append(current.position)
                current = current.parent
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            average_memory = sum(memory_snapshots) / len(memory_snapshots)

            print(f"Peak Memory Usage: {peak_memory / 1024:.2f} KB")
            print(f"Average Memory Usage: {average_memory / 1024:.2f} KB")
            return shortest_path[::-1], steps_taken

        for new_y, new_x in directions:
            new_position = (current.position[0] + new_y, current.position[1] + new_x)

            if 0 <= new_position[0] < len(labyrinth) and 0 <= new_position[1] < len(labyrinth[0]) and labyrinth[new_position[0]][new_position[1]] != "█":
                if new_position not in visited:
                    visited.add(new_position)
                    queue.append(Node(new_position, current))

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
    labyrinth, start, goal = load_map("maps/Map4.txt")

    # Measure execution time
    start_time = time.perf_counter()
    optimal_path, steps_taken = bfs_no_visual(labyrinth, start, goal)
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