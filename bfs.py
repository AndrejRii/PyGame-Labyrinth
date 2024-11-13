from collections import deque

import pygame
from time import sleep


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