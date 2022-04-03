import sys
import pygame as pg
from pygame.locals import *
import time


field = [[None] * 3, [None] * 3, [None] * 3]

WINNER = None
DRAW = False
LINE_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 400
HEIGHT = 400
XO = "X"



pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)
pg.display.set_caption("My Tic Tac Toe")
Clock = pg.time.Clock()
fps = 30

open_img = pg.image.load("tic tac opening.png")
o_img = pg.image.load("O.png")
x_img = pg.image.load("X.png")

open_img = pg.transform.scale(open_img, (WIDTH, HEIGHT + 100))
o_img = pg.transform.scale(o_img, (80, 80))
x_img = pg.transform.scale(x_img, (80, 80))


def game_opening():
    screen.blit(open_img, (0, 0))
    pg.display.update()

    time.sleep(2)

    screen.fill(WHITE)

    pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)

    pg.draw.line(screen, LINE_COLOR, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pg.draw.line(screen, LINE_COLOR, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)
    draw_status()

    pg.display.update()


def draw_status():
    global DRAW, XO
    if WINNER is None:
        status = f"{XO}'s Turn"
    else:
        status = f"{WINNER} Won!"
    if DRAW:
        status = "It's a Draw!"

    font = pg.font.Font(None, 30)
    text = font.render(status, 1, WHITE)
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(WIDTH / 2, 450))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global WINNER, DRAW, field
    for row in range(3):
        if field[row][0] == field[row][1] == field[row][2] and field[row][0] is not None:
            WINNER = field[row][0]
            pg.draw.line(screen, (255, 0, 0), (0, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         (WIDTH, (row + 1) * HEIGHT / 3 - HEIGHT / 6), 2)
            break

    for col in range(3):
        if field[0][col] == field[1][col] == field[2][col] and field[0][col] is not None:
            WINNER = field[0][col]

            pg.draw.line(screen, (255, 0, 0), ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 2)

            break
    if field[0][0] == field[1][1] == field[2][2] and field[0][0] is not None:
        WINNER = field[0][0]
        pg.draw.line(screen, (255, 0, 0), (50, 50), (350, 350), 2)

    elif field[0][2] == field[1][1] == field[2][0] and field[0][2] is not None:
        WINNER = field[0][2]
        pg.draw.line(screen, (255, 0, 0), (50, 350), (350, 50), 2)

    elif all([all(row) for row in field]) and WINNER is None:
        DRAW = True

    draw_status()


def draw_XO(row, col):
    global XO, field
    if row == 1:
        posy = 30

    elif row == 2:
        posy = HEIGHT / 3 + 30

    elif row == 3:
        posy = HEIGHT / 3 * 2 + 30

    if col == 1:
        posx = 30
    elif col == 2:
        posx = WIDTH / 3 + 30
    elif col == 3:
        posx = WIDTH / 3 * 2 + 30

    field[row - 1][col - 1] = XO
    if XO == "X":
        screen.blit(x_img, (posx, posy))
        XO = "O"
    else:
        screen.blit(o_img, (posx, posy))
        XO = "X"

    pg.display.update()


def user_click():
    x, y = pg.mouse.get_pos()
    if x < WIDTH / 3:
        col = 1
    elif x < WIDTH / 3 * 2:
        col = 2
    elif x < WIDTH:
        col = 3
    else:
        col = None

    if y < HEIGHT / 3:
        row = 1
    elif y < HEIGHT / 3 * 2:
        row = 2
    elif y < HEIGHT:
        row = 3
    else:
        row = None

    if row and col and field[row - 1][col - 1] is None:
        draw_XO(row, col)
        check_win()


def reset_game():
    global field, DRAW, WINNER, XO
    time.sleep(3)
    XO = "X"
    field = [[None] * 3, [None] * 3, [None] * 3]
    WINNER = None
    DRAW = False
    game_opening()


game_opening()

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_click()
            if (WINNER or DRAW):
                reset_game()

    pg.display.update()
    Clock.tick(fps)
