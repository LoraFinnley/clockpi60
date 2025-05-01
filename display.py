import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import os
import json
import config
import datetime
import logging

from time_manager import get_current_time
from word_mapper import map_time_to_words

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "grid_layout.json")


# Grundeinstellungen Uhr
CELL_SIZE = config.CELL_SIZE
GRID_WIDTH = config.GRID_WIDTH
GRID_HEIGHT = config.GRID_HEIGHT
FONT_SIZE = config.FONT_SIZE
MARGIN = config.MARGIN
BORDER = config.BORDER

# Farben
COLOR_BASE = config.COLOR_BASE
COLOR_TARGET = config.COLOR_TARGET
HEART_ACTIVE = config.HEART_ACTIVE
HEART_INACTIVE = config.HEART_INACTIVE
BG_COLOR = config.BG_COLOR
FADE_SPEED = config.FADE_SPEED

# === Grid-Daten laden ===
with open(file_path, encoding="utf-8") as f:
    data = json.load(f)
    grid = data["grid"]
    words = data["words"]

def get_ascii_grid(grid, active_positions):
    lines = []
    for row in range(len(grid)):
        line = ""
        for col in range(len(grid[row])):
            char = grid[row][col]
            if (row, col) in active_positions:
                line += char.upper() + " "
            else:
                line += char.lower() + " "
        lines.append(line)
    return "\n".join(lines)

def get_active_positions(active_words):
    active_positions = set()
    for word in active_words:
        for pos in words.get(word, []):
            active_positions.add(tuple(pos))
    return active_positions

def start_display():
    
    import pygame

    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/clock_output.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="[%H:%M:%S]"
    )

    # === Pygame Setup ===
    pygame.init()
    font = pygame.font.SysFont("monospace", FONT_SIZE)
    screen_width = GRID_WIDTH * CELL_SIZE + BORDER * 2
    screen_height = GRID_HEIGHT * CELL_SIZE + BORDER * 2
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mundart Wortuhr")
    clock = pygame.time.Clock()

    now = get_current_time()
    current_minute = now.minute
    active_words = map_time_to_words(now.hour, now.minute)
    active_positions = get_active_positions(active_words)

    letter_intensity = {}
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            letter_intensity[(row, col)] = COLOR_BASE[0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = datetime.datetime.now()
        if now.minute != current_minute:
            now_rounded = get_current_time()
            active_words = map_time_to_words(now_rounded.hour, now_rounded.minute)
            active_positions = get_active_positions(active_words)
            current_minute = now.minute
            ascii = get_ascii_grid(grid, active_positions)
            text_words = " ".join(active_words)
            logging.info(f"Neue Anzeige: {text_words}\n{ascii}\n")

        screen.fill(BG_COLOR)

        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                pos = (row, col)
                target_intensity = COLOR_TARGET[0] if pos in active_positions else COLOR_BASE[0]
                current = letter_intensity[pos]

                if current < target_intensity:
                    current = min(current + FADE_SPEED, target_intensity)
                elif current > target_intensity:
                    current = max(current - FADE_SPEED, target_intensity)

                letter_intensity[pos] = current

                try:
                    letter = grid[row][col]
                except IndexError:
                    continue

                color = (current, current, current)
                text = font.render(letter, True, color)
                x = BORDER + col * CELL_SIZE
                y = BORDER + row * CELL_SIZE
                screen.blit(text, (x, y))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def activate_heart_mode():
    global heart_mode_active, heart_mode_end_time
    heart_mode_active = True
    heart_mode_end_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    print("[DISPLAY] Herz-Modus aktiviert für 1 Stunde.")


if __name__ == "__main__":
    start_display()