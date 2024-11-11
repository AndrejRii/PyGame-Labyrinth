import heapq
import pygame
import time

from greedy_search import CELL_SIZE


def heuristic(pos, goal):
    if goal is None:
        return 0
    # heuristic function: manhattan distance to the goal
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


cell_size = 20


def astar(labyrinth, start, goal, screen):
    visited = set()  # set of visited nodes
    optimal_path = []  # list to record the optimal path without dead-ends
    full_path = []

    # priority queue (open list), storing (f, g, position, path_taken)
    # f = g + h where g is the cost from start, h is the heuristic (estimated cost to goal)
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start, [start]))  # (f, g, pos, path)

    # cost map to store the g values (cost to reach each node)
    g_costs = {start: 0}

    steps_taken = 0

    while open_list:
        _, g, current, path_taken = heapq.heappop(open_list)

        # visualize the visited nodes (like bfs and greedy search)
        y, x = current
        full_path.append(current)
        pygame.draw.circle(screen, (200, 200, 100), (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2),
                           cell_size // 4)
        pygame.display.flip()
        time.sleep(0.05)  # small delay to visualize each visit

        steps_taken += 1

        # check if the goal has been reached
        if goal and current == goal:
            optimal_path = path_taken  # record the optimal path (straight path from start to goal)
            break  # exit the loop once the goal is found

        # mark the current node as visited
        visited.add(current)

        # explore neighbors in the order (up, down, left, right)
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (current[0] + dx, current[1] + dy)
            if (0 <= new_pos[0] < len(labyrinth) and
                    0 <= new_pos[1] < len(labyrinth[0]) and
                    labyrinth[new_pos[0]][new_pos[1]] != "█" and
                    new_pos not in visited):
                new_g = g + 1  # cost to reach the neighbor (g value)
                new_h = heuristic(new_pos, goal)  # heuristic value (h)
                f = new_g + new_h  # total cost (f)
                neighbors.append((f, new_g, new_pos, path_taken + [new_pos]))

        # add neighbors to the open list, sorted by f (lowest first)
        for neighbor in neighbors:
            f, new_g, new_pos, new_path = neighbor
            if new_pos not in g_costs or new_g < g_costs[new_pos]:
                heapq.heappush(open_list, (f, new_g, new_pos, new_path))
                g_costs[new_pos] = new_g  # update the g value for the neighbor

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
