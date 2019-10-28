import pygame
import random
import math

from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((970, 621))

# background
background = pygame.image.load("background.jpg")
mixer.music.load("background_music.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load("player.png")
playerX = 453
playerY = 550
playerX_change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 15

for i in range(number_of_enemies):
    enemy_image.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 905))
    enemyY.append(random.randint(5, 330))
    enemyX_change.append(10)
    enemyY_change.append(15)

# Bullet
bullet_image = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 550
bulletX_change = 4
bulletY_change = 10
# Ready - bullet can't be seen on screen
# Fire - bullet is on the way
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over test
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 100))
    screen.blit(over_text, (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 20, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # Screen background color
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    # Get event
    for event in pygame.event.get():
        # Exit strategy
        if event.type == pygame.QUIT:
            running = False

        # Move spaceship
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("sound_shot.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 906:
        playerX = 906

    # Enemy movement
    for i in range(number_of_enemies):

        # Game over
        if enemyY[i] > 500:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text(300, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 906:
            enemyX_change[i] = -10
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("sound_explode.wav")
            explosion_sound.play()
            bulletY = 550
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 905)
            enemyY[i] = random.randint(5, 330)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 550
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
