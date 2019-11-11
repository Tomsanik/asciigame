from enum import Enum, auto

class Const(Enum):
    #game states
    GS_PAUSE = auto()
    GS_PLAY = auto()
    GS_INVENTORY = auto()
    GS_AIM = auto()

    #fractions
    FR_PLAYER = auto()
    FR_ENEMY = auto()
    FR_NEUTRAL = auto()

    #chars
    CH_At = auto()
    CH_LowDen = auto()
    CH_MedDen = auto()
    CH_HigDen = auto()
    CH_WhiteBox = auto()

    #Entity types
    EN_HUMAN = auto() # lidi a destructibles
    EN_LOOTABLE = auto() # Truhla a mrtvola
    EN_ITEM = auto() # itemy
    EN_MOVABLE = auto() # pohyblive
    EN_CURSOR = auto() #kurzor

    #Item types
    ITEM_CONSUM = auto()
    ITEM_WEAP = auto()
    ITEM_ARMOR = auto()
    ITEM_QUEST = auto()
    ITEM_GARBAGE = auto()