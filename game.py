import random
from tracemalloc import start
import pygame
import sys

# initialize PyGame modules
pygame.init()
pygame.display.set_caption('Flappy Bird')

# create the window that the game will be displayed on
screen = pygame.display.set_mode((500, 750))

# load background image
background_image = pygame.image.load('background.jpg')

# load the bird image
bird_image = pygame.image.load('flappybird.jpg')

# variables to keep track of the birds position on the screen
bird_x = 50
bird_y = 300
bird_y_change = 0.375

# blueprint variables for TOP obstacle dimensions/position
obstacle_width = 70
top_obstacle_height = random.randint(150, 450)
obstacle_colour = (211, 253, 117)
obstacle_x = 500
obstacle_x_change = -0.25  # moves the obstacles towards the bird
obstacle_gap = 175  # defines the size of the gap between the obstacles

# score/start/end menu
score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
start_menu_font = pygame.font.Font('freesansbold.ttf', 28)


def display_bird(x, y):
    screen.blit(bird_image, (x, y))


def draw_obstacles(top_obstacle_height):
    # draw top obstacle
    pygame.draw.rect(screen, obstacle_colour, (obstacle_x, 0,
                     obstacle_width, top_obstacle_height))

    # the y-position of where the bottom obstacle will be drawn
    bottom_obstacle_y_pos = top_obstacle_height + obstacle_gap
    # the height of the bottom obstacle
    bottom_obstacle_height = 635 - bottom_obstacle_y_pos

    # draw the bottom obstacle
    pygame.draw.rect(screen, obstacle_colour, (obstacle_x, bottom_obstacle_y_pos,
                     obstacle_width, bottom_obstacle_height))


def detect_collision(obstacle_x, top_obstacle_height, bird_y, bottom_obstacle_y_pos):
    # check if the obstacles are vertically aligned with any part of the bird
    if obstacle_x >= 50 and obstacle_x <= 50 + 64:
        # check if the bird made contact with either obstacle
        if bird_y <= top_obstacle_height or bird_y >= bottom_obstacle_y_pos - 64:
            return True

    # check if the bird makes contact with the ground
    elif bird_y >= 570:
        return True

    return False


def display_score(score):
    display = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(display, (10, 10))


def start_menu():
    # load background image
    background_image = pygame.image.load('background.jpg')
    bird_image = pygame.image.load('flappybird.jpg')
    screen.blit(background_image, (0, 0))
    screen.blit(bird_image, (50, 300))
    display = start_menu_font.render(
        "PRESS SPACEBAR TO BEGIN", True, (255, 255, 255))
    screen.blit(display, (50, 250))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


start_menu()


# game event loop
while True:

    # display background image
    screen.blit(background_image, (0, 0))

    # for loop effectively listens for all events that occur while the game is running
    for event in pygame.event.get():
        # check for quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # check for key presses to set the bird's change in y-position
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_y_change = -0.75
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            bird_y_change = 0.375

    # move the bird
    bird_y += bird_y_change

    # limit how far the bird can go in the y direction
    if bird_y <= 0:
        bird_y = 0
    if bird_y >= 570:
        bird_y = 570

    # move the obstacles
    obstacle_x += obstacle_x_change

    # increment score and generate new obstacles if the bird doesn't hit an obstacle
    if obstacle_x <= -10:
        score += 1
        obstacle_x = 500
        top_obstacle_height = random.randint(150, 450)

    collision = detect_collision(
        obstacle_x, top_obstacle_height, bird_y, top_obstacle_height + obstacle_gap)

    if collision:
        pygame.quit()
        sys.exit()

    # function calls to update the state of the game
    draw_obstacles(top_obstacle_height)
    display_bird(bird_x, bird_y)
    display_score(score)
    pygame.display.update()
