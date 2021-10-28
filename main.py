import pygame as pg
import random
from pygame import mixer

# Initialize pygame
pg.init()

# Create Screen
screen = pg.display.set_mode((800, 600))

# Create background
background = pg.image.load('spacebackground.jpg')

# Create background music
mixer.music.load('background_music.mp3')
mixer.music.play(-1)

# Create Title and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load('spaceship.png')
pg.display.set_icon(icon)

# Create player spaceship
player_ship = pg.image.load('player.png')
player_x_axis = 365
player_y_axis = 520
player_x_change = 0

# Create enemy spaceship
# Create multiple enemies
enemy_bug = []
enemy_x_axis = []
enemy_y_axis = []
enemy_x_change = []
enemy_y_change = []
num_of_enemy = 15

for i in range(num_of_enemy):
    enemy_bug.append(pg.image.load('robot.png'))
    enemy_x_axis.append(random.randint(0, 780))
    enemy_y_axis.append(random.randint(80, 150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(30)

# Create bullet
bullet_img = pg.image.load('bullet.png')
bullet_x_axis = 0
bullet_y_axis = 520
bullet_x_change = 0
bullet_y_change = 4.5
bullet_state = 'ready'
enemy_eliminated = 0

# Score
score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)
text_x_axis = 10
test_y_axis = 10

# Game Over Font
over = pg.font.Font('freesansbold.ttf', 256)
over_x_axis = 300
over_y_axis = 280


def game_over():
    over_test = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_test, (over_x_axis, over_y_axis))


def score_func(x, y):
    score = font.render("Score: {}".format(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_ship, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_bug[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def collision(enemy_x_axis, enemy_y_axis, bullet_x_axis, bullet_y_axis):
    distance = (((bullet_x_axis - enemy_x_axis) ** 2) + ((bullet_y_axis - enemy_y_axis) ** 2)) ** 0.5
    if distance < 10:
        return True
    else:
        return False


num_bullet = 3

# Game loop
"""We create a loop to keep the program running until the exit button is clicked"""
running = True
while running:

    # Add screen colour
    screen.fill((50, 85, 225))
    screen.blit(background, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player_x_change = -0.9

            if event.key == pg.K_RIGHT:
                player_x_change = 0.9

            # for i in range(num_bullet):
            if event.key == pg.K_SPACE:

                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('bullet_sound.mp3')
                    bullet_sound.play()
                    bullet_x_axis = player_x_axis
                    bullet(bullet_x_axis, bullet_y_axis)
            # print('You have {} bullets left'.format(num_bullet))
            # num_bullet -= 1

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player_x_change = 0
            if event.key == pg.K_RIGHT:
                player_x_change = 0

    #  Player movement
    player_x_axis += player_x_change

    if player_x_axis < 0:
        player_x_axis = 0
    elif player_x_axis >= 736:
        player_x_axis = 736

    # Enemy movement
    for i in range(num_of_enemy):
        # Game Over
        if enemy_y_axis[i] > 500:
            for j in range(num_of_enemy):
                enemy_y_axis[j] = 1000
            game_over()
            break

        enemy_x_axis[i] += enemy_x_change[i]

        if enemy_x_axis[i] < 0:
            enemy_x_change[i] = 0.5
            enemy_y_axis[i] += enemy_y_change[i]
        elif enemy_x_axis[i] >= 776:
            enemy_x_change[i] = -0.5
            enemy_y_axis[i] += enemy_y_change[i]

        # Collision
        is_collision = collision(enemy_x_axis[i], enemy_y_axis[i], bullet_x_axis, bullet_y_axis)
        if is_collision:
            collision_sound = mixer.Sound('short-explosion.wav')
            collision_sound.play()
            bullet_y_axis = 520
            bullet_state = 'ready'
            enemy_eliminated += 1
            score_value += 5
            print('Eliminated: ', enemy_eliminated)
            print('Score: ', score_value)
            enemy_x_axis[i] = random.randint(0, 800)
            enemy_y_axis[i] = random.randint(80, 150)

        enemy(enemy_x_axis[i], enemy_y_axis[i], i)

    # Bullet movement
    if bullet_y_axis <= 0:
        bullet_y_axis = 520
        bullet_state = 'ready'
    if bullet_state is 'fire':
        bullet(bullet_x_axis, bullet_y_axis)
        bullet_y_axis -= bullet_y_change

    player(player_x_axis, player_y_axis)
    score_func(text_x_axis, test_y_axis)

    pg.display.update()
