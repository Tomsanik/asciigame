import event_handling
import tcod as libtcod
from global_vars import gv
from constants import Const as C
from inventory import CInventory


class Entity:
    def __init__(self, x, y, h, char, type, color, name):
        self.x = x
        self.y = y
        self.h = h
        self.type = type
        self.char = char
        self.name = name
        self.color = color
        self.def_color = color
        self.def_char = char

        if self.type == C.EN_HUMAN:
            self.fighter = Fighter(0, 1, 0, C.FR_NEUTRAL)
        self.fighter = None
        self.item = None

    def move(self, dx, dy, dh): #gm=game_map
        gm = gv.game_map
        nx, ny = self.x + dx + gm.x*gm.w, self.y + dy + gm.y*gm.h
        if (nx) * (ny) < 0: return False

        kont = True
        for ent in gv.entities:
            if (ent.x, ent.y, ent.h) == (nx, ny, self.h + dh):
                kont = self.interact(ent, (dx,dy,dh))
                break
        if not kont: return False

        if not self.h + dh in gm.policko(nx, ny).block:
            # print(self.x + dx, self.y + dy, self.h + dh, gm.policko(nx, ny).block)
            self.x += dx
            self.y += dy
            self.h += dh
            if self.type == 0: #mapu posouva pouze hrac
                if self.x == gm.w:
                    gm.x += 1
                    self.x = 0
                if self.y == gm.h:
                    gm.y +=1
                    self.y = 0
                if (self.x < 0) and (gm.x > 0):
                    gm.x += -1
                    self.x = gm.w-1
                if (self.y < 0) and (gm.y > 0):
                    gm.y += -1
                    self.y = gm.h -1

            return True
        return False

    def interact(self, ent, move): # interakce po dvojicich!! (ent.typ, self.typ)
        # vraci, zda se ma postava pohnout (move)
        if ent.type == C.EN_ITEM:
            #ADD: zobrazeni panelu s info o predmetu
            return True
        elif (ent.type, self.type) == (C.EN_HUMAN, C.EN_HUMAN):
            print("ÚTOOOK!!")
            ent.fighter.take_dmg(ent, self.fighter.atk)
        elif ent.type == C.EN_MOVABLE:
            dx, dy, dh = move
            if ent.move(dx, dy, dh):
                return True # pohni se
        return False # zustan stat


class Fighter:
    def __init__(self, atk, hp, defe, fraction, auto = -1):
        #if auto >= 0:
            #self.type = auto
            #self.
        self.atk = atk
        self.hp = hp
        self.dfnc = defe
        self.fraction = fraction
        self.equip = {'weap': None, 'armor': None}
        self.inventory = CInventory(self)

    def death(self, me):
        blik = event_handling.EventChangeChar(me, "C", [])
        gv.events.append(blik)
        blik.start()
        me.type = C.EN_LOOTABLE

    def take_dmg(self, me, atk):
        atk = max(0, atk-self.dfnc)
        self.hp += -atk
        blik = event_handling.EventChangeColor(me,libtcod.red,[0.1])
        gv.events.append(blik)
        blik.start()
        if self.hp <= 0:
            self.death(me)


class Item:
    def __init__(self, kind, price=0):
        self.kind = kind
        self.stats = None
        self.price = price

    def add_stats(self, **kwargs): #available: heal (heal < 0 = dmg)
        self.stats = {'heal':0}
        for key, value in kwargs.items():
            #if (key,value)==("auto", True): # autofill
                #self.stats = const.item_stats.get(self.kind)
                #break
            self.stats[key] = value

    def use_item(self, user, target):
        if self.type == C.ITEM_HPPOT:
            user.hp += self.type.value
        if self.type == C.ITEM_SWORD1:
            if user.equip['weap'] != None:
                user.inventory.add(user.equip['weap'])
            user.equip['weap'] = self
