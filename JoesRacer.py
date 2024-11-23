import pygame
import random
import sys
import os
import time

# Set the working directory to the location of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Current working directory: {os.getcwd()}")

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CAR_WIDTH = 50
CAR_HEIGHT = 100
TRACK_WIDTH = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Multiplayer Racing Game")

# Load assets
try:
    player1_car = pygame.image.load("player1_car.png")
    player1_car = pygame.transform.scale(player1_car, (CAR_WIDTH, CAR_HEIGHT))
    print("Loaded player1_car.png successfully.")
except (pygame.error, FileNotFoundError) as e:
    print(f"Error loading player1_car.png: {e}")
    player1_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
    player1_car.fill(RED)

try:
    player2_car = pygame.image.load("player2_car.png")
    player2_car = pygame.transform.scale(player2_car, (CAR_WIDTH, CAR_HEIGHT))
    print("Loaded player2_car.png successfully.")
except (pygame.error, FileNotFoundError) as e:
    print(f"Error loading player2_car.png: {e}")
    player2_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
    player2_car.fill(GREEN)

try:
    obstacle_texture = pygame.image.load("obstacle.png")
    obstacle_texture = pygame.transform.scale(obstacle_texture, (CAR_WIDTH, CAR_HEIGHT))
    print("Loaded obstacle.png successfully.")
except (pygame.error, FileNotFoundError) as e:
    print(f"Error loading obstacle.png: {e}")
    obstacle_texture = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
    obstacle_texture.fill(BLACK)

try:
    death_image = pygame.image.load("death.png")  # Image for death animation
    death_image = pygame.transform.scale(death_image, (CAR_WIDTH, CAR_HEIGHT))
    print("Loaded death.png successfully.")
except (pygame.error, FileNotFoundError) as e:
    print(f"Error loading death.png: {e}")
    death_image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
    death_image.fill(GRAY)

try:
    heart_image = pygame.image.load("heart.png")  # Image for health
    heart_image = pygame.transform.scale(heart_image, (70, 70))
    print("Loaded heart.png successfully.")
except (pygame.error, FileNotFoundError) as e:
    print(f"Error loading heart.png: {e}")
    heart_image = pygame.Surface((70, 70))
    heart_image.fill(RED)

# Car positions
player1_x = SCREEN_WIDTH // 2 - TRACK_WIDTH // 4 - CAR_WIDTH // 2
player1_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
player2_x = SCREEN_WIDTH // 2 + TRACK_WIDTH // 4 - CAR_WIDTH // 2
player2_y = SCREEN_HEIGHT - CAR_HEIGHT - 20

# Speeds
player_speed = 5
obstacle_speed = 7
health_pack_speed = 5
moving_obstacle_speed = 5

# Obstacles
obstacles = []
moving_obstacles = []
health_packs = []

# Health
player1_health = 3
player2_health = 3

# Ready Status
player1_ready = False
player2_ready = False

# Clock
clock = pygame.time.Clock()

def draw_track():
    # Draw road texture
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - TRACK_WIDTH // 2, 0, TRACK_WIDTH, SCREEN_HEIGHT))
    # Draw lane markers
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - 5, y, 10, 20))

def draw_obstacles():
    for obstacle in obstacles:
        screen.blit(obstacle_texture, (obstacle.x, obstacle.y))
    for moving_obstacle in moving_obstacles:
        screen.blit(obstacle_texture, (moving_obstacle["rect"].x, moving_obstacle["rect"].y))

def draw_health_packs():
    for health_pack in health_packs:
        screen.blit(heart_image, (health_pack.x, health_pack.y))

def draw_health():
    # Draw health as hearts
    for i in range(player1_health):
        screen.blit(heart_image, (20 + i * 80, 100))
    for i in range(player2_health):
        screen.blit(heart_image, (SCREEN_WIDTH - 240 + i * 80, 100))

def draw_ready_status():
    # Draw ready status
    font = pygame.font.Font(None, 48)
    player1_ready_text = font.render("Player 1 Ready: Press R", True, GREEN if player1_ready else RED)
    player2_ready_text = font.render("Player 2 Ready: Press P", True, GREEN if player2_ready else RED)
    screen.blit(player1_ready_text, (20, SCREEN_HEIGHT // 2 - 50))
    screen.blit(player2_ready_text, (SCREEN_WIDTH - 450, SCREEN_HEIGHT // 2 - 50))

def death_animation(player_x, player_y):
    # Display death animation
    for _ in range(10):
        screen.fill(GRAY)
        draw_track()
        draw_obstacles()
        screen.blit(death_image, (player_x, player_y))
        pygame.display.flip()
        time.sleep(0.1)

def game_over(winner):
    # Display game over overlay
    font = pygame.font.Font(None, 74)
    overlay_text = f"Game Over. {winner} wins! Play again? (Y/N)"
    text_surface = font.render(overlay_text, True, RED)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # Wait for player response
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting = False
                    main()
                elif event.key == pygame.K_n:
                    waiting = False
                    pygame.quit()
                    sys.exit()

def countdown():
    font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        screen.fill(GRAY)
        draw_track()
        text_surface = font.render(str(i), True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        time.sleep(1)

def wait_for_ready():
    global player1_ready, player2_ready
    waiting = True
    while waiting:
        screen.fill(GRAY)
        draw_ready_status()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player1_ready = True
                if event.key == pygame.K_p:
                    player2_ready = True

        if player1_ready and player2_ready:
            waiting = False

def main():
    global player1_y, player2_y, player1_x, player2_x, player1_health, player2_health, player1_ready, player2_ready
    player1_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
    player2_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
    player1_x = SCREEN_WIDTH // 2 - TRACK_WIDTH // 4 - CAR_WIDTH // 2
    player2_x = SCREEN_WIDTH // 2 + TRACK_WIDTH // 4 - CAR_WIDTH // 2
    obstacles.clear()
    moving_obstacles.clear()
    health_packs.clear()
    player1_health = 3
    player2_health = 3
    player1_ready = False
    player2_ready = False

    # Wait for both players to be ready
    wait_for_ready()

    # Countdown before start
    countdown()

    running = True

    # Game loop
    while running:
        screen.fill(GRAY)
        draw_track()
        draw_health()
        draw_obstacles()
        draw_health_packs()

        # Draw player cars
        screen.blit(player1_car, (player1_x, player1_y))
        screen.blit(player2_car, (player2_x, player2_y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1_y > 0:
            player1_y -= player_speed
        if keys[pygame.K_s] and player1_y < SCREEN_HEIGHT - CAR_HEIGHT:
            player1_y += player_speed
        if keys[pygame.K_a] and player1_x > SCREEN_WIDTH // 2 - TRACK_WIDTH // 2:
            player1_x -= player_speed
        if keys[pygame.K_d] and player1_x < SCREEN_WIDTH // 2 - TRACK_WIDTH // 2 + TRACK_WIDTH - CAR_WIDTH:
            player1_x += player_speed
        if keys[pygame.K_UP] and player2_y > 0:
            player2_y -= player_speed
        if keys[pygame.K_DOWN] and player2_y < SCREEN_HEIGHT - CAR_HEIGHT:
            player2_y += player_speed
        if keys[pygame.K_LEFT] and player2_x > SCREEN_WIDTH // 2 - TRACK_WIDTH // 2:
            player2_x -= player_speed
        if keys[pygame.K_RIGHT] and player2_x < SCREEN_WIDTH // 2 - TRACK_WIDTH // 2 + TRACK_WIDTH - CAR_WIDTH:
            player2_x += player_speed

        # Player collision
        player1_rect = pygame.Rect(player1_x, player1_y, CAR_WIDTH, CAR_HEIGHT)
        player2_rect = pygame.Rect(player2_x, player2_y, CAR_WIDTH, CAR_HEIGHT)
        if player1_rect.colliderect(player2_rect):
            if keys[pygame.K_d]:
                player1_x -= player_speed
            if keys[pygame.K_a]:
                player1_x += player_speed
            if keys[pygame.K_RIGHT]:
                player2_x -= player_speed
            if keys[pygame.K_LEFT]:
                player2_x += player_speed

        # Obstacle movement
        for obstacle in obstacles.copy():
            obstacle.y += obstacle_speed
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)

        # Health pack movement
        for health_pack in health_packs.copy():
            health_pack.y += health_pack_speed
            if health_pack.y > SCREEN_HEIGHT:
                health_packs.remove(health_pack)

        # Moving obstacle movement
        for moving_obstacle in moving_obstacles.copy():
            moving_obstacle["rect"].x += moving_obstacle["speed_x"]
            moving_obstacle["rect"].y += moving_obstacle["speed_y"]

            if moving_obstacle["rect"].x <= SCREEN_WIDTH // 2 - TRACK_WIDTH // 2 or moving_obstacle["rect"].x >= SCREEN_WIDTH // 2 + TRACK_WIDTH // 2 - CAR_WIDTH:
                moving_obstacle["speed_x"] = -moving_obstacle["speed_x"]
            if moving_obstacle["rect"].y > SCREEN_HEIGHT:
                moving_obstacles.remove(moving_obstacle)

        # Collision detection with obstacles
        for obstacle in obstacles.copy():
            if player1_rect.colliderect(obstacle):
                player1_health -= 1
                obstacles.remove(obstacle)
                if player1_health == 0:
                    death_animation(player1_x, player1_y)
                    game_over("Player 2")
            if player2_rect.colliderect(obstacle):
                player2_health -= 1
                obstacles.remove(obstacle)
                if player2_health == 0:
                    death_animation(player2_x, player2_y)
                    game_over("Player 1")

        # Collision detection with health packs
        for health_pack in health_packs.copy():
            if player1_rect.colliderect(health_pack):
                player1_health = min(player1_health + 1, 3)
                health_packs.remove(health_pack)
            if player2_rect.colliderect(health_pack):
                player2_health = min(player2_health + 1, 3)
                health_packs.remove(health_pack)

        # Spawn obstacles
        if random.randint(0, 100) < 5:
            new_obstacle = pygame.Rect(random.randint(SCREEN_WIDTH // 2 - TRACK_WIDTH // 2, SCREEN_WIDTH // 2 + TRACK_WIDTH // 2 - CAR_WIDTH), -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT)
            obstacles.append(new_obstacle)

        # Spawn health packs
        if random.randint(0, 1000) < 3:
            new_health_pack = pygame.Rect(random.randint(SCREEN_WIDTH // 2 - TRACK_WIDTH // 2, SCREEN_WIDTH // 2 + TRACK_WIDTH // 2 - 70), -70, 70, 70)
            health_packs.append(new_health_pack)

        # Spawn moving obstacles
        if random.randint(0, 1000) < 2:
            new_moving_obstacle = {
                "rect": pygame.Rect(random.randint(SCREEN_WIDTH // 2 - TRACK_WIDTH // 2, SCREEN_WIDTH // 2 + TRACK_WIDTH // 2 - CAR_WIDTH), -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT),
                "speed_x": random.choice([-moving_obstacle_speed, moving_obstacle_speed]),
                "speed_y": obstacle_speed
            }
            moving_obstacles.append(new_moving_obstacle)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
