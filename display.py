import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import json
import config
import special_modes
import datetime

from time_manager import get_current_time
from word_mapper import map_time_to_words

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "grid_layout.json")

# Grundeinstellungen Uhr
GRID_WIDTH = config.GRID_WIDTH
GRID_HEIGHT = config.GRID_HEIGHT
FONT_SIZE = config.FONT_SIZE
BORDER = config.BORDER

# Farben
COLOR_BASE = config.COLOR_BASE
COLOR_TARGET = config.COLOR_TARGET
HEART_ACTIVE = config.HEART_ACTIVE
HEART_INACTIVE = (60, 30, 40)
BG_COLOR = config.BG_COLOR
FADE_SPEED = config.FADE_SPEED

# === Grid-Daten laden ===
with open(file_path, encoding="utf-8") as f:
    data = json.load(f)
    grid = data["grid"]
    words = data["words"]
    heart_coords = set(tuple(pos) for pos in data["pixel_arts"]["heart"])

def fade(current, target, step=FADE_SPEED):
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return current

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
    pygame.init()
    pygame.mouse.set_visible(False)

    info = pygame.display.Info()
    display_width = info.current_w
    display_height = info.current_h

    cell_size = min(
        (display_width - 2 * BORDER) // GRID_WIDTH,
        (display_height - 2 * BORDER) // GRID_HEIGHT
    )

    screen_width = GRID_WIDTH * cell_size + BORDER * 2
    screen_height = GRID_HEIGHT * cell_size + BORDER * 2
    offset_x = (display_width - screen_width) // 2
    offset_y = (display_height - screen_height) // 2


    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Mundart Wortuhr")

    font = pygame.font.SysFont("monospace", FONT_SIZE)
    clock = pygame.time.Clock()

    now = get_current_time()
    current_minute = now.minute
    active_words = map_time_to_words(now.hour, now.minute)
    active_positions = get_active_positions(active_words)

    letter_intensity = {
        (row, col): COLOR_BASE
            for row in range(GRID_HEIGHT)
            for col in range(GRID_WIDTH)
    }

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

        screen.fill(BG_COLOR)

        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                pos = (row, col)
                cur_r, cur_g, cur_b = letter_intensity[pos]

                if pos in active_positions:
                    if special_modes.HEART_MODE and pos in heart_coords:
                        target_color = HEART_ACTIVE
                    else:
                        target_color = COLOR_TARGET

                    r = fade(cur_r, target_color[0])
                    g = fade(cur_g, target_color[1])
                    b = fade(cur_b, target_color[2])
                    letter_intensity[pos] = (r, g, b)

                elif special_modes.HEART_MODE and pos in heart_coords:
                    # Kein Fade für passives Herz, direkt zeichnen
                    r, g, b = HEART_INACTIVE
                    letter_intensity[pos] = (r, g, b)

                else:
                    r = fade(cur_r, COLOR_BASE[0])
                    g = fade(cur_g, COLOR_BASE[1])
                    b = fade(cur_b, COLOR_BASE[2])
                    letter_intensity[pos] = (r, g, b)

                color = (r, g, b)
                letter = grid[row][col]
                text = font.render(letter, True, color)
                x = offset_x + BORDER + col * cell_size
                y = offset_y + BORDER + row * cell_size

                screen.blit(text, (x, y))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    start_display()
