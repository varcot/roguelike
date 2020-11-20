import pygame

pygame.init()

# GLOBALS
# extended color palette imported from pico-8
white = (255, 241, 232)  # FFF1E8
black = (0, 0, 0)  # 000000
brown = (171, 82, 54)  # AB5236
darkgrey = (95, 87, 79)  # 5F574F
litegrey = (194, 195, 199)  # C2C3C7
red = (255, 0, 77)  # FF004D
orange = (255, 163, 0)  # FFA300
yellow = (255, 236, 39)  # FFEC27
green = (0, 228, 54)  # 00E436
darkgreen = (0, 135, 81)  # 008751
blue = (41, 173, 255)  # 29ADFF
indigo = (131, 118, 156)  # 83769C
darkblue = (29, 43, 83)  # 1D2B53
darkpurp = (126, 37, 83)  # 7E2553
pink = (255, 119, 168)  # FF77A8
peach = (255, 204, 170)  # FFCCAA
# extended colors below, making up names(please excuse)
offblack = (41, 24, 20)  # 291814
darkerblue = (17, 29, 53)  # 111D35
darkerpurp = (66, 33, 54)  # 422136
bluegreen = (18, 83, 89)  # 125359
redbrown = (116, 47, 41)  # 742F29
offdarkgrey = (73, 51, 59)  # 49333B
offlitegrey = (162, 136, 121)  # A28879
altyellow = (243, 239, 125)  # F3EF7D
altred = (190, 18, 80)  # BE1250
altorange = (255, 108, 36)  # FF6C24
limegreen = (168, 231, 46)  # A8E72E
altgreen = (0, 181, 67)  # 00B543
altblue = (6, 90, 181)  # 065AB5
mauve = (117, 70, 101)  # 754665
darkpeach = (255, 110, 89)  # FF6E59
litepeach = (255, 157, 129)  # FF9D81

# window size and various variables
map_offset = 100
windx = 1200
windy = 600
fps = 60  # self explanatory
fov_algo = 0
fov_light = True
torch_radius = 3
#fonts and messages
font_basic = pygame.font.SysFont("Georgia", 12)
num_messages = 4

# Map variables
map_width = 30
map_height = 15
cell_width = 32
cell_height = 32
room_max_size = 8
room_min_size = 3
max_rooms = 6
max_enemies_room = 5

S_PLAYER = pygame.image.load("main_character_rog/newman.png")
S_ZOMBO = pygame.image.load("enemies/zomboman/zomboman.png")
S_WALL = pygame.image.load("tilework/wall.png")
S_FLOOR = pygame.image.load("tilework/floor.png")
S_DARK_WALL = pygame.image.load("tilework/darkwall.png")
S_DARK_FLOOR = pygame.image.load("tilework/darkfloor.png")
S_LIT_FLOOR = pygame.image.load("tilework/litfloor.png")
S_CORPSE = pygame.image.load("tilework/corpse.png")

S_LIFE = pygame.image.load("tilework/heart.png")
