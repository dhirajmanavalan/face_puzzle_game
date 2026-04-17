import pygame
import sys
import os
from camera import capture_image
from puzzle import create_puzzle
from game import run_game

pygame.init()

# 🎯 Create screen ONCE
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AI Face Puzzle Game")

# 🎨 SAFE IMAGE LOADER
def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        print(f"⚠️ Failed to load {path}")
        return None

# Assets
bg = load_image("assets/background.png", (800, 600))
camera_icon = load_image("assets/camera_icon.png", (100, 100))

# Fonts
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 30)

# Button
BTN_X, BTN_Y = 350, 250
BTN_W, BTN_H = 100, 100


def home_screen():
    global screen

    game_played = False   # ✅ control flag

    while True:
        # 🎨 Background
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((40, 40, 40))

        # 🎮 Title
        title = font.render("Face Puzzle Game", True, (255, 255, 255))
        screen.blit(title, (200, 60))

        mx, my = pygame.mouse.get_pos()

        # 🎥 Hover effect
        if BTN_X < mx < BTN_X + BTN_W and BTN_Y < my < BTN_Y + BTN_H:
            pygame.draw.rect(screen, (0, 255, 0), (BTN_X-5, BTN_Y-5, BTN_W+10, BTN_H+10), 3)

        # 📸 Camera button
        if camera_icon:
            screen.blit(camera_icon, (BTN_X, BTN_Y))
        else:
            pygame.draw.rect(screen, (0, 150, 255), (BTN_X, BTN_Y, BTN_W, BTN_H))
            cam_text = small_font.render("CAM", True, (255, 255, 255))
            screen.blit(cam_text, (BTN_X + 20, BTN_Y + 35))

        # 📌 Instruction
        if not game_played:
            text = small_font.render("Click Camera to Start", True, (255, 255, 255))
        else:
            text = small_font.render("Game Completed! Click to Play Again", True, (0, 255, 0))

        screen.blit(text, (250, 380))

        pygame.display.update()

        # 🎯 EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_X < mx < BTN_X + BTN_W and BTN_Y < my < BTN_Y + BTN_H:

                    # 🔒 Prevent auto re-run unless user clicks again
                    print("📸 Opening Camera...")

                    capture_image()

                    if not os.path.exists("captured.jpg"):
                        print("❌ Image capture failed!")
                        continue

                    pieces = create_puzzle("captured.jpg")

                    run_game(pieces)

                    # ✅ mark completed
                    game_played = True

                    # ✅ reset screen safely
                    screen = pygame.display.set_mode((800, 600))
                    pygame.display.set_caption("AI Face Puzzle Game")


# START
home_screen()