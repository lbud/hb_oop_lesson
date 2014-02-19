import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import string

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 12
GAME_HEIGHT = 7

######################

f1 = open("level1.txt")
l1 = [line.strip('\n') for line in f1.readlines()]


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
        GAME_BOARD.draw_msg("On to da next one")
        initializesecond()


class TallTree(SolidThings):
    IMAGE = "TallTree"


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
####   boardmaking functions:   ####

def get_level(filename):
    f = open(filename)
    return [string.upper(line.strip('\n')) for line in f.readlines()]
    f.close()

def make_level(level):
    gamesetup = {"wall_positions": [], "gem_positions": [], "door_positions": [], "open_door_positions": [], "tree_positions": [], "player_position": []}
    lineno = 0
    for line in level:
        charno = 0
        for char in line:
            if char == "#":
                pass
            elif char == "W":
                gamesetup.get("wall_positions").append((charno, lineno))
            elif char == "G":
                gamesetup.get("gem_positions").append((charno, lineno))
            elif char == "P":
                gamesetup.get("player_position").append((charno, lineno))
            elif char == "D":
                gamesetup.get("door_positions").append((charno, lineno))
            elif char == "O":
                gamesetup.get("open_door_positions").append((charno, lineno))
            elif char == "T":
                gamesetup.get("tree_positions").append((charno, lineno))
            charno += 1
        lineno += 1
    return gamesetup

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

l1 = get_level("level1.txt")
level_1 = make_level(l1)

l2 = get_level("level2.txt")
level_2 = make_level(l2)




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

    for pos in level.get("open_door_positions"):
        dooropen = DoorOpen()
        GAME_BOARD.register(dooropen)
        GAME_BOARD.set_el(pos[0], pos[1], dooropen)

    for pos in level.get("tree_positions"):
        talltree = TallTree()
        GAME_BOARD.register(talltree)
        GAME_BOARD.set_el(pos[0], pos[1], talltree)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(level.get("player_position")[0][0], level.get("player_position")[0][1], PLAYER)
    print PLAYER

def initializesecond():
    for y in range(GAME_HEIGHT):
        for x in range(GAME_WIDTH):
            if GAME_BOARD.get_el(x, y):
                GAME_BOARD.del_el(x, y)
    initialize(level_2)
    current_level = 2
    print current_level
    return current_level