import pygame as pg
from pygame.locals import *
import sys
import os
import random

pg.init()
monitor_width, monitor_height = pg.display.Info().current_w, pg.display.Info().current_h  # monitor size
screen_width_small, screen_height_small = (640, 480)  # small screen size
screen_width, screen_height = monitor_width, monitor_height
screen = pg.display.set_mode((monitor_width, monitor_height), pg.FULLSCREEN)  # sets screen size
fullscreen = True
pg.display.set_caption('Particle Test Chamber')  # set screen caption
clock = pg.time.Clock()  # initiates clock
fps = 60  # frames per second

tile_size = 10
options_font = pg.font.SysFont('Consolas', 15)
options = {
    0: ['Particle Options', ['-1'], -1],
    1: ['Amount: ', ['1', '2', '3', '4', '5', '10', '15', '20', '25', '30', '40', '50', '60', '70', '80', '90', '100'],
        0],
    2: ['Randomise: ', ['None', 'A Little', 'A Lot'], 1],
    3: ['X Velocity: ', ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5'], 5],
    4: ['Y Velocity: ', ['-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5'], 5],
    5: ['X Acceleration: ', ['-0.5', '-0.45', '-0.4', '-0.35', '-0.3', '-0.25', '-0.2', '-0.15', '-0.1', '-0.05', '0',
                             '0.05', '0.1', '0.15', '0.2', '0.25', '0.3', '0.35', '0.4', '0.45', '0.5'], 10],
    6: ['Y Acceleration: ', ['-0.5', '-0.45', '-0.4', '-0.35', '-0.3', '-0.25', '-0.2', '-0.15', '-0.1', '-0.05', '0',
                             '0.05', '0.1', '0.15', '0.2', '0.25', '0.3', '0.35', '0.4', '0.45', '0.5'], 10],
    7: ['Particle Colour: ', ['White', 'Black', 'Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange', 'Teal',
                              'Pink', 'Random'], 0],
    8: ['Size: ', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 3],
    9: ['Shrink Factor: ', ['0', '0.005', '0.01', '0.015', '0.02', '0.025', '0.03', '0.035', '0.04', '0.045', '0.05',
                            '0.055', '0.06', '0.065', '0.07', '0.075', '0.08', '0.085', '0.09', '0.095', '0.1'], 5],
    10: ['Glow: ', ['True', 'False'], 0],
    11: ['Glow Colour: ', ['White', 'Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange', 'Pink', 'Teal', 'Random'], 0],
    12: ['Physics: ', ['True', 'False'], 0],
    13: ['Bounce Factor: ', ['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'], 8],
    14: ['Orbit Point: ', ['None', 'Centre', 'Top Left', 'Top Right', 'Bottom Left', 'Bottom Right'], 0],
    15: ['Orbit Factor: ', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 4],
    16: ['Death Time: ', ['Never', '1', '2', '3', '4', '5', '10', '20', '30', '40', '50'], 0],

    17: ['Chamber Options', ['-1'], -1],
    18: ['Background Colour: ', ['White', 'Black', 'Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange'], 1],
    19: ['Tile Colour: ', ['White', 'Black', 'Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange', 'Teal',
                           'Pink', 'Random'], 0],
    20: ['Text Colour: ', ['White', 'Black', 'Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange'], 0],
    21: ['Border: ', ['None', 'Left', 'Right', 'Top', 'Bottom', 'L+R', 'T+B', 'All'], 7],
    22: ['Draw Orbit Point: ', ['True', 'False'], 1]
}  # options information dictionary (index: text, options, current option)


def main():
    global screen, screen_width, screen_height, fullscreen, buttons
    run = True
    particles = []
    clicking = [False] * 5
    tile_map = {}
    new_tile = {}
    remove_tile = {}
    button_collide = [0] * len(options)
    buttons = [0] * len(options)
    draw_options(button_collide)
    show_options = True
    while run:
        mouse_pos = (pg.mouse.get_pos()[0] + 1, pg.mouse.get_pos()[1] + 1)  # current position of mouse
        # checks for collision between mouse and all buttons
        button_collide = [int(buttons[index][2].collidepoint(mouse_pos)) if
                          options[index][2] != -1 and clicking == [False] * 5 else 0
                          for index in range(len(button_collide))]

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                keys_pressed = pg.key.get_pressed()
                if keys_pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_o:  # toggles options
                    show_options = not show_options
                if event.key == pg.K_f:
                    fullscreen = not fullscreen  # toggles full screen
                    if fullscreen:
                        for tile in range(int(screen_height / tile_size)):  # removes right border
                            name = str(int(screen_width / tile_size) - 1) + ';' + str(tile)
                            try:  # tries to remove tile from tile map
                                tile_map.pop(name)
                            except KeyError:
                                continue
                        for tile in range(int(screen_width / tile_size)):  # removes bottom border
                            name = str(tile) + ';' + str(int(screen_height / tile_size) - 1)
                            try:  # tries to remove tile from tile map
                                tile_map.pop(name)
                            except KeyError:
                                continue
                        screen_width, screen_height = monitor_width, monitor_height
                        screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)
                    else:
                        screen_width, screen_height = screen_width_small, screen_height_small
                        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (
                            int(pg.display.Info().current_w - screen_width) / 2,
                            int(pg.display.Info().current_h - screen_height) / 3)  # screen position
                        screen = pg.display.set_mode((screen_width, screen_height))

            if event.type == pg.MOUSEBUTTONDOWN:
                for button in range(1, 6):
                    if event.button == button:  # checks which mouse button has been pressed
                        clicking[button - 1] = True
                if event.button == 1:  # begins new tile placement
                    new_tile_pos_1 = [int(mouse_pos[0] / tile_size), int(mouse_pos[1] / tile_size)]
                if event.button == 2:  # begins tile replacement
                    remove_tile_pos_1 = [int(mouse_pos[0] / tile_size), int(mouse_pos[1] / tile_size)]

                if 1 in button_collide and show_options:  # if mouse is colliding with a button
                    if event.button == 4 or event.button == 5:
                        for _ in range(10):
                            particles.append(Particle(mouse_pos[0],
                                                      mouse_pos[1],
                                                      random.randint(-10, 10) / 10,
                                                      random.randint(-5, 5) / 10,
                                                      0,
                                                      0.2,
                                                      convert_colour(options[20][1][options[20][2]]),
                                                      random.randint(1, 3),
                                                      0.075,
                                                      False,
                                                      (0, 0, 0),
                                                      False,
                                                      0))
                        button = button_collide.index(1)  # gets collided button index
                        cur_index = options[button][2]
                        if event.button == 4:
                            new_index = cur_index + 1
                            if new_index > len(options[button][1]) - 1:  # wrap index value
                                new_index = 0
                        elif event.button == 5:
                            new_index = cur_index - 1
                            if new_index < 0:  # wrap index value
                                new_index = len(options[button][1]) - 1
                        options[button][2] = new_index  # new index

            if event.type == MOUSEBUTTONUP:
                for button in range(1, 6):
                    if event.button == button:  # checks which mouse button has been depressed
                        clicking[button - 1] = False
                        if event.button == 1:  # ends new tile placement
                            tile_map.update(new_tile)  # adds new tile to tile map
                            new_tile = {}  # resets new tile
                        if event.button == 2:  # ends new tile replacement
                            for tile in remove_tile:
                                try:  # tries to remove tile from tile map
                                    tile_map.pop(tile)
                                except KeyError:
                                    continue
                            remove_tile = {}  # resets remove tile

        for index, click in enumerate(clicking):
            if click:
                if index == 0:  # add tiles
                    new_tile_pos_2 = [int(mouse_pos[0] / tile_size), int(mouse_pos[1] / tile_size)]
                    new_tile_pos = [min(new_tile_pos_1[0], new_tile_pos_2[0]),
                                    max(new_tile_pos_1[0], new_tile_pos_2[0]),
                                    min(new_tile_pos_1[1], new_tile_pos_2[1]),
                                    max(new_tile_pos_1[1], new_tile_pos_2[1])]  # orders tile positions
                    new_tile = {}
                    for col in range(new_tile_pos[0], new_tile_pos[1]):  # creates dictionary for new tile
                        for row in range(new_tile_pos[2], new_tile_pos[3]):
                            new_tile[str(col) + ';' + str(row)] = [col, row,
                                                                   (convert_colour(options[19][1][options[19][2]]))]
                if index == 1:  # remove tiles
                    remove_tile_pos_2 = [int(mouse_pos[0] / tile_size), int(mouse_pos[1] / tile_size)]
                    remove_tile_pos = [min(remove_tile_pos_1[0], remove_tile_pos_2[0]),
                                       max(remove_tile_pos_1[0], remove_tile_pos_2[0]),
                                       min(remove_tile_pos_1[1], remove_tile_pos_2[1]),
                                       max(remove_tile_pos_1[1], remove_tile_pos_2[1])]  # orders tile positions
                    remove_tile = {}
                    for col in range(remove_tile_pos[0], remove_tile_pos[1]):  # creates dictionary for removing tile
                        for row in range(remove_tile_pos[2], remove_tile_pos[3]):
                            remove_tile[str(col) + ';' + str(row)] = [col, row,
                                                                      convert_colour(options[18][1][options[18][2]])]
                if index == 2:  # add particles
                    randomise = options[2][1][options[2][2]]
                    if randomise == 'None':
                        randomise = 0
                    elif randomise == 'A Little':
                        randomise = 1
                    elif randomise == 'A Lot':
                        randomise = 2
                    particle_options = [int(options[3][1][options[3][2]]), int(options[4][1][options[4][2]]),
                                        float(options[5][1][options[5][2]]), float(options[6][1][options[6][2]]),
                                        convert_colour(options[7][1][options[7][2]]), int(options[8][1][options[8][2]]),
                                        float(options[9][1][options[9][2]]), options[10][1][options[10][2]] == 'True',
                                        convert_glow_colour(options[11][1][options[11][2]]),
                                        options[12][1][options[12][2]] == 'True', float(options[13][1][options[13][2]]),
                                        convert_orbit(options[14][1][options[14][2]]),
                                        int(options[15][1][options[15][2]]),
                                        convert_death_time(options[16][1][options[16][2]])]
                    random_scale = [0.25, 0.25, 0, 0, 0, 0.25, 0, 0, 0, 0, 0.025, 0, 0, 0]

                    for _ in range(int(options[1][1][options[1][2]])):
                        if randomise > 0:  # adds randomness to particle options
                            for idx, scale in enumerate(random_scale):
                                if scale > 0:
                                    cur_option = particle_options[idx]
                                    min_option = cur_option - randomise * scale
                                    max_option = cur_option + randomise * scale
                                    new_option = random.randint(int(min(min_option, max_option) * 10),
                                                                int(max(min_option, max_option) * 10)) / 10
                                    particle_options[idx] = new_option

                        particles.append(Particle(mouse_pos[0],
                                                  mouse_pos[1],
                                                  particle_options[0],
                                                  particle_options[1],
                                                  particle_options[2],
                                                  particle_options[3],
                                                  particle_options[4],
                                                  particle_options[5],
                                                  particle_options[6],
                                                  particle_options[7],
                                                  particle_options[8],
                                                  particle_options[9],
                                                  particle_options[10],
                                                  particle_options[11],
                                                  particle_options[12],
                                                  particle_options[13]))

        tile_colour = convert_colour(options[19][1][options[19][2]], False)
        border = options[21][1][options[21][2]]
        for tile in range(int(screen_height / tile_size)):  # draws left and right border
            if border == 'Left' or border == 'L+R' or border == 'All':
                tile_map['0;' + str(tile)] = [0, tile, tile_colour]
            if border == 'Right' or border == 'L+R' or border == 'All':
                tile_map[str(int(screen_width / tile_size) - 1) + ';' + str(tile)] = \
                    [int(screen_width / tile_size) - 1, tile, tile_colour]
        for tile in range(int(screen_width / tile_size)):  # draws top and bottom border
            if border == 'Top' or border == 'T+B' or border == 'All':
                tile_map[str(tile) + ';0'] = [tile, 0, tile_colour]
            if border == 'Bottom' or border == 'T+B' or border == 'All':
                tile_map[str(tile) + ';' + str(int(screen_height / tile_size) - 1)] = \
                    [tile, int(screen_height / tile_size) - 1, tile_colour]

        orbit_centre = convert_orbit(options[14][1][options[14][2]])
        draw_screen(particles, tile_map, new_tile, remove_tile, button_collide, show_options, orbit_centre)
        clock.tick(fps)


def convert_colour(string, randomise=True):  # convert colour string to rgb value
    if string == 'White':
        if randomise:
            pigment = random.randint(150, 255)
            value = (pigment, pigment, pigment)
        else:
            value = (230, 230, 230)
    elif string == 'Black':
        if randomise:
            pigment = random.randint(0, 50)
            value = (pigment, pigment, pigment)
        else:
            value = (25, 25, 25)
    elif string == 'Red':
        if randomise:
            pigment = random.randint(50, 200)
            value = (pigment, 0, 0)
        else:
            value = (150, 0, 0)
    elif string == 'Green':
        if randomise:
            pigment = random.randint(50, 200)
            value = (0, pigment, 0)
        else:
            value = (0, 150, 0)
    elif string == 'Blue':
        if randomise:
            pigment = random.randint(50, 200)
            value = (0, 0, pigment)
        else:
            value = (0, 0, 150)
    elif string == 'Yellow':
        if randomise:
            pigment = random.randint(100, 255)
            value = (pigment, pigment, 0)
        else:
            value = (150, 150, 0)
    elif string == 'Purple':
        if randomise:
            pigment = random.randint(100, 255)
            value = (pigment - 75, 0, pigment)
        else:
            value = (100, 0, 150)
    elif string == 'Orange':
        if randomise:
            pigment = random.randint(100, 255)
            value = (pigment, pigment // 2, 0)
        else:
            value = (150, 75, 0)
    elif string == 'Teal':
        if randomise:
            pigment = random.randint(100, 255)
            value = (0, pigment, pigment - 50)
        else:
            value = (0, 150, 120)
    elif string == 'Pink':
        if randomise:
            pigment = random.randint(100, 255)
            value = (pigment, 0, pigment // 2)
        else:
            value = (150, 0, 75)
    elif string == 'Random':
        if randomise:
            value = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            value = (230, 230, 230)
    else:
        value = (230, 230, 230)
    return value


def convert_glow_colour(string):  # add more glow colours, add age counter and death check
    if string == 'White':
        value = (20, 20, 20)
    elif string == 'Red':
        value = (60, 0, 0)
    elif string == 'Green':
        value = (0, 60, 0)
    elif string == 'Blue':
        value = (0, 0, 60)
    elif string == 'Yellow':
        value = (60, 60, 0)
    elif string == 'Purple':
        value = (30, 0, 60)
    elif string == 'Orange':
        value = (60, 30, 0)
    elif string == 'Pink':
        value = (60, 0, 30)
    elif string == 'Teal':
        value = (0, 60, 30)
    elif string == 'Random':
        value = (random.randint(0, 60), random.randint(0, 60), random.randint(0, 60))
    else:
        value = (20, 20, 20)
    return value


def convert_death_time(string):
    if string == 'Never':
        value = -1
    else:
        value = int(string)
    return value


def convert_orbit(string):
    if string == 'None':
        value = None
    elif string == 'Centre':
        value = [int(screen_width / 2), int(screen_height / 2)]
    elif string == 'Top Left':
        value = [tile_size * 5, tile_size * 5]
    elif string == 'Top Right':
        value = [screen_width - tile_size * 5, tile_size * 5]
    elif string == 'Bottom Left':
        value = [tile_size * 5, screen_height - tile_size * 5]
    elif string == 'Bottom Right':
        value = [screen_width - tile_size * 5, screen_height - tile_size * 5]
    else:
        value = None
    return value


def draw_screen(particles, tile_map, new_tile, remove_tile, button_collide, show_options, orbit_centre):  # draws screen
    screen.fill(convert_colour(options[18][1][options[18][2]], False))
    draw_tiles(tile_map, new_tile, remove_tile)
    if show_options:
        draw_options(button_collide)
    draw_particles(particles, tile_map)
    if options[22][1][options[22][2]] == 'True' and options[14][1][options[14][2]] != 'None':
        draw_sun(orbit_centre)
    pg.display.update()


def draw_tiles(tile_map, new_tile, remove_tile):  # draw tiles
    for tile in tile_map:
        pg.draw.rect(screen, tile_map[tile][2], pg.Rect(tile_map[tile][0] * tile_size,
                                                        tile_map[tile][1] * tile_size, tile_size, tile_size))
    for tile in new_tile:
        pg.draw.rect(screen, new_tile[tile][2], pg.Rect(new_tile[tile][0] * tile_size,
                                                        new_tile[tile][1] * tile_size, tile_size, tile_size))
    for tile in remove_tile:
        pg.draw.rect(screen, remove_tile[tile][2], pg.Rect(remove_tile[tile][0] * tile_size,
                                                           remove_tile[tile][1] * tile_size, tile_size, tile_size))


def draw_options(button_collide):
    text_colour = convert_colour(options[20][1][options[20][2]], False)
    vertical_counter = tile_size * -1
    for index in range(len(options)):
        if options[index][2] != -1:
            vertical_counter += tile_size * 2
            temp_text_1 = options_font.render(options[index][0], True, text_colour)
            temp_text_2 = options_font.render(options[index][1][options[index][2]], True, text_colour)
            temp_button = pg.Rect(tile_size * 2 + temp_text_1.get_width(), vertical_counter,
                                  temp_text_2.get_width() + tile_size, temp_text_2.get_height() + int(tile_size / 4))
            buttons[index] = ([temp_text_1, temp_text_2, temp_button, vertical_counter])
        else:
            vertical_counter += tile_size * 3
            temp_text_1 = options_font.render(options[index][0], True, text_colour)
            buttons[index] = ([temp_text_1, vertical_counter])
    for index, button in enumerate(buttons):
        if options[index][2] != -1:
            screen.blit(button[0], (tile_size * 2, button[3]))
            screen.blit(button[1], (tile_size * 2 + button[0].get_width() + int(tile_size / 2),
                                    button[3] + int(tile_size / 8)))
            pg.draw.rect(screen, text_colour, button[2], 1 + button_collide[index])
        else:
            screen.blit(button[0], (tile_size * 2, button[1]))


def draw_sun(position):  # draws centre of orbit
    pg.draw.circle(screen, (201, 79, 8), position, 10)


class Particle:  # particle control
    def __init__(self, x_pos, y_pos, x_vel, y_vel, x_acc, y_acc, colour, size, shrink, glow, glow_colour, physics,
                 bounce, orbit=None, pull=None, death=-1):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.colour = colour
        self.size = size
        self.shrink = shrink
        self.glow = glow
        self.glow_colour = glow_colour
        self.physics = physics
        self.bounce = bounce
        self.orbit = orbit
        self.pull = pull
        self.age = 0
        self.death = death

    def draw(self, tile_map):
        if self.glow:
            glow_radius = self.size * 1.5
            screen.blit(glow_surface(glow_radius, self.glow_colour),
                        (int(self.x_pos - glow_radius + 1), int(self.y_pos - glow_radius + 1)),
                        special_flags=BLEND_RGB_ADD)  # draws glow effect around particle
        pg.draw.circle(screen, self.colour, (int(self.x_pos), int(self.y_pos)), int(self.size))  # draw particle
        self.update(tile_map)

    def update(self, tile_map):
        self.x_pos += self.x_vel  # x position + velocity
        if self.physics:
            loc_str = str(int(self.x_pos / tile_size)) + ';' + str(int(self.y_pos / tile_size))  # current location
            if loc_str in tile_map:  # if particle colliding with tile
                self.x_vel *= -self.bounce  # x velocity * - bounce
                self.x_pos += self.x_vel * 2  # x position - 2 * velocity
        self.y_pos += self.y_vel  # y position + velocity
        if self.physics:
            loc_str = str(int(self.x_pos / tile_size)) + ';' + str(int(self.y_pos / tile_size))  # current location
            if loc_str in tile_map:  # if particle colliding with tile
                self.y_vel *= -self.bounce  # y velocity * - bounce
                self.y_pos += self.y_vel * 2  # y position - 2 * velocity
        self.x_vel += self.x_acc  # x velocity + acceleration
        self.y_vel += self.y_acc  # y velocity + acceleration
        if self.orbit:  # if centre of orbit given
            # distance from particle to centre of orbit
            difference = [self.orbit[0] - self.x_pos, self.orbit[1] - self.y_pos]
            # adds particle acceleration towards centre of orbit
            self.x_acc += (difference[0] * self.pull) / (screen_width * 2000)
            self.y_acc += (difference[1] * self.pull) / (screen_height * 2000)
            # limits particle acceleration
            if self.x_acc > 0.5:
                self.x_acc = 0.5
            elif self.x_acc < -0.5:
                self.x_acc = -0.5
            if self.y_acc > 0.5:
                self.y_acc = 0.5
            elif self.y_acc < -0.5:
                self.y_acc = -0.5
        self.size -= self.shrink  # adjust particle size
        self.age += 1  # increments age


def draw_particles(particles, tile_map):  # draws particles
    for _, particle in sorted(enumerate(particles), reverse=True):
        if particle.size <= 0 or not (-screen_width <= particle.x_pos <= screen_width * 2) \
                or not (-screen_height <= particle.y_pos <= screen_height * 2) \
                or (str(int(particle.x_pos / tile_size)) + ';' + str(int(particle.y_pos / tile_size)) in tile_map
                    and particle.physics) or particle.age / fps == particle.death:
            particles.remove(particle)  # remove particle if too small, too far off screen, in tile, or too old
        else:
            particle.draw(tile_map)  # draw particle


def glow_surface(radius, colour):
    radius = int(radius)
    surface = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(surface, colour, (radius, radius), radius)
    surface.set_colorkey((0, 0, 0))
    return surface


def start_up():  # start up screen
    global screen, screen_width, screen_height, fullscreen
    controls_text = ['Welcome to the particle test chamber', ' ', 'Click and drag LMB to draw tile',
                     'Click and drag MMB to remove tile', 'Press O to toggle options',
                     'Press F to toggle full screen', 'Press SPACE to skip intro', 'Press ESC to quit']
    colour_ini = (25, 25, 25)  # initial text colour
    colour_end = (230, 230, 230)  # end text colour
    colour = colour_ini
    colour_update = 40
    dt = 0
    title_counter = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                keys_pressed = pg.key.get_pressed()
                if keys_pressed[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
                if keys_pressed[pg.K_f]:
                    fullscreen = not fullscreen  # toggles full screen
                    if fullscreen:
                        screen_width, screen_height = monitor_width, monitor_height
                        screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)
                    else:
                        screen_width, screen_height = screen_width_small, screen_height_small
                        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (
                            int(pg.display.Info().current_w - screen_width) / 2,
                            int(pg.display.Info().current_h - screen_height) / 3)  # screen position
                        screen = pg.display.set_mode((screen_width, screen_height))
                if keys_pressed[pg.K_SPACE]:
                    main()

        screen.fill(colour_ini)
        for index, string in enumerate(controls_text):
            text = options_font.render(string, True, colour)
            screen.blit(text, (int((screen_width - text.get_width()) / 2),
                               int(screen_height / 3) + index * text.get_height()))
        pg.display.update()
        dt += clock.tick(fps)
        if dt > colour_update and colour != colour_end:
            colour = (colour[0] + 1, colour[1] + 1, colour[2] + 1)
            dt = 0
        if colour == colour_end:
            title_counter += 1
            if title_counter > fps * 3:
                main()


start_up()
