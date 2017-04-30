
from tilegamelib import Frame, Vector, TileFactory, TiledMap
from tilegamelib import EventGenerator, ExitListener, FigureMoveListener, FigureColorListener
from tilegamelib.sprites import Sprite
from tilegamelib.draw_timer import draw_timer
from tilegamelib.move import wait_for_move
from tilegamelib.game import Game
from tilegamelib.vector import RED, BLUE, YELLOW, PURPLE, GREEN, ORANGE
from pygame import Rect
import pygame
import time


FRUITMAP = """####################
####################
####################
#bs#################
#y##################
#pgbry5#############
#o##g###############
#br#os##############
#igyp###############
####################"""


FIGURE_COLORS = {
    RED: 'b.pac_up',
    BLUE: 'b.pac_down',
    YELLOW: 'b.pac_left',
    PURPLE: 'b.ghost',
    GREEN: 'b.tail',
    ORANGE: 'b.dot'
}


class Colors:

    def __init__(self, screen):
        self.screen = screen
        self.frame = Frame(self.screen, Rect(0, 30, 640, 640))
        self.tile_factory = TileFactory('data/colortiles.conf')
        self.tm = TiledMap(self.frame, self.tile_factory)
        self.player = Sprite(self.frame, self.tile_factory.get('b.pac_right'),
                             Vector(1, 8), speed=3)
        self.tm.set_map(FRUITMAP)
        self.draw()
        self.events = None
        self.score = 0

    def draw(self):
        self.tm.draw()
        self.player.draw()
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
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.move))
        self.events.add_listener(FigureColorListener(self.set_color))
        self.events.add_listener(ExitListener(self.events.exit_signalled))
        with draw_timer(self, self.events):
            self.events.event_loop()


if __name__ == '__main__':
    game = Game('data/colors.conf', Colors) #Change to data/colors.conf after creating title screen
    game.run()
