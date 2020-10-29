import tcod
import pygame
import constants
import math
import random

GAMEDISPLAY = None


# Tile Structure, inanimate objects in General
class Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False


class Asset:
    pass


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersect(self, other):
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1


# Game Object Class, unused for now!!
class Game:
    def __init__(self):
        self.curr_map = map_create()
        self.curr_objs = []
        self.history = []


# Base Object Entity, animate or interactive objects such as player or enemies or items, etc
class Entity:
    def __init__(self, x, y, ani, blocks=False, creature=None, ai=None):
        self.x = x
        self.y = y
        self.blocks = blocks  # Indicates whether this entity is capable of blocking other objects on its tile
        self.facing = 0       # The direction this entity faces
        self.offx = 0
        self.offy = 0
        self.ani = ani
        # self.framerate = .1
        # self.frame_timer = 0
        # self.frame_index = 0
        self.creature = creature
        if creature:
            self.creature.owner = self
        self.ai = ai
        if ai:
            self.ai.owner = self

    def update_offsets(self):
        if self.offx > 0:
            self.offx -= 4
        if self.offx < 0:
            self.offx += 4
        if self.offy > 0:
            self.offy -= 4
        if self.offy < 0:
            self.offy += 4

    def draw(self):
        is_visible = FOV.fov[self.y][self.x]
        if is_visible:
            self.update_offsets()
            if len(self.ani) == 1:
                GAMEDISPLAY.blit(self.ani[0], (
                    self.x * constants.cell_width + self.offx, self.y * constants.cell_height + self.offy))
            elif len(self.ani) > 1:
                # self.frame_timer += CLOCK.get_time()
                # if self.frame_timer > (self.framerate * 1000):
                # self.frame_timer = 0
                # self.frame_index = (self.frame_index + 1) % len(self.ani)
                # GAMEDISPLAY.blit(self.ani[math.floor(T >> 3) % len(self.ani)],
                # (self.x * constants.cell_width, self.y * constants.cell_height))
                GAMEDISPLAY.blit(self.ani[math.floor(T >> 3) % len(self.ani)],
                                 (
                                     self.x * constants.cell_width + self.offx,
                                     self.y * constants.cell_height + self.offy))

    def flip(self):
        for i in range(len(self.ani)):
            self.ani[i] = pygame.transform.flip(self.ani[i], True, False)
        self.facing = not self.facing


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file)
        self.ani_list = []

    def get_image(self, col, row, width, height, scale=None):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sheet, (0, 0), (col * width, row * height, width, height))
        # image.set_colorkey(constants.black)
        if scale:
            (neww, newh) = scale
            image = pygame.transform.scale(image, (neww, newh))
        self.ani_list.append(image)
        return self.ani_list

    def get_ani(self, col, row, width, height, length, scale=None):
        for i in range(length):
            image = pygame.Surface([width, height]).convert()
            image.blit(self.sheet, (0, 0), (col * width + (width * i), row * height, width, height))
            # image.set_colorkey(constants.black)
            if scale:
                (neww, newh) = scale
                image = pygame.transform.scale(image, (neww, newh))
            self.ani_list.append(image)
        return self.ani_list


##    def __init__(self, file, cols, rows):
##        self.sheet = pygame.image.load(file)
##        self.cols = cols
##        self.rows = rows
##        self.cellCount = cols * rows
##        self.rect = self.sheet.get_rect()
##        w = self.cellwidth = self.rect.width / cols
##        h = self.cellheight = self.rect.height / rows
##        hw, hh = self.cellcenter = (self.cellwidth / 2, self.cellheight / 2)
##        self.cells = list([(index % cols * w, index / cols * h, w, h) for index in range(self.cellCount)])
##        self.handle = list([(0, 0), (-hw, 0), (-w, 0), (0, -hh), (-hw, -hh), (-w, -hh), (0, -h), (-hw, -h), (-w, -h)])
##
##    def draw(self, surface, index, x, y, handle=0):
##        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[index])


# COMPONENTS
# Animate objects that can move, perform actions, die, be born etc
class Creature:
    def __init__(self, name, hp=5):
        self.name = name
        self.maxhp = hp
        self.hp = hp

    def move(self, dx, dy):
        # self.owner.offx = dx * -(constants.cell_width)
        # self.owner.offy = dy * -(constants.cell_height)
        walltile = (GAMEMAP[self.owner.x + dx][self.owner.y + dy].block_path == True)
        target = map_check(self.owner.x + dx, self.owner.y + dy, self.owner)
        if not walltile and not target:
            self.owner.offx = dx * -(constants.cell_width)
            self.owner.offy = dy * -(constants.cell_height)
            self.owner.x += dx
            self.owner.y += dy
        else:
            self.owner.offx = (dx * (constants.cell_width)) / 2
            self.owner.offy = (dy * (constants.cell_height)) / 2
            if target:
                self.attack(target, 1)

    def attack(self, target, damage):
        # print(self.name + " ATTACKS " + target.creature.name + " for " + str(damage) + " damagio")
        game_message(self.name + " ATTACKS " + target.creature.name + " for " + str(damage) + " damagio", constants.red)
        target.creature.damage(damage)

    def damage(self, damage):
        self.hp -= damage
        # print(self.name + " has had its hp reduced to " + str(self.hp) + "/" + str(self.maxhp))
        game_message(self.name + " has had its hp reduced to " + str(self.hp) + "/" + str(self.maxhp), constants.black)
        if self.hp <= 0:
            self.die()

    def die(self):
        # print(self.name + " is dead!!!! OH NOOOOO")
        game_message(self.name + " is dead!!!! OH NOOOOO", constants.altred)
        # die motherfucker die


class AI_test:
    def __init__(self):
        self.options = [-1, 1]
        self.finmove = [None, None]

    def turn(self):
        zeroplace = random.randint(0, 1)
        self.finmove[zeroplace] = 0
        self.finmove[not zeroplace] = random.choice(self.options)
        self.owner.creature.move(self.finmove[0], self.finmove[1])
        # self.owner.creature.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))

class AI_2:
    def __init__(self):
        self.options = [-1, 1]
        self.finmove = [None, None]

    def turn(self):
        zeroplace = random.randint(0, 1)
        self.finmove[zeroplace] = 0
        self.finmove[not zeroplace] = random.choice(self.options)
        self.owner.creature.move(self.finmove[0], self.finmove[1])


# Usable and interactive objects
class Item:
    pass


# A box that can hold things
class Container:
    pass


def create_room(room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            GAMEMAP[x][y].block_path = False


def space_blocked(x, y):
    if GAMEMAP[x][y].block_path:
        return True
    for obj in GAMEOBJS:
        if obj.blocks and obj.x == x and obj.y == y:
            return True
    return False


def populate_room(room):
    global GAMEOBJS
    num_enemies = random.randint(1, constants.max_enemies_room)
    for i in range(num_enemies):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        if not space_blocked(x, y):
            GAMEOBJS.append(Entity(x, y, S_ZOMBO, True, Creature("Zombo" + str(i)), AI_test()))


def create_h_tunnel(x1, x2, y):
    global GAMEMAP
    for x in range(min(x1, x2), max(x1, x2) + 1):
        GAMEMAP[x][y].block_path = False


def create_v_tunnel(y1, y2, x):
    global GAMEMAP
    for y in range(min(y1, y2), max(y1, y2) + 1):
        GAMEMAP[x][y].block_path = False


# Map creation function
def map_create():
    global GAMEMAP
    # rooms = []
    # num_rooms = 0
    GAMEMAP = [[Tile(True) for y in range(0, constants.map_height)] for x in range(0, constants.map_width)]
    room1 = Rect(0, 0, 8, 8)
    create_room(room1)
    populate_room(room1)
    # for r in range(constants.max_rooms):
    #     w = tcod.random_get_int(0,constants.room_min_size,constants.room_max_size)
    #     h = tcod.random_get_int(0,constants.room_min_size,constants.room_max_size)
    #     x = tcod.random_get_int(0,0,constants.map_width-w-1)
    #     y = tcod.random_get_int(0,0,constants.map_height-h-1)
    #     new_room = Rect(x,y,w,h)
    #     failed = False
    #     for other_room in rooms:
    #         if new_room.intersect(other_room):
    #             failed = True
    #             break
    #     if not failed:
    #         create_room(new_room)
    #         newx,newy = new_room.center()
    #         if num_rooms == 0:
    #             pass
    #         else:
    #             prevx,prevy = rooms[num_rooms-1].center()
    #             if tcod.random_get_int(0,0,1) == 1:
    #                 create_h_tunnel(prevx,newx,prevy)
    #                 create_v_tunnel(prevy,newy,newx)
    #             else:
    #                 create_v_tunnel(prevy,newy,prevx)
    #                 create_h_tunnel(prevx,newx,newy)
    #         rooms.append(new_room)
    #         num_rooms += 1
    for x in range(constants.map_width):
        GAMEMAP[x][0].block_path = True
        GAMEMAP[x][constants.map_height - 1].block_path = True
    for y in range(constants.map_height):
        GAMEMAP[0][y].block_path = True
        GAMEMAP[constants.map_width - 1][y].block_path = True
    map_make_fov(GAMEMAP)
    return GAMEMAP


def map_check(x, y, exclude=None):
    for obj in GAMEOBJS:
        if obj != exclude and obj.x == x and obj.y == y and obj.creature:
            return obj
    return None


def map_make_fov(map):
    global FOV
    # FOV = tcod.map_new(constants.map_width,constants.map_height)
    FOV = tcod.map.Map(constants.map_width, constants.map_height)
    for y in range(constants.map_height):
        for x in range(constants.map_width):
            FOV.transparent[y][x] = not map[x][y].block_path
            FOV.walkable[y][x] = not map[x][y].block_path
            # tcod.map_set_properties(FOV, x, y, not map[x][y].block_path, not map[x][y].block_path)


def map_calc_fov():
    global FOV_CALC
    # print(FOV_CALC)
    if FOV_CALC:
        FOV_CALC = False
        FOV.compute_fov(PLAYER.x, PLAYER.y, constants.torch_radius, constants.fov_light, tcod.FOV_BASIC)
        # tcod.map_compute_fov(FOV, PLAYER.x, PLAYER.y, constants.torch_radius, constants.fov_light,constants.fov_algo )


# Game Initialization
def initialize():
    global GAMEDISPLAY, GAMEMAP, PLAYER, ENEMY, GAMEOBJS, FOV_CALC, CLOCK, GAME_MSGS, T, S_ZOMBO, GAME_STATE
    pygame.init()
    CLOCK = pygame.time.Clock()

    GAMEDISPLAY = pygame.display.set_mode((constants.windx, constants.windy))
    GAME_STATE = 'Playing'
    T = 0
    pygame.display.set_caption('RogueLyke')
    clock = pygame.time.Clock()  # clock variable
    GAMEOBJS = []
    zombosheet = SpriteSheet("enemies/zomboman/zomboman.png")
    S_ZOMBO = zombosheet.get_image(0, 0, 32, 32)
    # crea2 = Creature("Zombie")
    # AI = AI_test()
    map_create()
    GAME_MSGS = []
    FOV_CALC = True
    # print(FOV_CALC)
    playersheet = SpriteSheet("main_character_rog/mainchar.png")
    # playersheet = SpriteSheet("main_character_rog/newman.png")
    # zombosheet = SpriteSheet("enemies/zomboman/zomboman.png")
    S_PLAYER = playersheet.get_ani(0, 0, 16, 16, 4, (32, 32))
    # S_PLAYER = playersheet.get_image(0, 0, 32, 32)
    # S_ZOMBO = zombosheet.get_image(0, 0, 32, 32)
    crea1 = Creature("Vasheel")
    # crea2 = Creature("Zombie")
    # AI = AI_test()
    PLAYER = Entity(2, 2, S_PLAYER, True, crea1)
    # ENEMY = Entity(8, 1, S_ZOMBO, crea2, AI)
    GAMEOBJS.append(PLAYER)


# General Game Drawing Function
def draw():
    global GAMEDISPLAY

    # clear the surface
    GAMEDISPLAY.fill(constants.black)
    # draw the map
    draw_map(GAMEMAP)
    # draw char
    # GAMEDISPLAY.blit(constants.S_PLAYER, (constants.cell_width, constants.cell_height))
    for x in GAMEOBJS:
        x.draw()
    draw_message()
    draw_debug()
    # update the display
    pygame.display.flip()


# Map Drawing Function
def draw_map(map):
    for x in range(0, constants.map_width):
        for y in range(0, constants.map_height):
            # is_visible = tcod.map_is_in_fov(FOV,x,y)
            is_visible = FOV.fov[y][x]
            if is_visible:
                if map[x][y].block_path:
                    GAMEDISPLAY.blit(constants.S_WALL, (
                        (x * constants.cell_width),
                        (y * constants.cell_height)))
                else:
                    GAMEDISPLAY.blit(constants.S_LIT_FLOOR, (
                        (x * constants.cell_width),
                        (y * constants.cell_height)))
                map[x][y].explored = True
            else:
                if map[x][y].explored:
                    if map[x][y].block_path:
                        GAMEDISPLAY.blit(constants.S_DARK_WALL, (
                            (x * constants.cell_width),
                            (y * constants.cell_height)))
                    else:
                        GAMEDISPLAY.blit(constants.S_DARK_FLOOR, (
                            (x * constants.cell_width),
                            (y * constants.cell_height)))


def draw_debug():
    draw_text(GAMEDISPLAY, "fps: " + str(round(CLOCK.get_fps(), 3)), (1100, 0), constants.altred, constants.white)


def draw_message():
    font_height = text_height(constants.font_basic)
    start = constants.map_height * constants.cell_height - (constants.num_messages * font_height)
    i = 0
    messages = GAME_MSGS[-constants.num_messages:]
    for i, x in enumerate(messages):
        draw_text(GAMEDISPLAY, x[0], (0, start + (i * font_height)), x[1], constants.white)


def draw_text(display, text, co_ords, color, bg=None):
    text_surf, text_rect = text_objs(text, color, bg)
    text_rect.topleft = co_ords
    display.blit(text_surf, text_rect)


def text_objs(text, color, bg):
    if bg:
        text_surf = constants.font_basic.render(text, True, color, bg)
    else:
        text_surf = constants.font_basic.render(text, True, color)
    return text_surf, text_surf.get_rect()


def text_height(font):
    fontobj = font.render("a", False, (0, 0, 0))
    font_rect = fontobj.get_rect()
    return font_rect.height


def game_message(message, color):
    GAME_MSGS.append((message, color))


def handle_input():
    global FOV_CALC
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "Quit"
        if event.type == pygame.KEYDOWN:
            if GAME_STATE == 'Playing':
                if event.key == pygame.K_LEFT:
                    PLAYER.creature.move(-1, 0)
                    FOV_CALC = True
                    if PLAYER.facing == 0:
                        PLAYER.flip()
                    return "Moved"
                if event.key == pygame.K_RIGHT:
                    PLAYER.creature.move(1, 0)
                    FOV_CALC = True
                    if PLAYER.facing == 1:
                        PLAYER.flip()
                    return "Moved"
                if event.key == pygame.K_UP:
                    PLAYER.creature.move(0, -1)
                    FOV_CALC = True
                    return "Moved"
                if event.key == pygame.K_DOWN:
                    PLAYER.creature.move(0, 1)
                    FOV_CALC = True
                    return "Moved"
                else:
                    return "Wait"
    return "None"


# Game Loop - Where the Magic happens
def gameLoop():
    global T
    gameExit = False
    out = "None"

    while not gameExit:
        out = handle_input()
        map_calc_fov()
        if out == "Quit":
            gameExit = True

        if out != "None":
            for x in GAMEOBJS:
                if x.ai:
                    x.ai.turn()
        draw()
        T += 1
        CLOCK.tick(constants.fps)

    pygame.quit()
    quit()


if __name__ == '__main__':
    initialize()
    gameLoop()
