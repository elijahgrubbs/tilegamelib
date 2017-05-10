
from tilegamelib import Frame, Vector, TileFactory, TiledMap
from tilegamelib import EventGenerator, ExitListener, FigureMoveListener, FigureColorListener
from tilegamelib.bar_display import BarDisplay
from tilegamelib.basic_boxes import DictBox
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
ccsound=pygame.mixer.Sound("music/colorchange.ogg")
damsound=pygame.mixer.Sound("music/damage.ogg")
deadsound=pygame.mixer.Sound("music/dead.ogg")
startsound=pygame.mixer.Sound("music/gamestart.ogg")
movesound=pygame.mixer.Sound("music/move.ogg")
souleatsound=pygame.mixer.Sound("music/souleat.ogg")

FIGURE_SPRITES = [
    ['p_red_u', 'p_red_d', 'p_red_l', 'p_red_r'],
    ['p_blue_u', 'p_blue_d', 'p_blue_l', 'p_blue_r'],
    ['p_yellow_u', 'p_yellow_d', 'p_yellow_l', 'p_yellow_r'],
    ['p_purple_u', 'p_purple_d', 'p_purple_l', 'p_purple_r'],
    ['p_green_u', 'p_green_d', 'p_green_l', 'p_green_r'],
    ['p_orange_u', 'p_orange_d', 'p_orange_l', 'p_orange_r']
]

GHOST_TILE = 'enemy_d'



class Colors:

    def __init__(self, screen):
        self.screen = screen
        self.frame = Frame(self.screen, Rect(32, 32, 720, 720))
        self.tile_factory = TileFactory('data/colortiles.conf')
        self.current_level = 4
        self.level_loader = levels
        self.score = 0

        self.level = None
        self.player = None
        self.events = None
        self.ghosts = []
        self.update_mode = None
        self.status_box = None

        self.create_level()
        self.create_player()
        self.create_ghosts()
        self.create_status_box()

        self.collided = False
        self.mode = None
        self.update_mode = self.update_ingame

    def create_level(self):
        tmap = TiledMap(self.frame, self.tile_factory)
        self.level = ColorsLevel(self.level_loader.getlevel(self.current_level), tmap, self.level_loader.getGhostSpeed(self.current_level))

    def draw(self):
        self.update_mode()
        self.level.draw()
        self.player.update()
        self.player.draw()
        for g in self.ghosts:
            g.update()
            g.draw()
        self.status_box.draw()
        pygame.display.update()
        self.check_collision(self.player.sprite.pos)
        time.sleep(0.005)

    def create_player(self):
        self.player = Player(self.frame, self.tile_factory, self.level_loader.getplayerpos(self.current_level), self.level)
        self.player.set_direction(DOWN)

    def run(self):
        startsound.play()
        pygame.mixer.music.load("music/shootingstars.ogg")
        pygame.mixer.music.play(-1)
        self.events = EventGenerator()
        self.events.add_listener(FigureMoveListener(self.player.move))
        self.events.add_listener(FigureMoveListener(self.unstuck_ghosts))
        self.events.add_listener(FigureColorListener(self.player.set_color))
        self.events.add_listener(ExitListener(self.complete_level))
        with draw_timer(self, self.events):
            self.events.event_loop()

    def create_ghosts(self):
        self.ghosts = []
        for pos in self.level_loader.getghostpos(self.current_level):
            self.ghosts.append(Ghost(self.frame, self.tile_factory,
                               pos, self.level))

    def unstuck_ghosts(self, pos):
        for g in self.ghosts:
            g.unstuck()

    def check_collision(self, pos):
        if self.player.collision(self.ghosts):
            self.update_mode = self.update_die
            self.player.die()
            self.collided = True
        else:
            field = self.level.at(pos)
            if field in '123456':
                time.sleep(1)
                self.update_mode = self.update_level_complete
            elif field == 's':
                self.level.remove_soul(pos)

    def update_die(self):
        """finish movements"""
        if self.player.sprite.finished:
            time.sleep(1)
            self.player.lives = self.player.lives - 1
            if self.player.lives == 0:
                deadsound.play()
                self.events.exit_signalled()
                self.player.lives = 3
                self.run()
            else:
                self.status_box.data['lives'] = self.player.lives
                self.reset_level()
                self.events.empty_event_queue()
                self.update_mode = self.update_ingame

    def update_level_complete(self):
        """finish movement"""
        if self.player.sprite.finished:
            time.sleep(1)
            self.complete_level()


    def reset_level(self):
        self.player.sprite.pos = self.level_loader.getplayerpos(self.current_level)
        self.create_ghosts()

    def update_ingame(self):
        self.check_collision(self.player.sprite.pos)

    def create_status_box(self):
        frame = Frame(self.screen, Rect(700, 20, 200, 50))
        data = {
            'lives': 3,
            'level': 1,
        }
        self.status_box = DictBox(frame, data)

    def complete_level(self):
        print("complete")
        self.frame = Frame(self.screen, Rect(32, 32, 720, 720))
        self.tile_factory = TileFactory('data/colortiles.conf')
        self.current_level = 6
        self.level_loader = levels
        self.score = 0

        self.level = None
        self.player = None
        self.events = None
        self.ghosts = []
        self.update_mode = None
        self.status_box = None

        self.create_level()
        self.create_player()
        self.create_ghosts()
        self.create_status_box()

        self.collided = False
        self.mode = None
        self.update_mode = self.update_ingame
        self.run()


class Player:

    def __init__(self, frame, tile_factory, pos, level):
        self.level = level
        self.tile_factory = tile_factory
        tile = tile_factory.get('p_red_d')
        self.sprite = Sprite(frame, tile, pos, speed=4)
        self.eaten = None
        self.score = 0
        self.buffered_move = None

        self.color = RED
        self.direction = DOWN
        self.lives = 3

    def get_sprite_from_table(self, color, direction):
        row = 0
        col = 0
        if color == RED:
            row = 0
        elif color == BLUE:
            row = 1
        elif color == YELLOW:
            row = 2
        elif color == PURPLE:
            row = 3
        elif color == GREEN:
            row = 4
        elif color == ORANGE:
            row = 5
        if direction == UP:
            col = 0
        if direction == DOWN:
            col = 1
        if direction == LEFT:
            col = 2
        if direction == RIGHT:
            col = 3
        return self.tile_factory.get(FIGURE_SPRITES[row][col])

    def set_direction(self, direction):
        self.direction = direction
        self.sprite.tile = self.get_sprite_from_table(self.color, self.direction)

    def set_color(self, color):
        self.color = color
        self.sprite.tile = self.get_sprite_from_table(self.color, self.direction)
        ccsound.play()

    def move(self, direction):
        if not self.sprite.finished:
            self.buffered_move = direction
            return
        nearpos = self.sprite.pos + direction
        self.set_direction(direction)
        near = self.level.at(nearpos)

        allowedToMove = near == self.color and near != '#' or near == 'w' or near == 'i' or near == 's'
        # Allows movement to portal tiles if player color matches
        if near == '1' and BLUE == self.color:
            allowedToMove = True
        elif near == '2' and RED == self.color:
            allowedToMove = True
        elif near == '3' and YELLOW == self.color:
            allowedToMove = True
        elif near == '4' and GREEN == self.color:
            allowedToMove = True
        elif near == '5' and ORANGE == self.color:
            allowedToMove = True
        elif near == '6' and PURPLE == self.color:
            allowedToMove = True

        if allowedToMove:
            self.sprite.add_move(direction)
            movesound.play()

    def update(self):
        """Try eating dots and fruit"""
        if self.sprite.finished and self.buffered_move:
            self.move(self.buffered_move)
            self.buffered_move = None
        if not self.sprite.finished:
            self.sprite.move()

    def draw(self):
        self.sprite.draw()

    def collision(self, sprites):
        for sprite in sprites:
            if self.sprite.pos == sprite.sprite.pos:
                return True

    def die(self):
        self.buffered_move = None
        self.sprite.path = []
        damsound.play()

class Ghost:

    def __init__(self, frame, tile_factory, pos, level):
        tile = tile_factory.get(GHOST_TILE)
        self.level = level
        self.sprite = Sprite(frame, tile, pos, self.level.get_speed())
        self.direction = None
        self.set_random_direction()
        self.stuck = True

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
        elif not self.stuck:
            self.sprite.move()

    def update(self):
        self.move()

    def draw(self):
        self.sprite.draw()

    def unstuck(self):
        self.stuck = False


class ColorsLevel:

    def __init__(self, data, tmap, ghost_speed):
        self.tmap = tmap
        self.tmap.set_map(data)
        self.tmap.cache_map()
        self.souls_left = 0
        self.ghost_speed = ghost_speed

    def at(self, pos):
        return self.tmap.at(pos)

    def remove_soul(self, pos):
        tile = self.at(pos)
        self.tmap.set_tile(pos, 'w')
        self.tmap.cache_map()
        self.draw()
        souleatsound.play()

    def draw(self):
        self.tmap.draw()

    def get_speed(self):
        return self.ghost_speed

if __name__ == '__main__':
    pygame.mixer.music.load("music/allstar.ogg")
    pygame.mixer.music.play(-1)
    game = Game('data/colors.conf', Colors) #Change to data/colors.conf after creating title screen
    game.run()
