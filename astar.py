import heapq
import pygame
import time
import tracemalloc


def heuristic(pos, goal):
    if goal is None:
        return 0
    # heuristic function: manhattan distance to the goal
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

pygame.init()

OFFSET_Y = 50
CELL_SIZE = 20
DELAY = 0.1
FONT2 = pygame.font.Font(None, 25)


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
        steps_taken += 1

        pygame.draw.rect(screen, (20, 20, 30), (0, 0, 1000, 50))

        mode_text = FONT2.render(f"Mode: A*", True, (200, 200, 200))
        algo_steps_text = FONT2.render(f"Algo steps: {steps_taken}", True, (200, 200, 200))
        steps_taken_text = FONT2.render(f"Steps taken: 0", True, (200, 200, 200))

        screen.blit(mode_text, (10, 15))
        screen.blit(algo_steps_text, (135, 15))
        screen.blit(steps_taken_text, (275, 15))

        pygame.draw.circle(screen, (200, 200, 100), (x * CELL_SIZE + CELL_SIZE // 2, (y * CELL_SIZE + CELL_SIZE // 2) + OFFSET_Y),
                           CELL_SIZE // 4)
        pygame.display.flip()
        time.sleep(DELAY)  # small delay to visualize each visit



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


def astar_no_visualization(labyrinth, start, goal):
    visited = set()  # set of visited nodes
    optimal_path = []  # list to record the optimal path without dead-ends
    full_path = []  # track all visited nodes
    memory_snapshots = []
    tracemalloc.start()

    # priority queue (open list), storing (f, g, position, path_taken)
    # f = g + h where g is the cost from start, h is the heuristic (estimated cost to goal)
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), 0, start, [start]))  # (f, g, pos, path)

    # cost map to store the g values (cost to reach each node)
    g_costs = {start: 0}

    steps_taken = 0

    while open_list:
        _, g, current, path_taken = heapq.heappop(open_list)

        current_memory, _ = tracemalloc.get_traced_memory()
        memory_snapshots.append(current_memory)

        # Track visited nodes and steps
        full_path.append(current)
        steps_taken += 1

        # Check if the goal has been reached
        if goal and current == goal:
            optimal_path = path_taken  # record the optimal path (straight path from start to goal)

            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            average_memory = sum(memory_snapshots) / len(memory_snapshots)

            print(f"Peak Memory Usage: {peak_memory / 1024:.2f} KB")
            print(f"Average Memory Usage: {average_memory / 1024:.2f} KB")

            break  # exit the loop once the goal is found

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
                new_g = g + 1  # cost to reach the neighbor (g value)
                new_h = heuristic(new_pos, goal)  # heuristic value (h)
                f = new_g + new_h  # total cost (f)
                neighbors.append((f, new_g, new_pos, path_taken + [new_pos]))

        # Add neighbors to the open list, sorted by f (lowest first)
        for neighbor in neighbors:
            f, new_g, new_pos, new_path = neighbor
            if new_pos not in g_costs or new_g < g_costs[new_pos]:
                heapq.heappush(open_list, (f, new_g, new_pos, new_path))
                g_costs[new_pos] = new_g  # update the g value for the neighbor

    # If the search completes and finds a solution
    if optimal_path:
        return optimal_path, steps_taken  # Return the optimal path and steps taken

    # If no path was found
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    average_memory = sum(memory_snapshots) / len(memory_snapshots)

    print(f"Peak Memory Usage: {peak_memory / 1024:.2f} KB")
    print(f"Average Memory Usage: {average_memory / 1024:.2f} KB")

    return None, steps_taken  # Indicate failure and steps taken

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
    labyrinth, start, goal = load_map("maps/Map7.txt")

    # Measure execution time
    start_time = time.perf_counter()
    optimal_path, steps_taken = astar_no_visualization(labyrinth, start, goal)
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