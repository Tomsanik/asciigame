from enum import Enum, auto

class Const(Enum):
    #game states
    GS_PAUSE = 0
    GS_PLAY = 1
    GS_INVENTORY = 2
    GS_AIM = 3

    #fractions
    FR_PLAYER = 0
    FR_ENEMY = 1
    FR_NEUTRAL = 9

    #chars
    CH_At = 64
    CH_LowDen = 176
    CH_MedDen = 177
    CH_HigDen = 178
    CH_WhiteBox = 254

    #Entity types
    EN_HUMAN = 0 # lidi a destructibles
    EN_LOOTABLE = 1 # Truhla a mrtvola
    EN_ITEM = 2 # itemy
    EN_MOVABLE = 3 # pohyblive

    #Item types
    ITEM_CONSUM = auto()
    ITEM_EQUIP = auto()
    ITEM_QUEST = auto()
    ITEM_GARBAGE = auto()