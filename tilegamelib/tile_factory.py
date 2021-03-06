
from pygame import Rect, image
from .vector import Vector
from .tiles import Tile
import json
import os

TILE_SIZE = (32, 32)


class NoTileError(Exception): pass


class TileFactory:
    """
    Manages a set of tiles.
    """
    def __init__(self, config_filename):
        self.tiles = {}
        self.tile_size = Vector(32, 32)
        self.path = ''
        self.parse_config(config_filename)

    def parse_config(self, config_filename):
        path, fn = os.path.split(config_filename)
        self.path = path + os.sep
        conf = json.loads(open(config_filename).read())
        self.tile_size = Vector(conf['tile_size'][0], conf['tile_size'][1])
        for tileset in conf['tilesets'].values():
            self.load_tiles(tileset)
        self.add_tile_synonyms(conf['synonyms'])

    def load_tiles(self, tileset):
        """Loads tile graphics from a file."""
        img = image.load(self.path + tileset['filename']).convert_alpha()
        for xpos, ypos, name in tileset['tiles']:
            index = Vector(int(xpos), int(ypos))
            self.tiles[name] = Tile(name, index, self.tile_size, img)

    def add_tile_synonyms(self, synonyms):
        for abbrev in synonyms:
            self.tiles[abbrev] = self.get(synonyms[abbrev])
    
    def get(self, key):
        """Returns a Tile instance."""
        result = self.tiles.get(key, None)
        if not result:
            raise NoTileError("No such tile: %s" % str(key))
        return result
