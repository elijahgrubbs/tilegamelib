
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


FRUITMAP = """##########
#b.#...aa#
##.#.#####
#h.#.e#.c#
##.#.##.##
##a#.#f..#
#*..b..#g#
##########"""


FIGURE_COLORS = {
    RED: 'b.pac_up',
    BLUE: 'b.pac_down',
    YELLOW: 'b.pac_left',
    PURPLE: 'b.ghost',
    GREEN: 'b.tail',
    ORANGE: 'b.dot'
}


class CollectFruit:

    def __init__(self, screen):
        self.screen = screen
        self.frame = Frame(self.screen, Rect(64, 64, 320, 320))
        self.tile_factory = TileFactory('data/tiles.conf')
        self.tm = TiledMap(self.frame, self.tile_factory)
        self.player = Sprite(self.frame, self.tile_factory.get('b.pac_right'),
                             Vector(4, 1), speed=2)
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
        if near == '#':
            return
        self.player.add_move(direction)
        wait_for_move(self.player, self.screen, self.draw, 0.01)
        self.check_player_square()

    def set_color(self, color):
        self.player.tile = self.tile_factory.get(FIGURE_COLORS[color])

    def check_player_square(self):
        field = self.tm.at(self.player.pos)
        if field == '*':
            time.sleep(1)
            self.events.exit_signalled()
        elif field in 'abcdefgh':
            self.score += 100
            self.tm.set_tile(self.player.pos, '.')
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
    game = Game('data/collect_fruit.conf', CollectFruit)
    game.run()
