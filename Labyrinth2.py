import pygame
import sys

from docutils.nodes import header
from panel.models import Player
from Algorithms_enum import Algorithms

from greedy_search import greedy_search
from astar import astar
from bfs import bfs
from dfs import dfs

# Initialize Pygame
pygame.init()

# Define colors
WALLS = (200, 200, 200)  # Light gray for walls
BACKGROUND = (20, 20, 30)  # Muted dark blue background
PLAYER = (100, 150, 255)  # Soft light blue for the player
END = (144, 238, 144)  # Soft pastel green for the goal

# Define fonts
FONT = pygame.font.Font(None, 36)
FONT2 = pygame.font.Font(None, 25)

# Map list
maps = ["Map 1", "Map 2", "Map 3", "Map 4", "Map 5", "Map 6", "Map 7"]

# Cell size in pixels
CELL_SIZE = 20

OFFSET_Y = 50
Algorithm: Algorithms | None = None


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

# Congratulations screen drawing function
def draw_congratulations(screen, steps_taken = 0):
    screen.fill(BACKGROUND)
    congrats_text = FONT.render("Congratulations, you won!", True, END)
    screen.blit(congrats_text, (screen.get_width() // 2 - congrats_text.get_width() // 2,
                                screen.get_height() // 2 - congrats_text.get_height() // 2 - 50))
    congrats_text = FONT.render(f"You took {steps_taken} steps.", True, END)
    screen.blit(congrats_text, (screen.get_width() // 2 - congrats_text.get_width() // 2,
                                screen.get_height() // 2 - congrats_text.get_height() // 2 - 20))

    instruction_text = FONT.render("Press Enter to return to menu", True, WALLS)
    screen.blit(instruction_text,
                (screen.get_width() // 2 - instruction_text.get_width() // 2, screen.get_height() // 2 + 50))

    instruction_text = FONT2.render("Press Escape to quit game", True, WALLS)
    screen.blit(instruction_text,
                (screen.get_width() // 2 - instruction_text.get_width() // 2, screen.get_height() // 2 + 80))

    pygame.display.flip()

# Menu drawing function
def draw_menu(screen):
    screen.fill(BACKGROUND)
    title_text = FONT.render("Choose a Map", True, WALLS)
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

    for i, map_name in enumerate(maps):
        map_text = FONT.render(f"{i + 1}. {map_name}", True, PLAYER)
        screen.blit(map_text, (screen.get_width() // 2 - map_text.get_width() // 2, 130 + i * 40))

    # Draw the ESC key instruction
    esc_text = FONT2.render("Press Escape key to quit game", True, WALLS)
    screen.blit(esc_text, (screen.get_width() // 2 - esc_text.get_width() // 2, 150 + len(maps) * 40 + 10))

    pygame.display.flip()

# Choose solution function
def draw_solution_menu(screen):
    screen.fill(BACKGROUND)
    solution_menu_text = FONT.render("Solve the maze yourself or use an algorithm?", True, WALLS)
    screen.blit(solution_menu_text, (screen.get_width() // 2 - solution_menu_text.get_width() // 2, 50))

    solve_yourself_text = FONT.render("1. Solve yourself", True, PLAYER)
    screen.blit(solve_yourself_text, (screen.get_width() // 2 - solve_yourself_text.get_width() // 2, 150))

    use_algorithm_text = FONT.render("2. Use algorithm", True, PLAYER)
    screen.blit(use_algorithm_text, (screen.get_width() // 2 - use_algorithm_text.get_width() // 2, 200))
    pygame.display.flip()

# Algorithm menu function
def draw_algorithm_menu(screen):
    screen.fill(BACKGROUND)
    algorithm_menu_text = FONT.render("Choose algorithm", True, WALLS)
    screen.blit(algorithm_menu_text, (screen.get_width() // 2 - algorithm_menu_text.get_width() // 2, 50))

    dfs_text = FONT.render("1. DFS", True, PLAYER)
    screen.blit(dfs_text, (screen.get_width() // 2 - dfs_text.get_width() // 2, 150))

    bfs_text = FONT.render("2. BFS", True, PLAYER)
    screen.blit(bfs_text, (screen.get_width() // 2 - bfs_text.get_width() // 2, 200))

    a_star_text = FONT.render("3. A*", True, PLAYER)
    screen.blit(a_star_text, (screen.get_width() // 2 - a_star_text.get_width() // 2, 250))

    greedy_text = FONT.render("4. Greedy Search", True, PLAYER)
    screen.blit(greedy_text, (screen.get_width() // 2 - greedy_text.get_width() // 2, 300))
    pygame.display.flip()

# Labyrinth drawing function
def draw_labyrinth(screen, labyrinth, player_pos, goal_pos, steps_taken = 0, algo_header = False, algo_steps = 0):
    screen.fill(BACKGROUND)

    if algo_header:
        mode_text = FONT2.render(f"Mode: {Algorithm.value}", True, WALLS)
        algo_steps_text = FONT2.render(f"Algo steps: {algo_steps}", True, WALLS)
        steps_taken_text = FONT2.render(f"Steps taken: {steps_taken}", True, WALLS)

        screen.blit(mode_text, (10, 15))
        screen.blit(algo_steps_text, (135, 15))
        screen.blit(steps_taken_text, (275, 15))
    else:
        header_text = f"Mode: Player   |   Steps taken: {steps_taken}"
        screen.blit(FONT2.render(header_text, True, WALLS), (10, 15))

    for y, row in enumerate(labyrinth):
        for x, cell in enumerate(row):
            draw_x = x * CELL_SIZE
            draw_y = y * CELL_SIZE + OFFSET_Y  # Apply vertical offset here

            if cell == "█":
                pygame.draw.rect(screen, WALLS, (draw_x, draw_y, CELL_SIZE, CELL_SIZE))
            elif (y, x) == goal_pos:
                pygame.draw.rect(screen, END, (draw_x, draw_y, CELL_SIZE, CELL_SIZE))
            elif (y, x) == player_pos:
                pygame.draw.circle(screen, PLAYER, (draw_x + CELL_SIZE // 2, draw_y + CELL_SIZE // 2),
                                   CELL_SIZE // 2)

    pygame.display.flip()

# Player movement function
def move_player(labyrinth, player_pos, dx, dy):
    y, x = player_pos
    new_y, new_x = y + dy, x + dx

    # Ensure new position is within bounds and not a wall
    if 0 <= new_y < len(labyrinth) and 0 <= new_x < len(labyrinth[0]) and labyrinth[new_y][new_x] != "█":
        return new_y, new_x
    return player_pos

# Player movement function with delay
def move_player_continuously(labyrinth, player_pos, dx, dy, last_move_time, move_delay):
    y, x = player_pos
    new_y, new_x = y + dy, x + dx

    # Ensure new position is within bounds and not a wall
    if 0 <= new_y < len(labyrinth) and 0 <= new_x < len(labyrinth[0]) and labyrinth[new_y][new_x] != "█":
        # If enough time has passed since last move, update the position
        if pygame.time.get_ticks() - last_move_time >= move_delay:
            return (new_y, new_x), pygame.time.get_ticks(), True
    return player_pos, last_move_time, False

def display_path(path, labyrinth, player_pos, goal_pos, screen, algo_steps = 0):
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter to make player run to goal
                    waiting_for_input = False

    if path:
        steps_taken = 0
        # Now move the player along the path
        for step in path:
            steps_taken += 1
            player_pos = step

            draw_labyrinth(screen, labyrinth, player_pos,
                           goal_pos, steps_taken, True, algo_steps)

            pygame.display.flip()
            pygame.time.delay(100)
    else:
        main()

# Main program
def main():
    global Algorithm
    # Create the screen once, before entering the menu loop
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Labyrinth Game")
    # Menu loop
    menu = True
    selected_map = None
    while menu:
        # Draw the menu
        draw_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,pygame.K_7):
                    selected_map = int(event.unicode) - 1  # Choose map index based on number key
                    menu = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Solution menu loop
    solution_menu = True
    algorithm_solution = False
    player_solution = False
    while solution_menu:
        draw_solution_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_solution = True
                    solution_menu = False
                elif event.key == pygame.K_2:
                    algorithm_solution = True
                    solution_menu = False
                elif event.key == pygame.K_ESCAPE:
                    main()

    while algorithm_solution:
        draw_algorithm_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Algorithm = Algorithms.DFS
                    algorithm_solution = False
                elif event.key == pygame.K_2:
                    Algorithm = Algorithms.BFS
                    algorithm_solution = False
                elif event.key == pygame.K_3:
                    Algorithm = Algorithms.A_star
                    algorithm_solution = False
                elif event.key == pygame.K_4:
                    Algorithm = Algorithms.Greedy
                    algorithm_solution = False
                elif event.key == pygame.K_ESCAPE:
                    main()

    # Load selected map
    labyrinth, player_pos, goal_pos = load_map(f"maps\\Map{selected_map + 1}.txt")

    # Calculate dynamic screen size based on map dimensions
    screen_width = len(labyrinth[0]) * CELL_SIZE
    screen_height = len(labyrinth) * CELL_SIZE + OFFSET_Y
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Movement delay in milliseconds (0.3 seconds)
    move_delay = 150
    last_move_time = pygame.time.get_ticks()  # Time of the last move

    steps_taken = 0
    running = True
    while running:
        if Algorithm is None:
            draw_labyrinth(screen, labyrinth, player_pos, goal_pos, steps_taken, False)
        else:
            draw_labyrinth(screen, labyrinth, player_pos, goal_pos, steps_taken, True)

        if Algorithm == Algorithms.Greedy:
            # Run Greedy and get the path
            path, steps_taken = greedy_search(labyrinth, player_pos, goal_pos, screen)
            display_path(path, labyrinth, player_pos, goal_pos, screen, steps_taken)
            player_pos = goal_pos
            algorithm_solution = False
            steps_taken = len(path)
        elif Algorithm == Algorithms.A_star:
            # Run Astar and get the path
            path, steps_taken = astar(labyrinth, player_pos, goal_pos, screen)
            display_path(path, labyrinth, player_pos, goal_pos, screen, steps_taken)
            player_pos = goal_pos
            algorithm_solution = False
            steps_taken = len(path)
        elif Algorithm == Algorithms.BFS:
            # Run BFS and get the path
            path, steps_taken = bfs(labyrinth, player_pos, goal_pos, screen)
            display_path(path, labyrinth, player_pos, goal_pos, screen, steps_taken)
            player_pos = goal_pos
            algorithm_solution = False
            steps_taken = len(path)
        elif Algorithm == Algorithms.DFS:
            # Run DFS and get the path
            path, steps_taken = dfs(labyrinth, player_pos, goal_pos, screen)
            display_path(path, labyrinth, player_pos, goal_pos, screen, steps_taken)
            player_pos = goal_pos
            algorithm_solution = False
            steps_taken = len(path)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the current key states (hold and repeat detection)
        keys = pygame.key.get_pressed()

        moved = False
        # Movement with delay
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_pos, last_move_time, moved = move_player_continuously(labyrinth, player_pos, 0, -1, last_move_time,
                                                                  move_delay)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_pos, last_move_time, moved = move_player_continuously(labyrinth, player_pos, 0, 1, last_move_time,
                                                                  move_delay)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_pos, last_move_time, moved = move_player_continuously(labyrinth, player_pos, -1, 0, last_move_time,
                                                                  move_delay)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_pos, last_move_time, moved = move_player_continuously(labyrinth, player_pos, 1, 0, last_move_time,
                                                                  move_delay)
        elif keys[pygame.K_r]:
            labyrinth, player_pos, goal_pos = load_map(f"maps\\Map{selected_map + 1}.txt")
            steps_taken = 0
        elif keys[pygame.K_ESCAPE]:
            running = False
            steps_taken = 0
            main()

        if moved:
            steps_taken += 1

        # Check if the player has reached the goal
        if player_pos == goal_pos:
            draw_congratulations(screen, steps_taken)
            waiting_for_key = True
            while waiting_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Enter key to return to menu
                            waiting_for_key = False
                            main()  # Return to menu loop
                        elif event.key == pygame.K_ESCAPE:
                            waiting_for_key = False
                            pygame.quit()
                            sys.exit()

# Run the main function
if __name__ == "__main__":
    main()
    pygame.quit()
