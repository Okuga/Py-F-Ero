import pygame
import time
import random

pygame.init()

#CONSTANTS
GAME_NAME = "Py-F-Ero"
FAILURE_TEXT = "Game Over"
SCORE_LABEL = "Dodged: "
PAUSE_LABEL = "Paused"
GO_BUTTON_LABEL = "Go"
QUIT_BUTTON_LABEL = "Quit"
CONTINUE_BUTTON_LABEL = "Continue"

#256:224 is the SNES original resolution
DISPLAY_WIDTH = 256 * 3
DISPLAY_HEIGHT = 224 * 3

INITIAL_X = int(DISPLAY_WIDTH * 0.45)
INITIAL_Y = int(DISPLAY_HEIGHT * 0.65)
PLAYER_INITIAL_SPEED = 12

THING_INITIAL_Y = -600
THING_INITIAL_SPEED = 12

BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
LIGHT_RED = (255, 0, 0)
LIGHT_GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

CAR_WIDTH = 120
CAR_HEIGHT = 120
CAR_SIZE = (CAR_WIDTH, CAR_HEIGHT)

IMAGES_EXTENSION = ".png"
PLAYERS_OPTIONS = 4
PLAYER_FRAMES = 8

GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(GAME_NAME)
CLOCK = pygame.time.Clock()

LARGE_TEXT = 115
SMALL_TEXT = 25

TRACK_RECT_W = DISPLAY_WIDTH
TRACK_RECT_H = int(DISPLAY_HEIGHT/6) #The denominator must be even
TRACK_RECT_INITIAL_X = 0
TRACK_RECT_COLOR = BLUE
TRACK_BORDER_RATIO = 0.1
TRACK_BORDER_RATIO_PLAYER = 0.05
TRACK_SPEED = 60
LINE_COLOR = YELLOW
LINE_WIDTH = 25
CIRCLE_COLOR = YELLOW
CIRCLE_RADIUS = 15

ALLOWED_USER_ERROR = 0.9

NUMBER_OF_RECTS = int(DISPLAY_HEIGHT/TRACK_RECT_H)
NUMBER_OF_CIRCLES = int(DISPLAY_HEIGHT / (CIRCLE_RADIUS * 2)) + 1

DIFICULTY_INCREASE = 5

TRACK_M = 3

#GLOBAL VARIABLES
pause = False
track_state = True
players_imgs = []
 
#FUNCTIONS
def init_player_imgs():
    global players_imgs
    for i in range(0, PLAYERS_OPTIONS):
        player_imgs = []
        for j in range(0, PLAYER_FRAMES):
            img_path = "../art/player_" + str(i) + "_" + str(j) + IMAGES_EXTENSION
            player_imgs.append(pygame.transform.scale(pygame.image.load(img_path), CAR_SIZE))
        players_imgs.append(player_imgs)

def draw_player(x, y, p, i):
    global players_imgs
    GAME_DISPLAY.blit(players_imgs[p][i], (x, y))

def crash():
    GAME_DISPLAY.fill(BLACK)
    message_display_centered(FAILURE_TEXT, WHITE, LARGE_TEXT)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def message_display_centered(text, text_color, text_size):
    displayText = pygame.font.SysFont(None, text_size)
    text_surf, text_rect = text_objects(text, displayText, text_color)
    text_rect.center = (int(DISPLAY_WIDTH/2), int(DISPLAY_HEIGHT/2))
    GAME_DISPLAY.blit(text_surf, text_rect)

def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def draw_things(thingx, thingy, thingp, thingi):
    global players_imgs
    GAME_DISPLAY.blit(players_imgs[thingp][thingi], (thingx, thingy))

def things_dodged(count):
    font = pygame.font.SysFont(None, SMALL_TEXT)
    text = font.render(SCORE_LABEL + str(count), True, WHITE)
    GAME_DISPLAY.blit(text, (int(DISPLAY_WIDTH*0.01), int(DISPLAY_HEIGHT*0.01)))

def button(msg, x, y, w, h, active_color, color, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(GAME_DISPLAY, active_color, (x, y, w, h))
        if click[0] == 1:
            if(action != None):
                action()
    else:
        pygame.draw.rect(GAME_DISPLAY, color, (x, y, w, h))

    small_text = pygame.font.SysFont(None, SMALL_TEXT)
    text_surf, text_rect = text_objects(msg, small_text, WHITE)
    text_rect.center = (int(x+(w/2)), int(y+(h/2)))
    GAME_DISPLAY.blit(text_surf, text_rect)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_RETURN:
                    go()
        
        GAME_DISPLAY.fill(BLACK)
        message_display_centered(GAME_NAME, WHITE, LARGE_TEXT)

        button(GO_BUTTON_LABEL, int(DISPLAY_WIDTH*0.3), int(DISPLAY_HEIGHT*0.8), 100, 50, LIGHT_GREEN, GREEN, go)
        button(QUIT_BUTTON_LABEL, int(DISPLAY_WIDTH*0.6), int(DISPLAY_HEIGHT*0.8), 100, 50, LIGHT_RED, RED, quit_game)

        pygame.display.update()
        CLOCK.tick(15)

def pause_game():
    global pause
    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key == pygame.K_RETURN:
                    unpause()
        
        GAME_DISPLAY.fill(BLACK)
        message_display_centered(PAUSE_LABEL, WHITE, LARGE_TEXT)

        button(CONTINUE_BUTTON_LABEL, 150, 450, 100, 50, LIGHT_GREEN, GREEN, unpause)
        button(QUIT_BUTTON_LABEL, 550, 450, 100, 50, LIGHT_RED, RED, quit_game)

        pygame.display.update()
        CLOCK.tick(15)

def unpause():
    global pause
    pause = False

def go():
    game_loop()

def quit_game():
    pygame.quit()
    quit()

def draw_background():
    global track_state
    if track_state:
        track_rect_y = 0
    else:
        track_rect_y = int(TRACK_RECT_H/2)

    for i in range(0, NUMBER_OF_RECTS):
        rect_color = BLUE
        if i % 2 == 0:
            rect_color = GRAY
        draw_track_rect(track_rect_y, rect_color)
        track_rect_y = (track_rect_y + TRACK_RECT_H) % DISPLAY_HEIGHT

    pygame.draw.polygon(GAME_DISPLAY, BLACK, (
        (int(DISPLAY_WIDTH * TRACK_BORDER_RATIO), 0),
        (0, DISPLAY_HEIGHT),
        (0, 0)
        ))
    pygame.draw.polygon(GAME_DISPLAY, BLACK, (
        (int(DISPLAY_WIDTH * (1 - TRACK_BORDER_RATIO)), 0),
        (DISPLAY_WIDTH, DISPLAY_HEIGHT),
        (DISPLAY_WIDTH, 0)
        ))
    
    circle_x_left = int(DISPLAY_WIDTH * TRACK_BORDER_RATIO)
    circle_x_right = int(DISPLAY_WIDTH * (1 - TRACK_BORDER_RATIO))
    
    if track_state:
        circle_y = 0
    else:
        circle_y = CIRCLE_RADIUS
    
    for i in range(NUMBER_OF_CIRCLES):
        pygame.draw.circle(GAME_DISPLAY, CIRCLE_COLOR, (circle_x_left, circle_y), CIRCLE_RADIUS)
        pygame.draw.circle(GAME_DISPLAY, CIRCLE_COLOR, (circle_x_right, circle_y), CIRCLE_RADIUS)
        circle_x_left -= TRACK_M
        circle_x_right += TRACK_M
        circle_y += CIRCLE_RADIUS * 2

    track_state = not track_state

def draw_track_rect(track_rect_y, rect_color):
    pygame.draw.rect(GAME_DISPLAY, rect_color, (TRACK_RECT_INITIAL_X, track_rect_y, TRACK_RECT_W, TRACK_RECT_H))
    if(track_rect_y + TRACK_RECT_H > DISPLAY_HEIGHT):
        track_rect_y_offset_h = (track_rect_y + TRACK_RECT_H) - DISPLAY_HEIGHT
        track_rect_y_offset_y = 0
        pygame.draw.rect(GAME_DISPLAY, rect_color, (TRACK_RECT_INITIAL_X, track_rect_y_offset_y, TRACK_RECT_W, track_rect_y_offset_h))

#MAIN GAME FUNCTION
def game_loop():
    x = INITIAL_X
    y = INITIAL_Y

    player_img = 0
    player_frame = 0

    x_change = 0

    thing_starty = THING_INITIAL_Y
    thing_speed = THING_INITIAL_SPEED
    thing_width = CAR_WIDTH
    thing_height = CAR_HEIGHT
    thing_startx = random.randrange(int(DISPLAY_WIDTH * TRACK_BORDER_RATIO), int(DISPLAY_WIDTH * (1 - TRACK_BORDER_RATIO)) - thing_width)
    thing_player_frame = random.randrange(0, PLAYER_FRAMES)
    thing_player_img = random.randrange(0, PLAYERS_OPTIONS)

    game_exit = False

    dodged = 0

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -PLAYER_INITIAL_SPEED
                if event.key == pygame.K_RIGHT:
                    x_change = PLAYER_INITIAL_SPEED
                if event.key == pygame.K_ESCAPE:
                    pause_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        draw_background()
        draw_things(thing_startx, thing_starty, thing_player_img, thing_player_frame)
        draw_player(x, y, player_img, player_frame)
        things_dodged(dodged)

        thing_player_frame = (thing_player_frame + 1) % PLAYER_FRAMES
        thing_starty += thing_speed

        if x > (DISPLAY_WIDTH * (1 - TRACK_BORDER_RATIO_PLAYER)) - CAR_WIDTH or x < DISPLAY_WIDTH * TRACK_BORDER_RATIO_PLAYER:
            crash()

        if thing_starty >= DISPLAY_HEIGHT:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(int(DISPLAY_WIDTH * TRACK_BORDER_RATIO), int(DISPLAY_WIDTH * (1 - TRACK_BORDER_RATIO)) - thing_width)
            thing_player_img = random.randrange(0, PLAYERS_OPTIONS)
            dodged += 1
            if(dodged % DIFICULTY_INCREASE == 0):
                thing_speed += 1

        if y <= thing_starty + (thing_height * ALLOWED_USER_ERROR) and y + (CAR_HEIGHT * ALLOWED_USER_ERROR) >= thing_starty:
            if x + (CAR_WIDTH * ALLOWED_USER_ERROR) >= thing_startx and x <= thing_startx + (thing_width * ALLOWED_USER_ERROR):
                crash()

        player_frame = (player_frame + 1) % PLAYER_FRAMES

        pygame.display.update()
        CLOCK.tick(30)

init_player_imgs()
game_intro() 