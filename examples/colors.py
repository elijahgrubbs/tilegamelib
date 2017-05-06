
from tilegamelib import Frame, Vector, TileFactory, TiledMap
from tilegamelib import EventGenerator, ExitListener, FigureMoveListener, FigureColorListener
from tilegamelib.sprites import Sprite
from tilegamelib.draw_timer import draw_timer
from tilegamelib.move import wait_for_move
from tilegamelib.game import Game
from tilegamelib.vector import RED, BLUE, YELLOW, PURPLE, GREEN, ORANGE, LEFT, RIGHT, UP, DOWN
from pygame import Rect
import pygame
import time
import random
import levels

pygame.init()
pygame.mixer.music.load("music/shootingstars.ogg")

FRUITMAP = levels.getlevel(6)


FIGURE_COLORS = {
    RED: 'p_red_d',
    BLUE: 'p_blue_d',
    YELLOW: 'p_yellow_d',
    PURPLE: 'p_purple_d',
    GREEN: 'p_green_d',
    ORANGE: 'p_orange_d'
}

GHOST_TILE = 'b.ghost'

GHOST_POSITIONS = levels.ghostpos(6)
PLAYER_POSISTION = levels.playerpos(6)

class Colors:

    def __init__(self, screen):
        self.screen = screen
        self.level = None
        self.ghosts = []
        self.frame = Frame(self.screen, Rect(32, 32, 720, 720))
        self.tile_factory = TileFactory('data/colortiles.conf')
        self.tm = TiledMap(self.frame, self.tile_factory)
        self.level = ColorsLevel(FRUITMAP, self.tm)
        self.player = Sprite(self.frame, self.tile_factory.get('p_purple_d'),
                             PLAYER_POSISTION, speed=3)

        self.create_ghosts()
        self.tm.set_map(FRUITMAP)
        self.draw()
        self.events = None
        self.score = 0



    def draw(self):
        self.tm.draw()
        self.player.draw()
        for g in self.ghosts:
            g.update()
            g.draw()
        pygame.display.update()

    def move(self, direction):
        nearpos = self.player.pos + direction
        near = self.tm.at(nearpos)
        if near == 'r':
            if self.player.tile != self.tile_factory.get(FIGURE_COLORS[RED]):
                return # Currently makes it so player can't move unless changed to RED player sprite
        if near == 'b':
            if self.player.tile != self.tile_factory.get(FIGURE_COLORS[BLUE]):
                return # Currently makes it so player can't move unless changed to BLUE player sprite
        if near == 'y':
            if self.player.tile != self.tile_factory.get(FIGURE_COLORS[YELLOW]):
                return # Currently makes it so player can't move unless changed to YELLOW player sprite
        if near == 'p':
            if self.player.tile != self.tile_factory.get(FIGURE_COLORS[PURPLE]):
                return # Currently makes it so player can't move unless changed to PURPLE player sprite
        if near == 'g':
            if self.player.tile != self.tile_factory.get(FIGURE_COLORS[GREEN]):
                return # Currently makes it so player can't move unless changed to GREEN player sprite
        if near == 'o':
            if self.player.tile != self.tile_factory.get(FIGURE_COLORS[ORANGE]):
                return # Currently makes it so player can't move unless changed to ORANGE player sprite
        if near == '#':
            return
        self.player.add_move(direction)
        wait_for_move(self.player, self.screen, self.draw, 0.01)
        self.check_player_square()

    def set_color(self, color):
        self.player.tile = self.tile_factory.get(FIGURE_COLORS[color])

    def check_player_square(self):
        field = self.tm.at(self.player.pos)
        if field in '123456':
            time.sleep(1)
            self.events.exit_signalled()
        elif field == 's':
            self.score += 100
            self.tm.set_tile(self.player.pos, 'w')
            self.tm.cache_map()
            self.draw()

    def run(self):
        pygame.mixer.music.play(-1)
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.move))
        self.events.add_listener(FigureColorListener(self.set_color))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()

    def create_ghosts(self):
        self.ghosts = []
        for pos in GHOST_POSITIONS:
            self.ghosts.append(Ghost(self.frame, self.tile_factory,
                               pos, self.level))


class Ghost:

    def __init__(self, frame, tile_factory, pos, level):
        tile = tile_factory.get(GHOST_TILE)
        self.sprite = Sprite(frame, tile, pos, speed=2)
        self.level = level
        self.direction = None
        self.set_random_direction()

    def get_possible_moves(self):
        result = []
        directions = [LEFT, RIGHT, UP, DOWN]
        for vector in directions:
            if vector * -1 != self.direction:
                newpos = self.sprite.pos + vector
                tile = self.level.at(newpos)
                if tile != '#':
                    result.append(vector)
        if not result:
            result = [self.direction * (-1)]
        return result

    def set_random_direction(self):
        moves = self.get_possible_moves()
        i = random.randint(0, len(moves) - 1)
        self.direction = moves[i]

    def move(self):
        if self.sprite.finished:
            self.set_random_direction()
            self.sprite.add_move(self.direction)
        else:
            self.sprite.move()

    def update(self):
        self.move()

    def draw(self):
        self.sprite.draw()


class ColorsLevel:

    def __init__(self, data, tmap):
        self.tmap = tmap
        self.tmap.set_map(str(data))
        self.tmap.cache_map()
        self.souls_left = 0

    def at(self, pos):
        return self.tmap.at(pos)

    def remove_soul(self, pos):
        tile = self.at(pos)
        # if tile != '.':
        #     self.tmap.set_tile(pos, '.')
        #     self.tmap.cache_map()
        #     if tile == '*':
        #         self.souls_left -= 1

    def draw(self):
        self.tmap.draw()

if __name__ == '__main__':
    game = Game('data/colors.conf', Colors) #Change to data/colors.conf after creating title screen
    game.run()
