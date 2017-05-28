#!/usr/bin/python3
import sys
import sdl2
import sdl2.ext
from random import randint
import functools
import time

WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)
YELLOW = sdl2.ext.Color(255, 255, 0)
RED = sdl2.ext.Color(160, 0, 0)
GRAY = sdl2.ext.Color(50, 50, 50)
W = 640
H = 480

width = 64
height = 40

stepx = 10
stepy = 10

init_stepx = stepx
init_stepy = stepy

originx = 0
originy = 0

speed = 0

show_grid = True
show_fingerprint = True

def print_help():
    print("Controls:")
    print("WASD        - move map")
    print("mouse drag  - move map")
    print("mouse click - toggle cell")
    print("+ or \"-\"    - change zoom level")
    print("mouse wheel - change zoom level")
    print("r           - clear map")
    print("c           - fill map with random")
    print("n           - toggle grid")
    print("f           - toggle fingerprint display")

if (len(sys.argv) != 3):
    print("usage: ./life.py width height [--help]")
    if len(sys.argv) == 2 and (sys.argv[1] == "--help"):
        print_help()
    exit(0)
else:
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    if (width <= 0 or height <= 0):
        print("ERROR: Invalid map size!")
        exit(1)


def get_start_end():
    startx = -(originx // stepx) - 1
    starty = -(originy // stepy) - 1
    endx = int((W / stepx)) - (originx) // stepx
    endy = int((H / stepy)) - (originy) // stepy
    # endx = int((width / stepx) * init_stepx) - (originx) // stepx
    # endy = int((height / stepy) * init_stepy) - (originy) // stepy

    startx = width if (startx > width) else startx
    starty = height if (starty > height) else starty
    endx = width if (endx > width) else endx
    endy = height if (endy > height) else endy
    startx = 0 if (startx < 0) else startx
    starty = 0 if (starty < 0) else starty
    endx = 0 if (endx < 0) else endx
    endy = 0 if (endy < 0) else endy
    return (((starty, startx), (endy, endx)))

def draw_grid(window):
    surface = window.get_surface()
    i = 0
    while i <= height:
        sdl2.ext.line(surface, GRAY,
            (0 + originx,
            i * stepy + originy,
            (width) * stepx + originx,
            i * stepy + originy))
        i += 1
    i = 0
    while i <= width:
        sdl2.ext.line(surface, GRAY,
            (i * stepx + originx,
            0 + originy,
            i * stepx + originx,
            (height) * stepy + originy))
        i += 1

def map_init():
    h_map = []
    for i in range(0, height):
        h_map.append([])
    for i in range(0, height):
        h_map[i] = ([0] * width)
    return (h_map)

def fill_rand_map(h_map):
    for i in range(0, height):
        for j in range(0, width):
            h_map[i][j] = randint(0,1)
    return (h_map);

def print_map(h_map,back_up_map, window):
    surface = window.get_surface()
    if (show_fingerprint):
        print_fingerprint(back_up_map, window)
    else:
        sdl2.ext.fill(surface, BLACK)
    ((starty, startx), (endy, endx)) = get_start_end()
    if (show_grid):
        draw_grid(window)
    for i in range(starty, endy):
        for j in range(startx, endx):
            if (h_map[i][j] == 1):
                sdl2.ext.fill(surface, YELLOW,
                    (j * stepx + originx, i * stepy + originy, stepx, stepy))

def add_to_fing(h_map, back_up_map):
    for i in range(0, height):
        for j in range(0, width):
            if (h_map[i][j] == 1):
                back_up_map[i][j] = 1
    return (back_up_map)

def print_fingerprint(h_map, window):
    surface = window.get_surface()
    sdl2.ext.fill(surface, BLACK)
    ((starty, startx), (endy, endx)) = get_start_end()
    if (show_grid):
        draw_grid(window)
    for i in range(starty, endy):
        for j in range(startx, endx):
            if (h_map[i][j] == 1):
                sdl2.ext.fill(surface, RED,
                    (j * stepx + originx, i * stepy + originy, stepx, stepy))

def valid_neigh(pos):
    if (pos[0] < 0 or pos[0] >= height or pos[1] < 0 or pos[1] >= width):
        return (False)
    else:
        return (True)

def set_to_valid(pos):
    if (pos[0] < 0):
        pos[0] = height - 1
        return (set_to_valid(pos))
    if (pos[0] >= height):
        pos[0] = 0
        return (set_to_valid(pos))
    if (pos[1] < 0):
        pos[1] = width - 1
        return (set_to_valid(pos))
    if (pos[1] >= width):
        pos[1] = 0
        return (set_to_valid(pos))
    return (pos)


def neighbours(pos):
    neigh = []
    for i in range(-1, 1 + 1):
        for j in range(-1, 1 + 1):
            if (j == 0 and i == 0):
                continue
            t_pos = [pos[0] + i, pos[1] + j]
            if (valid_neigh(t_pos)):
                neigh.append(t_pos)
            else:
                neigh.append(set_to_valid(t_pos))
    return (neigh)

def ind_to_el(ind, h_map):
    res = []
    for el in ind:
        y = el[0]
        x = el[1]
        test = h_map[y][x]
        res.append(test)
    return (res)

def alive_neigh(h_map, pos):
    neigh_el = ind_to_el(neighbours(pos), h_map)
    return (functools.reduce((lambda res, el: res + el), neigh_el))

def evolve_cell(h_map, new_map, pos):
    aliveneigh = alive_neigh(h_map, pos)
    if (aliveneigh < 2):
        new_map[pos[0]][pos[1]] = 0
    if (aliveneigh == 3):
        new_map[pos[0]][pos[1]] = 1
    if (aliveneigh == 2 and h_map[pos[0]][pos[1]] == 1):
        new_map[pos[0]][pos[1]] = 1
    if (aliveneigh > 3):
        new_map[pos[0]][pos[1]] = 0

def evolve(h_map, new_map):
    for i in range(0, height):
        for j in range(0, width):
            evolve_cell(h_map, new_map, (i, j))
    return (new_map)

def toggle_cell(h_map, pos):
    y = (pos[0] - originy) // stepy
    x = (pos[1] - originx) // stepx
    if (not valid_neigh((y, x))):
        return (h_map)
    h_map[y][x] = (h_map[y][x] + 1) % 2
    return (h_map)

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("The Game of Life", size=(W, H))
    window.show()
    h_map = fill_rand_map(map_init())
    back_up_map = h_map
    print_map(h_map, back_up_map, window)
    running = True
    is_evolve = False
    while (running):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                    break
                if (event.key.keysym.sym == sdl2.SDLK_RETURN
                    or event.key.keysym.sym == sdl2.SDLK_p):
                    is_evolve = not is_evolve
                if event.key.keysym.sym == sdl2.SDLK_w:
                    global originy
                    originy += 10
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_s:
                    originy -= 10
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_a:
                    global originx
                    originx += 10
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_d:
                    originx -= 10
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_EQUALS:
                    global stepx, stepy
                    stepx += 1
                    stepy += 1
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_MINUS:
                    stepx -= 1
                    stepy -= 1
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_r:
                    h_map = map_init()
                    back_up_map = h_map
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_c:
                    h_map = fill_rand_map(map_init())
                    back_up_map = h_map
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_COMMA:
                    global speed
                    speed += 1
                if event.key.keysym.sym == sdl2.SDLK_PERIOD:
                    speed -= 1
                    if (speed < 0):
                        speed = 0
                if event.key.keysym.sym == sdl2.SDLK_n:
                    global show_grid
                    show_grid = not show_grid
                    print_map(h_map, back_up_map, window)
                if event.key.keysym.sym == sdl2.SDLK_f:
                    global show_fingerprint
                    show_fingerprint = not show_fingerprint
                    print_map(h_map, back_up_map, window)
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                h_map = toggle_cell(h_map, (event.button.y, event.button.x))
                print_map(h_map, back_up_map, window)
            if event.type == sdl2.SDL_MOUSEWHEEL:
                if event.wheel.y > 0:
                    stepx += 1
                    stepy += 1
                    print_map(h_map, back_up_map, window)
                elif event.wheel.y < 0:
                    stepx -= 1
                    stepy -= 1
                    if (stepx <= 0):
                        stepx = 1
                    if (stepy <= 0):
                        stepy = 1
                    print_map(h_map, back_up_map, window)
            if event.type == sdl2.SDL_MOUSEMOTION:
                if event.motion.state & sdl2.SDL_BUTTON_LMASK:
                    originx += event.motion.xrel
                    originy += event.motion.yrel
                    print_map(h_map, back_up_map, window)
        if is_evolve:
            h_map = evolve(h_map, map_init())
            back_up_map = add_to_fing(h_map, back_up_map)
            print_map(h_map, back_up_map, window)
            if (speed > 0):
                time.sleep(speed / 10)
        window.refresh()
    return (0)

if __name__ == "__main__":
    sys.exit(run())
