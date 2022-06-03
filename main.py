import pygame
import random
import math
from pygame import mixer
import time


# Initiallizing pygame:
pygame.init()

# Width and Height of screen:
screen = pygame.display.set_mode((1080, 720))

# Icon of the window
icon = pygame.image.load("ufo.png")

# Background of the window
background = pygame.image.load("background.jpeg")

# Background Music:
mixer.music.load("backgroundMusic.mp3")
mixer.music.play(-1)

# Setting background, title and icon of the window:
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)

# Score:
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_X = 10
text_Y = 10


def show_score(x, y):
    global score_value
    score = font.render("Score: "+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

    # Player:
player_image = pygame.image.load("player.png")
player_X = 480
player_Y = 600

# Enemy:
enemy_image = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []

no_of_enemies = 8
for i in range(no_of_enemies):
    enemy_image.append(pygame.image.load("enemy.png"))
    enemy_X.append(random.randint(0, 980))
    enemy_Y.append(random.randint(0, 200))
    enemyX_change.append(0.5)
    enemyY_change.append(0.5)

# Bullet:
bullet_image = pygame.image.load("bullet.png")
bullet_Y = 550
bullet_X = 0
bulletY_change = 3
bullet_state = "ready"

# Creating a function to draw the characters on the screen:


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x+45, y+50))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    if distance < 20:
        return True


display = True
game_over = False
font_over = ""
text_over = ""

start_ticks = pygame.time.get_ticks()  # starter tick


def game():
    global screen, icon, background, score_value, font, text_X, text_Y, high_score_file, high_score, high_score_X, player_image, playerX_change, player_X, player_Y, enemy_image, enemy_X, enemy_Y, enemyX_change, enemyY_change, no_of_enemies, bullet_image, bullet_Y, bullet_X, bulletY_change, bullet_state, display, game_over, text_over, font_over, start_ticks

    mixer.music.play(-1, fade_ms=5000)

    while display:

        screen.blit(background, (0, 0))
        playerX_change = 0
        keys = pygame.key.get_pressed()  # checking key holds

        if keys[pygame.K_LEFT]:
            playerX_change -= 2
        if keys[pygame.K_RIGHT]:
            playerX_change += 2
        if keys[pygame.K_SPACE]:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound("gunshot.mp3")
                bullet_sound.play()
                bullet_X = player_X
                fire_bullet(player_X, bullet_Y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         if bullet_state == "ready":
            #             bullet_sound = mixer.Sound("gunshot.mp3")
            #             bullet_sound.play()
            #             bullet_X = player_X
            #             fire_bullet(player_X, bullet_Y)

        # Background colour of the window:
        # screen.fill((12, 34, 56))

        # Player movement:
        if player_X <= 0:
            player_X = 0
        elif player_X >= 980:
            player_X = 980

        player_X += playerX_change

        # Enemy movement:
        for i in range(no_of_enemies):

            if enemy_X[i] <= 0:
                enemyX_change[i] = 0.5
            elif enemy_X[i] >= 980:
                enemyX_change[i] = -0.5

            enemy_X[i] += enemyX_change[i]

            if enemy_Y[i] <= 0:
                enemyY_change[i] = 0.5
            elif enemy_Y[i] >= 640:
                enemyY_change[i] = -0.5

            enemy_Y[i] += enemyY_change[i]

            collision = is_collision(
                enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
            if collision:
                kill_sound = mixer.Sound("kill.mp3")
                kill_sound.play()

                bullet_Y = 550
                bullet_state = "ready"
                score_value += 1

                enemy_X[i] = random.randint(0, 980)
                enemy_Y[i] = random.randint(0, 200)

            # Game Over:
            difference = 50
            difference_X = enemy_X[i] - player_X
            difference_Y = enemy_Y[i] - player_Y

            if (difference_X <= difference and difference_X >= (-1*difference)) and (difference_Y <= difference and difference_Y >= (-1*difference)):

                font_over = pygame.font.Font("freesansbold.ttf", 72)

                text_over = font_over.render(
                    "-1", True, (255, 255, 255))
                game_over = True
                main()

            enemy(enemy_X[i], enemy_Y[i], i)

        # Bullet movement:
        if bullet_Y <= -100:
            bullet_state = "ready"
            bullet_Y = 480

        if bullet_state == "fire":
            fire_bullet(bullet_X, bullet_Y)
            bullet_Y -= bulletY_change
        if game_over == True:
            screen.blit(text_over, (200, 315))

        player(player_X, player_Y)
        show_score(text_X, text_Y)
        pygame.display.update()


# game()


def main():
    global game_over, no_of_enemies, enemy_Y, score_value
    if game_over == True:
        for i in range(no_of_enemies):
            enemy_Y[i] = random.randint(0, 200)
        game_over = False
        score_value -= 2
        mixer.music.stop()

        game_over_sound = mixer.Sound("game_over.wav")
        game_over_sound.play()
        game()
    else:
        game()


main()
