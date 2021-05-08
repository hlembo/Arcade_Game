import pygame
import sys
from pygame.locals import *
import random
import math
from pygame import mixer

pygame.init()
WIDTH = 1920
HEIGHT = 1080
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)

# background image
back_ground = pygame.image.load('venv/assests/Background.jpg')

# Score variable
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Title and Icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('venv/assests/game.png')
pygame.display.set_icon(icon)

# keys boolean variables
K_A = False
K_S = False
K_D = False
K_W = False
K_SPACE = False

# player
player_img = pygame.image.load('venv/assests/Ship.png')
player_X = WIDTH / 2
player_Y = HEIGHT / 2
player_x_change = 0
player_y_change = 0

# enemy
en_im = []
en_img = (pygame.image.load('venv/assests/ufo.png'))
en_X = []
en_Y = []
en_x_change = []
en_y_change = []
num_enemy = 10
for i in range(num_enemy):
    en_im.append(pygame.image.load('venv/assests/sonic.png'))
    en_X.append(random.randint(0, screen.get_width() - en_im[i].get_width()))
    en_Y.append(random.randint(0, (screen.get_height() - en_im[i].get_height()) / 4))
    en_x_change.append(5)
    en_y_change.append(132)

# bullet
bullet_img = pygame.image.load('venv/assests/bullet.png')
bullet_X = player_X
bullet_Y = player_Y
bullet_y_player = 0
bullet_x_change = 1
bullet_y_change = 20
bullet_State = False

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def key_released():
    global K_A
    global K_S
    global K_D
    global K_W
    global K_SPACE

    if event.key == pygame.K_w:
        K_W = False
        print("W")
    if event.key == pygame.K_s:
        K_S = False
        print("S")
    if event.key == pygame.K_d:
        K_D = False
        print("D")
    if event.key == pygame.K_a:
        K_A = False
        print("A")
    if event.key == pygame.K_SPACE:
        K_SPACE = False
        print("space")
def key_pressed():
    global K_A
    global K_S
    global K_D
    global K_W
    global K_SPACE
    if event.key == pygame.K_w:
        K_W = True
    if event.key == pygame.K_s:
        K_S = True
    if event.key == pygame.K_d:
        K_D = True
    if event.key == pygame.K_a:
        K_A = True
    if event.key == pygame.K_SPACE:
        K_SPACE = True


def game_over_text():
    over_text = font.render("GAME OVER ", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(over_text, (screen.get_width() / 2, screen.get_height() / 2))


def fire_bullet(x, y):
    global bullet_State
    bullet_State = True
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if bullet_State:
        if distance < 27:
            return True
        else:
            return False


def enemy(x, y, i_i):
    screen.blit(en_im[i_i], (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))



def show_score(x, y):
    score_1 = font.render("Score :" + str(score), True, (255, 255, 255))
    screen.blit(score_1, (x, y))

def bullet_Condition(bullet_S):
    global bullet_Y
    global bullet_X
    if not bullet_State:
        bullet_sound = mixer.Sound('venv/assests/ex.mp3')
        bullet_sound.play()
        bullet_X = player_X
        bullet_Y = player_Y
        fire_bullet(bullet_X, bullet_Y)

# GAME LOOP
game_over = True
# back ground game sound
if game_over:
    mixer.music.load('venv/assests/SAO.mp3')
    mixer.music.set_volume(1000000)
    mixer.music.play(-1)
else:
    mixer.music.load('venv/assests/inter.ogg')
    mixer.music.set_volume(1000000)
    mixer.music.play(-1)
while game_over:  # main game loop
    # Red Green Blue 0-255 (Also fills the background before Player is drawn)
    screen.fill((0, 0, 0))
    back_ground = pygame.transform.scale(back_ground, (screen.get_width(), screen.get_height()))
    screen.blit(back_ground, (0, 0))
    pygame.draw.line(screen, (255,0,0),(screen.get_width(), ((screen.get_height() * 0.75) - en_img.get_height())),(0, screen.get_height() * 0.75 - en_img.get_height()), en_img.get_height() - 60)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            WIDTH = screen.get_width()
            HEIGHT = screen.get_height()
        if event.type == WINDOWMINIMIZED:
            screen = pygame.display.set_mode((500, 500), RESIZABLE)
        if event.type == pygame.KEYDOWN:
            key_pressed()
        if event.type == pygame.KEYUP:
            key_released()

    if not K_A:
        player_x_change = 0
    if not K_D:
        player_x_change = 0
    if not K_S:
        player_y_change = 0
    if not K_W:
        player_y_change = 0
    if K_A:
        player_x_change = -10
    if K_D:
        player_x_change = 10
    if K_S:
        player_y_change = 10
    if K_W:
        player_y_change = -10
    if K_SPACE:
        bullet_Condition(bullet_State)


    # Affecting the players x and y changes
    player_X += player_x_change
    player_Y += player_y_change

    #BOUNDARY CONDIITONS
    if player_X <= 0:
        player_X = 0
    if player_X >= WIDTH - player_img.get_width():
        player_X = WIDTH - player_img.get_width()
    if player_Y <= 0:
        player_Y = 0
    if player_Y >= HEIGHT - player_img.get_height():
        player_Y = HEIGHT - player_img.get_height()

        #Enemy Conditions for GAME OVER
    for i in range(num_enemy):
        if en_Y[i] >= screen.get_height() * 0.79:
            num_enemy = 2
            del en_im[0:]
            break
        if len(en_im) == 0:
            player_x_change = 0
            player_y_change = 0
            player_X = 0
            player_Y = 0
            game_over_text()
            break
        en_X[i] += en_x_change[i]
        if en_X[i] <= 0:
            en_X[i] = -1
            en_Y[i] += en_y_change[i]
        if en_X[i] >= WIDTH - en_im[i].get_width():
            en_X[i] = 1
            en_Y[i] += en_y_change[i]
        if en_Y[i] >= HEIGHT - en_im[i].get_height():
            en_X[i] = random.randint(0, screen.get_width() - en_im[i].get_width())
            en_Y[i] = random.randint(0, (screen.get_height() - en_im[i].get_height()) / 4)
        collision = is_collision(en_X[i], en_Y[i], bullet_X, bullet_Y)
        if collision:
            ex_sound = mixer.Sound('venv/assests/ex.mp3')
            ex_sound.play()
            point_sound = mixer.Sound('venv/assests/Point.wav')
            point_sound.play()
            bullet_State = False
            score += 1

            en_X[i] = random.uniform(0, (screen.get_width() - en_im[i].get_width()))
            en_Y[i] = random.uniform(0, (screen.get_height() - en_im[i].get_height()) / 4)

        enemy(en_X[i], en_Y[i], i)
    # Bullet Movement

    # the Reset for the bullet
    if bullet_Y <= 0:
        bullet_Y = player_Y
        bullet_State = False
    if bullet_State:
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_y_change

    # collison
    player(player_X, player_Y)
    show_score(textX, textY)

    pygame.display.update()

