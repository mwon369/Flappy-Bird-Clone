import random
import pygame
import sys

# initialize PyGame modules
pygame.init()
pygame.display.set_caption('Flappy Bird')

# initialize the window that the game will be displayed on
screen = pygame.display.set_mode((500, 750))

# load game art
background_image = pygame.image.load('background.jpg')
bird_image = pygame.image.load('flappybird.jpg')

# variables to keep track of & change the birds position on screen
bird_x = 50
bird_y = 300
bird_y_change = 4

# variables for the dimensions, colour and position of the obstacles
obstacle_width = 70
top_obstacle_height = random.randint(150, 450)
obstacle_colour = (211, 253, 117)
obstacle_x = 500
obstacle_x_change = -2.5
obstacle_gap = 150

# variables for the score, highscore, start and end menus
score = 0
score_list = [0]
score_font = pygame.font.Font('freesansbold.ttf', 32)
menu_font = pygame.font.Font('freesansbold.ttf', 28)


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
    background_image = pygame.image.load('background.jpg')
    bird_image = pygame.image.load('flappybird.jpg')
    screen.blit(background_image, (0, 0))
    screen.blit(bird_image, (50, 300))

    start_menu_text = menu_font.render(
        "PRESS SPACEBAR TO BEGIN", True, (255, 255, 255))
    screen.blit(start_menu_text, (50, 250))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


def game_over_menu(score, score_list):
    background_image = pygame.image.load('background.jpg')
    screen.blit(background_image, (0, 0))

    # initialize all the text
    game_over_text = menu_font.render(
        "GAME OVER!", True, (255, 50, 50))
    current_score = menu_font.render(
        f"Your score was: {score}", True, (255, 255, 255))
    high_score = menu_font.render(
        f"Your current high score is: {max(score_list)}", True, (255, 255, 255))
    play_again = menu_font.render(
        "Press TAB to play again!", True, (255, 255, 255))
    new_high_score_1 = menu_font.render(
        "Congratulations!", True, (50, 255, 50))
    new_high_score_2 = menu_font.render(
        f"Your NEW highscore is {score}!", True, (50, 255, 50))

    # display the text
    if score > max(score_list[:-1]):
        screen.blit(game_over_text, (150, 225))
        screen.blit(current_score, (125, 275))
        screen.blit(new_high_score_1, (130, 325))
        screen.blit(new_high_score_2, (75, 375))
        screen.blit(play_again, (80, 425))
    else:
        screen.blit(game_over_text, (150, 250))
        screen.blit(current_score, (125, 300))
        screen.blit(high_score, (60, 350))
        screen.blit(play_again, (80, 400))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                return


# infinite loop to start and run the game
while True:
    start_menu()

    # reset all variables that changed during the last session to default values
    bird_y = 300
    obstacle_x = 500
    obstacle_x_change = -2.5
    score = 0
    clock = pygame.time.Clock()

    while True:
        # ensures that all computers run the program at the same speed for consistency
        clock.tick(60)
        # display background image
        screen.blit(background_image, (0, 0))

        # loop to listen for all user-input related events while the game runs
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # check for key presses to set the bird's change in y-position
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_y_change = -8
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                bird_y_change = 4

        # move the bird
        bird_y += bird_y_change

        # limit how far the bird can go in the y direction
        if bird_y <= 0:
            bird_y = 0
        if bird_y >= 570:
            bird_y = 570

        # move the obstacles
        obstacle_x += obstacle_x_change

        # increment score, generate new obstacles and increase game speed everytime the player passes an obstacle
        if obstacle_x <= -10:
            score += 1
            obstacle_x = 500
            obstacle_x_change -= 0.1
            top_obstacle_height = random.randint(150, 450)

        # check for the player losing
        collision = detect_collision(
            obstacle_x, top_obstacle_height, bird_y, top_obstacle_height + obstacle_gap)
        if collision:
            score_list.append(score)
            game_over_menu(score, score_list)
            break

        # function calls to update the state of the game
        draw_obstacles(top_obstacle_height)
        display_bird(bird_x, bird_y)
        display_score(score)
        pygame.display.update()
