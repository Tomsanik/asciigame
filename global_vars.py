import tcod as libtcod
from map_objects.game_map import CGameMap
from constants import Const as C


class CGVars:
    def __init__(self):
        self.timer = 0
        self.events = []
        self.screen_width = 80
        self.screen_height = 50

        self.map_width = 50
        self.map_height = 50

        self.colors = {
            -4: libtcod.Color(255, 39, 39),
            -3: libtcod.Color(255, 85, 85),
            -2: libtcod.Color(255, 131, 131),
            -1: libtcod.Color(255, 180, 180),
            0: libtcod.white,
            1: libtcod.Color(208, 224, 255),
            2: libtcod.Color(192, 213, 255),
            3: libtcod.Color(154, 187, 255),
            4: libtcod.Color(115, 161, 255),
            5: libtcod.Color(95, 140, 255)
        }

        self.entities = []
        self.game_map = CGameMap(self.map_width, self.map_height)

        self.GAME_STATE = C.GS_PLAY

        self.item_stats = {
            C.ITEM_HPPOT1: {'heal': 20},
            C.ITEM_SWORD1: {'heal': -20}
        }

        #self.fighter_stats = {
        #    const.EN_HUMAN:
        #}


gv = CGVars()
