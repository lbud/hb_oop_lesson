import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 12
GAME_HEIGHT = 7
LEVEL = 1

###########################
#### CLASS DEFINITIONS ####
###########################

#### Parent Class: solid things

class SolidThings(GameElement):
    SOLID = True


class Rock(SolidThings):
    IMAGE = "Rock"


class Wall(SolidThings):
    IMAGE = "Wall"


class DoorClosed(SolidThings):
    IMAGE = "DoorClosed"

    def interact(self, player):
        for i in player.inventory:
            if i.name == "key":
                print "have the key"
                GAME_BOARD.draw_msg("Opened the door! Let's go!")
                open_door(self.x, self.y)
            else:
                GAME_BOARD.draw_msg("Hm, this seems to be locked...")


class DoorOpen(SolidThings):
    IMAGE = "DoorOpen"

    def interact(self, player):
        nextlevel = True
        GAME_BOARD.draw_msg("I'm trying to go to the next level helllllp")
        initializenext()




#### Parent class: collectible things

class Collectible(GameElement):
    SOLID = False
    def __init__(self, name, collect_message):
        self.name = name
        self.collect_message = collect_message

        super(Collectible, self).__init__()

    def __repr__(self):
        return self.name

    def check_inventory(self, player):
        howmanygems = 0
        print "Inventory:"
        for i in player.inventory:
            print i.name
            if i.name == "gem":
                howmanygems += 1
            if howmanygems == 4:
                key_appears(2,1)
                GAME_BOARD.draw_msg("Hey, look, a key appeared!")

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You found a %s! Rad. %s" % (self.name, self.collect_message))
        self.check_inventory(player)


class Key(Collectible):
    def __init__(self):
        super(Key, self).__init__("key", "This will probably come in handy sometime.")
    IMAGE = "Key"


class Gem(Collectible):
    IMAGE = "BlueGem"
    def __init__(self):
        super(Gem, self).__init__("gem", "Are there any more around here?")


#### player

class Character(GameElement):
    IMAGE = "Cat"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None







####   End class definitions    ####
####   mini-functions:          ####

def open_door(doorx, doory):
    opendoor = DoorOpen()
    GAME_BOARD.register(opendoor)
    GAME_BOARD.set_el(doorx, doory, opendoor)

def key_appears(keyx, keyy):
    key1 = Key()
    GAME_BOARD.register(key1)
    GAME_BOARD.set_el(keyx, keyy, key1)






####   End mini-functions       ####
####   Level setup:             ####

level_1 = {
    "wall_positions": [
            (0, 5),
            (1, 0),
            (1, 1),
            (1, 3),
            (1, 5),
            (2, 0),
            (2, 3),
            (2, 5),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 5),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 5),
            (5, 6),
            (6, 5),
            (7, 1),
            (7, 5),
            (8, 1),
            (8, 2),
            (8, 3),
            (8, 4),
            (8, 5),
            (9, 1),
            (9, 3),
            (9, 4)
        ],
    "gem_positions": [
            (0, 6),
            (7, 2),
            (7, 6),
            (9, 2)            
        ],
    "door_positions": [
            (10, 1)
        ]
    }

level_2 = {
    "wall_positions": [
        ],
    "gem_positions": [
        ],
    "door_positions": [
        ]
    }   



####   End level setup          ####
####   keyboard handler:        ####


def keyboard_handler():
    direction = None
    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        print "next x: ", next_x
        next_y = next_location[1]
        print "next y: ", next_y

        if next_x in range(0, GAME_WIDTH) and next_y in range(0, GAME_HEIGHT):
            on_board = True
        else:
            on_board = False

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if (existing_el is None or not existing_el.SOLID) and on_board:

            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)



def initialize(level):

    for pos in level.get("wall_positions"):
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)

    for pos in level.get("gem_positions"):
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)

    for pos in level.get("door_positions"):
        doorclosed = DoorClosed()
        GAME_BOARD.register(doorclosed)
        GAME_BOARD.set_el(pos[0], pos[1], doorclosed)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(10, 5, PLAYER)
    print PLAYER


    GAME_BOARD.draw_msg("This game is wicked awesome.")


def initializenext():
    for y in range(GAME_HEIGHT):
        for x in range(GAME_WIDTH):
            if GAME_BOARD.get_el(x, y):
                GAME_BOARD.del_el(x, y)
    initialize(level_2)