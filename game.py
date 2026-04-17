import pygame
import random
import time
from leaderboard import get_leaderboard

# ✅ UI CONSTANTS
BG_COLOR = (30, 30, 30)
TILE_BORDER = (255, 255, 255)
SELECT_BORDER = (255, 0, 0)

TILE_SIZE = 200
OFFSET_X = 50
OFFSET_Y = 100
GRID_SIZE = 3


# ❓ HELP → SHOW REFERENCE IMAGE
def show_reference(screen):
    try:
        img = pygame.image.load("captured.jpg").convert()
        img = pygame.transform.scale(img, (400, 400))
    except:
        print("❌ Reference image not found")
        return

    font = pygame.font.Font(None, 40)

    running = True
    while running:
        screen.fill((0, 0, 0))

        text = font.render("Reference Image (Press ESC)", True, (255, 255, 255))
        screen.blit(text, (120, 50))
        screen.blit(img, (150, 150))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# 🏆 LEADERBOARD
def show_leaderboard(screen):
    title_font = pygame.font.Font(None, 60)
    font = pygame.font.Font(None, 40)

    data = get_leaderboard()

    running = True
    while running:
        screen.fill((20, 20, 20))

        title = title_font.render("🏆 Leaderboard", True, (255, 255, 255))
        screen.blit(title, (200, 50))

        if data:
            for i, row in enumerate(data):
                text = font.render(
                    f"{i+1}. {row[0]} - {int(row[1])}s",
                    True,
                    (0, 255, 0)
                )
                screen.blit(text, (200, 150 + i * 60))
        else:
            no_data = font.render("No players yet!", True, (255, 100, 100))
            screen.blit(no_data, (230, 250))

        exit_text = font.render("Press ESC to Exit", True, (200, 200, 200))
        screen.blit(exit_text, (220, 600))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# 🎮 MAIN GAME
def run_game(pieces):
    screen = pygame.display.set_mode((700, 750))
    pygame.display.set_caption("Face Puzzle Game")

    font = pygame.font.Font(None, 36)

    # ✅ Load tiles safely
    tiles = []
    for p in pieces:
        try:
            img = pygame.image.load(p["image"]).convert()
        except:
            img = pygame.Surface((TILE_SIZE, TILE_SIZE))
            img.fill((100, 100, 100))

        tiles.append({
            "img": img,
            "correct_pos": p["correct_pos"]
        })

    random.shuffle(tiles)

    selected = []
    moves = 0
    start_time = time.time()

    running = True
    solved = False

    while running:
        screen.fill(BG_COLOR)

        # 🎮 DRAW PUZZLE
        for i, tile in enumerate(tiles):
            x = (i % GRID_SIZE) * TILE_SIZE + OFFSET_X
            y = (i // GRID_SIZE) * TILE_SIZE + OFFSET_Y

            screen.blit(tile["img"], (x, y))
            pygame.draw.rect(screen, TILE_BORDER, (x, y, TILE_SIZE, TILE_SIZE), 2)

            if i in selected:
                pygame.draw.rect(screen, SELECT_BORDER, (x, y, TILE_SIZE, TILE_SIZE), 4)

        # ⏱️ TIMER + MOVES
        elapsed_time = int(time.time() - start_time)

        screen.blit(font.render(f"Moves: {moves}", True, (0, 255, 255)), (20, 20))
        screen.blit(font.render(f"Time: {elapsed_time}s", True, (255, 255, 0)), (20, 60))

        # ❓ HELP BUTTON
        pygame.draw.rect(screen, (255, 140, 0), (550, 20, 100, 40))
        screen.blit(font.render("HELP", True, (0, 0, 0)), (560, 25))

        pygame.display.update()

        # 🎯 EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not solved:
                mx, my = pygame.mouse.get_pos()

                # ❓ HELP
                if 550 <= mx <= 650 and 20 <= my <= 60:
                    show_reference(screen)
                    continue

                # 🎮 GRID CLICK
                if OFFSET_X <= mx <= OFFSET_X + TILE_SIZE * GRID_SIZE and \
                   OFFSET_Y <= my <= OFFSET_Y + TILE_SIZE * GRID_SIZE:

                    col = (mx - OFFSET_X) // TILE_SIZE
                    row = (my - OFFSET_Y) // TILE_SIZE
                    index = int(row * GRID_SIZE + col)

                    if index < len(tiles):
                        selected.append(index)

                # 🔄 SWAP
                if len(selected) == 2:
                    i1, i2 = selected
                    tiles[i1], tiles[i2] = tiles[i2], tiles[i1]

                    moves += 1
                    selected = []

                    solved = all(tile["correct_pos"] == i for i, tile in enumerate(tiles))

        # 🏆 SUCCESS
        if solved:
            screen.blit(font.render("🎉 SOLVED!", True, (0, 255, 0)), (250, 350))
            pygame.display.update()

            pygame.time.delay(1500)
            show_leaderboard(screen)
            return