import os
import keyboard
import time


def load_map(filename):
    labyrinth = []
    player_pos = None
    goal_pos = None
    with open(filename, 'r', encoding='utf-8') as file:
        for y, line in enumerate(file):
            row = list(line.rstrip())
            labyrinth.append(row)
            if 'P' in row:
                player_pos = (y, row.index('P'))
                row[row.index('P')] = ' '  # Remove 'P' from map, we'll handle it dynamically
            if 'G' in row:
                goal_pos = (y, row.index('G'))
    return labyrinth, player_pos, goal_pos


def clear_screen():
    # For Windows, use 'cls', for other OSes use 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')


def display_map(labyrinth, player_pos):
    clear_screen()
    for y, row in enumerate(labyrinth):
        if y == player_pos[0]:
            # Insert player symbol at the player’s position in the row being displayed
            print("".join(row[:player_pos[1]]) + '@' + "".join(row[player_pos[1] + 1:]))
        else:
            print("".join(row))


def move_player(labyrinth, player_pos, direction):
    y, x = player_pos
    if direction == 'up' and labyrinth[y - 1][x] in [' ', 'G']:
        return y - 1, x
    elif direction == 'down' and labyrinth[y + 1][x] in [' ', 'G']:
        return y + 1, x
    elif direction == 'left' and labyrinth[y][x - 1] in [' ', 'G']:
        return y, x - 1
    elif direction == 'right' and labyrinth[y][x + 1] in [' ', 'G']:
        return y, x + 1
    return player_pos


def main():
    filename = 'maps/Map4.txt'
    labyrinth, player_pos, goal_pos = load_map(filename)

    if player_pos is None or goal_pos is None:
        print("Map must contain both a player (P) and a goal (G) position.")
        return

    display_map(labyrinth, player_pos)  # Display initial map with player symbol

    while True:
        if player_pos == goal_pos:
            print("\nCongratulations! You've reached the goal!")
            break

        # Wait for user input
        event = keyboard.read_event()
        if event.event_type == 'down':
            if event.name == 'w' or event.name == 'up':
                move = 'up'
            elif event.name == 's' or event.name == 'down':
                move = 'down'
            elif event.name == 'a' or event.name == 'left':
                move = 'left'
            elif event.name == 'd' or event.name == 'right':
                move = 'right'
            elif event.name == 'r':
                print("Restarting the game...")
                main()  # Restart the game
                return
            else:
                move = None

            if move:
                new_pos = move_player(labyrinth, player_pos, move)
                if new_pos != player_pos:  # Only update if the player actually moves
                    player_pos = new_pos
                    display_map(labyrinth, player_pos)  # Refresh map only when player moves

            time.sleep(0.1)


if __name__ == "__main__":
    main()
