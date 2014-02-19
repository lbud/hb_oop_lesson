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

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Key(GameElement):
    IMAGE = "Key"

    def interact(self, player):
        if not player.inventory.get("key"):
            player.inventory["key"] = 1
        else:
            player.inventory["key"] += 1
        GAME_BOARD.draw_msg("You found a key! Rad. This will probably come in handy sometime.")
        print player.inventory

class DoorOpen(GameElement):
    IMAGE = "DoorOpen"
    SOLID = True

    def interact(self, player):
        pass

class DoorClosed(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        # pass
        if player.inventory.get("key"):
            GAME_BOARD.draw_msg("Opened the door! Let's go!")
            open_door(self.x, self.y)
        else:
            GAME_BOARD.draw_msg("Hm, this seems to be locked...")

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        if not player.inventory.get("gem"):
            player.inventory["gem"] = 1
        else:
            player.inventory["gem"] += 1
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d gems!" % player.inventory["gem"])
        if player.inventory.get("gem") == 4:
            key_appears(2, 1)
            GAME_BOARD.draw_msg("Hey, look, a key appeared!")


class Character(GameElement):
    IMAGE = "Cat"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

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

def open_door(doorx, doory):
    opendoor = DoorOpen()
    GAME_BOARD.register(opendoor)
    GAME_BOARD.set_el(doorx, doory, opendoor)

def key_appears(keyx, keyy):
    key1 = Key()
    GAME_BOARD.register(key1)
    GAME_BOARD.set_el(keyx, keyy, key1)


def initialize():
    """Put game initialization code here"""
    rock_positions = [
            
        ]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    wall_positions = [
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
        ]
    walls = []

    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        walls.append(wall)

    gem_positions = [
            (0, 6),
            (7, 2),
            (7, 6),
            (9, 2),
        ]

    for pos in gem_positions:
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)

    doorclosed = DoorClosed()
    GAME_BOARD.register(doorclosed)
    GAME_BOARD.set_el(10, 1, doorclosed)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(10, 5, PLAYER)
    print PLAYER


    GAME_BOARD.draw_msg("This game is wicked awesome.")