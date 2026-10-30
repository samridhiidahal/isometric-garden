import pygame
import sys
import math
import random
import json
from datetime import datetime, timedelta

# --- Configuration ---
WIDTH, HEIGHT = 1000, 700
TILE_WIDTH, TILE_HEIGHT = 64, 32
GRID_WIDTH, GRID_HEIGHT = 10, 10
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 30
FPS = 60

# --- Colors ---
SKY_DAY = (135, 206, 235)
SKY_NIGHT = (10, 10, 50)
DIRT = (139, 69, 19)
BLACK = (0, 0, 0)
WATERED = (100, 60, 30)
PLANT_COLOR = (0, 200, 0)
FLOWER_COLOR = (255, 105, 180)
FRUIT_COLOR = (255, 165, 0)
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
RAIN_COLOR = (173, 216, 230)
BUTTON_COLOR = (200, 200, 200)
BUTTON_ACTIVE = (150, 200, 255)
BUTTERFLY_COLORS = [(255, 105, 180), (255, 165, 0), (138, 43, 226)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("\U0001F331 Isometric Garden Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# --- Time Setup ---
game_time = datetime(2025, 1, 1, 6, 0)
TIME_SPEED = timedelta(minutes=60)

# --- Grid Setup ---
grid = [[{"state": "empty", "watered": False, "plant_time": None, "type": None} for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# --- Rain, Bees & Butterflies ---
rain_drops = []
raining = False

class Bee:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(100, HEIGHT - 100)
        self.speed = random.uniform(1, 2)
        self.angle = random.uniform(0, math.pi * 2)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        if random.random() < 0.05:
            self.angle += random.uniform(-0.5, 0.5)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), 3)
        pygame.draw.line(surface, (0, 0, 0), (int(self.x)-2, int(self.y)), (int(self.x)+2, int(self.y)), 1)

class Butterfly:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.base_y = random.randint(100, HEIGHT - 200)
        self.y = self.base_y
        self.speed = random.uniform(0.5, 1.2)
        self.angle = random.uniform(0, 2 * math.pi)
        self.phase = random.uniform(0, 2 * math.pi)
        self.color = random.choice(BUTTERFLY_COLORS)
        self.wing_flap_speed = random.uniform(5, 10)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y = self.base_y + math.sin(pygame.time.get_ticks() / 300 + self.phase) * 12
        if self.x < 0 or self.x > WIDTH:
            self.angle = math.pi - self.angle

    def draw(self, surface):
        t = pygame.time.get_ticks() / 100
        wing_angle = math.sin(t * self.wing_flap_speed) * math.pi / 6

        # body
        center = (int(self.x), int(self.y))
        pygame.draw.line(surface, BLACK, (self.x, self.y - 3), (self.x, self.y + 3), 2)

        # wings
        size = 8
        left = (
            self.x - math.cos(wing_angle) * size,
            self.y - math.sin(wing_angle) * size
        )
        right = (
            self.x + math.cos(wing_angle) * size,
            self.y - math.sin(wing_angle) * size
        )
        pygame.draw.polygon(surface, self.color, [center, left, right])

bees = [Bee() for _ in range(6)]
butterflies = [Butterfly() for _ in range(5)]

# --- Plant Types ---
plant_types = ["crop", "flower", "fruit"]
selected_type = "crop"
buttons = []
for i, ptype in enumerate(plant_types):
    rect = pygame.Rect(10 + i * (BUTTON_WIDTH + 10), HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
    buttons.append({"type": ptype, "rect": rect})

# --- Helper Functions ---
def iso_coords(x, y):
    sx = (x - y) * TILE_WIDTH // 2 + WIDTH // 2
    sy = (x + y) * TILE_HEIGHT // 2 + 60
    return sx, sy

def draw_tile(x, y, color):
    sx, sy = iso_coords(x, y)
    points = [
        (sx, sy),
        (sx + TILE_WIDTH // 2, sy + TILE_HEIGHT // 2),
        (sx, sy + TILE_HEIGHT),
        (sx - TILE_WIDTH // 2, sy + TILE_HEIGHT // 2)
    ]
    pygame.draw.polygon(screen, color, points)

def draw_plant(surface, x, y, plant_type):
    color = {"crop": PLANT_COLOR, "flower": FLOWER_COLOR, "fruit": FRUIT_COLOR}.get(plant_type, PLANT_COLOR)
    pygame.draw.circle(surface, color, (x, y - TILE_HEIGHT // 2), 6)
    pygame.draw.line(surface, DARK_GREEN, (x, y), (x, y - 10), 2)

def draw_sky(hour):
    fade = max(0, min(1, (hour - 18) / 6 if hour > 18 else (6 - hour) / 6))
    r = SKY_DAY[0] * (1 - fade) + SKY_NIGHT[0] * fade
    g = SKY_DAY[1] * (1 - fade) + SKY_NIGHT[1] * fade
    b = SKY_DAY[2] * (1 - fade) + SKY_NIGHT[2] * fade
    screen.fill((int(r), int(g), int(b)))

def draw_rain():
    for drop in rain_drops:
        pygame.draw.line(screen, RAIN_COLOR, (drop[0], drop[1]), (drop[0], drop[1] + 5), 1)

def get_season(dt):
    m = dt.month
    return ["Winter", "Spring", "Summer", "Autumn"][(m % 12) // 3]

def save_garden():
    with open("garden_save.json", "w") as f:
        json.dump(grid, f)
    print("Garden saved.")

def load_garden():
    global grid
    try:
        with open("garden_save.json", "r") as f:
            grid = json.load(f)
        print("Garden loaded.")
    except:
        print("No save file found.")

# --- Main Loop ---
running = True
last_tick = pygame.time.get_ticks()

while running:
    now = pygame.time.get_ticks()
    if now - last_tick > 1000:
        last_tick = now
        game_time += TIME_SPEED
        if random.random() < 0.1:
            raining = True
            rain_drops = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(120)]
            for row in grid:
                for tile in row:
                    if tile["state"] == "seed":
                        tile["watered"] = True
        else:
            raining = False
            rain_drops = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for btn in buttons:
                if btn["rect"].collidepoint(mx, my):
                    selected_type = btn["type"]
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    sx, sy = iso_coords(x, y)
                    rect = pygame.Rect(sx - TILE_WIDTH // 2, sy, TILE_WIDTH, TILE_HEIGHT)
                    if rect.collidepoint(mx, my):
                        tile = grid[y][x]
                        if event.button == 1:
                            if tile["state"] == "empty":
                                tile["state"] = "seed"
                                tile["plant_time"] = datetime.now().timestamp()
                                tile["type"] = selected_type
                        elif event.button == 3:
                            if tile["state"] == "seed":
                                tile["watered"] = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_garden()
            elif event.key == pygame.K_l:
                load_garden()

    hour = game_time.hour + game_time.minute / 60
    draw_sky(hour)

    # Draw Rain
    if raining:
        draw_rain()

    # Draw Grid and Plants
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = grid[y][x]
            color = WATERED if tile["state"] == "seed" and tile["watered"] else DIRT
            if tile["state"] == "seed":
                if tile["watered"] and tile["plant_time"] and datetime.now().timestamp() - tile["plant_time"] > 5:
                    tile["state"] = "grown"
            draw_tile(x, y, color)
            sx, sy = iso_coords(x, y)
            if tile["state"] == "grown":
                draw_plant(screen, sx, sy, tile["type"])

    # Draw Bees
    for bee in bees:
        bee.update()
        bee.draw(screen)

    # Draw Butterflies
    for butterfly in butterflies:
        butterfly.update()
        butterfly.draw(screen)

    # HUD: Time & Season
    season = get_season(game_time)
    text = font.render(f"{game_time.strftime('%A %I:%M %p')} - {season}", True, WHITE)
    screen.blit(text, (10, 10))

    # GUI Buttons
    for btn in buttons:
        pygame.draw.rect(screen, BUTTON_ACTIVE if btn["type"] == selected_type else BUTTON_COLOR, btn["rect"])
        label = font.render(btn["type"].capitalize(), True, BLACK)
        screen.blit(label, (btn["rect"].x + 10, btn["rect"].y + 5))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
