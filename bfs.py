from collections import deque

import pygame


class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (y, x) position
        self.parent = parent  # Parent node (None for start node)

CELL_SIZE = 20


def bfs(labyrinth, start, goal, screen):
    from time import sleep
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([Node(start)])
    visited = {start}
    shortest_path = []
    steps_taken = 0

    while queue:
        current = queue.popleft()

        # Visualize the visited nodes
        y, x = current.position
        pygame.draw.circle(screen, (200, 200, 100), (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        pygame.display.flip()
        sleep(0.05)  # Small delay to visualize each visit
        steps_taken += 1

        # Check if reached the goal
        if current.position == goal:
            while current:
                shortest_path.append(current.position)
                current = current.parent

            # Change color of shortest path to bluee
            for step in shortest_path:
                y, x = step
                pygame.draw.circle(screen, (0, 0, 255), (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
            pygame.display.flip()
            print(f"Shortest path: {shortest_path[::-1]}")
            print(f"Shortest path length: {len(shortest_path)}")
            print(f"Steps taken (nodes visited): {steps_taken}")

            return shortest_path[::-1]  # Return the reversed path to start -> goal

        for new_y, new_x in directions:
            new_position = (current.position[0] + new_y, current.position[1] + new_x)

            if 0 <= new_position[0] < len(labyrinth) and 0 <= new_position[1] < len(labyrinth[0]) and labyrinth[new_position[0]][new_position[1]] != "█":
                if new_position not in visited:
                    visited.add(new_position)
                    queue.append(Node(new_position, current))

    return None