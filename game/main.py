import pygame
import time
from inst import *

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("dodge (beta)")

FONT = pygame.font.SysFont("comicsans", 21)
LARGE_FONT = pygame.font.SysFont("comicsans", 40)
STAGE_FONT = pygame.font.SysFont("comicsans", 60)
BG = pygame.image.load("background 1600x900.png")

game_play = {
    1: {
        "obstacles": [
            (OBSTACLE_X, OBSTACLE_Y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
            (OBSTACLE_X_2, OBSTACLE_Y_2, OBSTACLE_WIDTH_2, OBSTACLE_HEIGHT_2),
            (OBSTACLE_X_3, OBSTACLE_Y_3, OBSTACLE_WIDTH_3, OBSTACLE_HEIGHT_3),
            (OBSTACLE_X_4, OBSTACLE_Y_4, OBSTACLE_WIDTH_4, OBSTACLE_HEIGHT_4),
            (OBSTACLE_X_5, OBSTACLE_Y_5, OBSTACLE_WIDTH_5, OBSTACLE_HEIGHT_5),
            (OBSTACLE_X_6, OBSTACLE_Y_6, OBSTACLE_WIDTH_6, OBSTACLE_HEIGHT_6),
            (OBSTACLE_X_7, OBSTACLE_Y_7, OBSTACLE_WIDTH_7, OBSTACLE_HEIGHT_7),
            (OBSTACLE_X_8, OBSTACLE_Y_8, OBSTACLE_WIDTH_8, OBSTACLE_HEIGHT_8)
        ],
        "coins": [(COIN_X_1, COIN_Y_1), (COIN_X_2, COIN_Y_2), (COIN_X_3, COIN_Y_3)],
        "ending": (ENDING_X, ENDING_Y, ENDING_WIDTH, ENDING_HEIGHT)
    },
    2: {
        "obstacles": [
            (200, 100, 50, 50), (400, 300, 50, 50), (600, 200, 50, 50), (800, 500, 50, 50),
            (300, 600, 50, 50), (700, 700, 50, 50), (1000, 150, 50, 50), (1200, 400, 50, 50)
        ],
        "coins": [(500, 150), (900, 450), (150, 700)],
        "ending": (WIDTH - 150, HEIGHT - 150, ENDING_WIDTH, ENDING_HEIGHT)
    },
    3: {
        "obstacles": [
            (100, 200, 50, 50), (300, 400, 50, 50), (500, 100, 50, 50), (700, 600, 50, 50),
            (900, 300, 50, 50), (1100, 500, 50, 50), (1300, 200, 50, 50), (500, 750, 50, 50)
        ],
        "coins": [(400, 250), (800, 150), (1200, 650)],
        "ending": (WIDTH // 2 - 50, 50, ENDING_WIDTH, ENDING_HEIGHT)
    }
}

def draw_text_center(text, font, color, y_offset=0):

    rendered_text = font.render(text, 1, color)
    x = WIDTH // 2 - rendered_text.get_width() // 2
    y = HEIGHT // 2 - rendered_text.get_height() // 2 + y_offset
    WIN.blit(rendered_text, (x, y))

def main_menu():
    clock = pygame.time.Clock()
    while True:
        WIN.fill(BLACK)
        draw_text_center("DODGE (BETA)", LARGE_FONT, WHITE, -50)
        draw_text_center("Press SPACE to Play", FONT, WHITE, 20)
        draw_text_center("Press ESC to Quit", FONT, WHITE, 60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: return
                if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
        clock.tick(FPS)

def stage_splash(level_num):
    WIN.fill(BLACK)
    draw_text_center(f"STAGE {level_num}", STAGE_FONT, RED, 0)
    draw_text_center("Goal: Collect all 3 coins!", FONT, WHITE, 60)
    pygame.display.update()
    time.sleep(2) 

def pause_menu():
    clock = pygame.time.Clock()
    while True:
        draw_text_center("GAME PAUSED", LARGE_FONT, WHITE, -40)
        draw_text_center("Press TAB to Resume", FONT, WHITE, 10)
        draw_text_center("Press ESC to Quit", FONT, WHITE, 40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB: return
                if event.key == pygame.K_ESCAPE: pygame.quit(); quit()
        clock.tick(FPS)

def end_game_screen(message, text_color):
    clock = pygame.time.Clock()
    while True:
        WIN.fill(BLACK)
        draw_text_center(message, LARGE_FONT, text_color, -50)
        draw_text_center("Press R to Restart", FONT, WHITE, 10)
        draw_text_center("Press ESC to Quit", FONT, WHITE, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return True
                if event.key == pygame.K_ESCAPE: return False
        clock.tick(FPS)

def load_level_objects(level):
    data = game_play[level]
    
    obstacles = [pygame.Rect(*obs) for obs in data["obstacles"]]
    coins = [pygame.Rect(pos[0], pos[1], COIN_WIDTH_1, COIN_HEIGHT_1) for pos in data["coins"]]
    ending = pygame.Rect(*data["ending"])
    
    return obstacles, coins, ending

def reset_player_position(player, invincibility_duration):
    player.x, player.y = PLAYER_X, PLAYER_Y
    return invincibility_duration

def draw_game_scene(player, elapsed_time, score, level, coins_collected, show_warning, obstacles, ending, coins, player_attempts, invincible_timer):
    WIN.blit(BG, (0, 0))

    WIN.blit(FONT.render(f"Time: {round(elapsed_time)}s", 1, WHITE), (10, 10))
    WIN.blit(FONT.render(f"Attempts: {player_attempts}", 1, WHITE), (10, 40))
    WIN.blit(FONT.render(f"Score: {score}", 1, WHITE), (10, 70))
    WIN.blit(FONT.render(f"Coins: {coins_collected}/3", 1, YELLOW), (10, 100))
    
    draw_text_center(f"Stage: {level}", FONT, WHITE, -HEIGHT // 2 + 25)
    if show_warning:
        draw_text_center("COLLECT ALL COINS TO PROGRESS!", FONT, RED, -HEIGHT // 2 + 55)

    if invincible_timer > 0:
        inv_text = FONT.render(f"{player_attempts} lives remaining", 1, LIGHT_RED)
        WIN.blit(inv_text, (WIDTH - 200, 10))

    pygame.draw.rect(WIN, PLAYER_COLOR, player)
    pygame.draw.rect(WIN, ENDING_COLOR, ending)

    obs_colors = {5: OBSTACLE_COLOR_6, 6: OBSTACLE_COLOR_7, 7: OBSTACLE_COLOR_8}
    for idx, obstacle in enumerate(obstacles):
        pygame.draw.rect(WIN, obs_colors.get(idx, OBSTACLE_COLOR), obstacle)

    coin_colors = {0: COIN_COLOR_1, 1: COIN_COLOR_2}
    for idx, coin in enumerate(coins):
        if coin.x != -100:
            pygame.draw.rect(WIN, coin_colors.get(idx, COIN_COLOR_3), coin)


def main():
    main_menu()
    
    current_level = 1
    stage_splash(current_level)

    player_attempts = PLAYER_ATTEMPTS_LIMIT
    score = PLAYER_SCORE
    invincible_timer = 0
    coins_collected = 0
    show_coin_warning = False
    warning_timer = 0
    elapsed_time = 0
    
    player = pygame.Rect(PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
    obstacles, coins, ending = load_level_objects(current_level)
    
    clock = pygame.time.Clock()
    run = True
    
    while run:
        elapsed_time += 1 / FPS

        if invincible_timer > 0: invincible_timer -= 1
        if show_coin_warning:
            warning_timer -= 1
            if warning_timer <= 0: show_coin_warning = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB: pause_menu()
                if event.key == pygame.K_ESCAPE: run = False
        
        if not run: break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  player.x = max(0, player.x - PLAYER_SPEED)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: player.x = min(WIDTH - PLAYER_WIDTH, player.x + PLAYER_SPEED)
        if keys[pygame.K_w] or keys[pygame.K_UP]:    player.y = max(0, player.y - PLAYER_SPEED)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  player.y = min(HEIGHT - PLAYER_HEIGHT, player.y + PLAYER_SPEED)

        if invincible_timer == 0:
            if any(player.colliderect(obs) for obs in obstacles):
                player_attempts -= 1
                if player_attempts < 0:
                    if end_game_screen("Game Over! You ran out of attempts!", RED):
                        main()
                    run = False
                    break
                else:
                    invincible_timer = reset_player_position(player, 60)
                    continue

        for coin in coins:
            if coin.x != -100 and player.colliderect(coin):
                score += 1
                coins_collected += 1
                coin.x = -100

        if player.colliderect(ending) or elapsed_time >= 30:
            if coins_collected >= 3:
                if current_level < 3:
                    current_level += 1
                    stage_splash(current_level)
                    invincible_timer = reset_player_position(player, 30)
                    elapsed_time = 0
                    coins_collected = 0
                    obstacles, coins, ending = load_level_objects(current_level)
                else:
                    if end_game_screen("You won the whole game!", YELLOW):
                        main()
                    run = False
                    break
            else:
                show_coin_warning = True
                warning_timer = 90  

        draw_game_scene(player, elapsed_time, score, current_level, coins_collected, show_coin_warning, 
                        obstacles, ending, coins, player_attempts, invincible_timer)
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

main()
