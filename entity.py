import event_handling
import tcod as libtcod
from global_vars import gv
from constants import Const as C
from inventory import CInventory


class Entity:
    def __init__(self, x:int, y:int, h:int, char:int, type:int, color, name:str):
        self.x = x
        self.y = y
        self.h = h
        self.type = type
        self.char = char
        self.name = name
        self.color = color
        self.def_color = color
        self.def_char = char
        self.inventory = CInventory(self) #inv musi mit uz Entity kvuli truhlam
        self.visible = True

        self.fighter = None
        self.item = None
        if self.type == C.EN_HUMAN:
            self.fighter = Fighter(self)
        elif self.type == C.EN_ITEM:
            self.item = Item(self)

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
            if self.type == C.EN_HUMAN: #mapu posouva pouze hrac
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
            ent.fighter.take_dmg(self.fighter.stats['attack'])
        elif ent.type == C.EN_MOVABLE:
            dx, dy, dh = move
            if ent.move(dx, dy, dh):
                return True # pohni se
        return False

class Fighter:
    def __init__(self, owner):
        self.stats = {'attack': 0, 'hp': 0, 'defense': 0, 'fraction': 0}
        self.equip = {'weap': None, 'armor': None}
        self.me = owner

    def set_stats(self, add: bool=False, **kwargs): #available: heal (heal < 0 = dmg)
        for key, value in kwargs.items():
            self.stats[key] = value

    def stat(self, stat_name: str):
        # vraci dany stat ze slovniku stats
        if stat_name in self.stats:
            return self.stats[stat_name]
        else:
            return 0

    def death(self):
        blik = event_handling.EventChangeChar(self.me, "C", [])
        gv.events.append(blik)
        blik.start()
        self.me.type = C.EN_LOOTABLE

    def take_dmg(self, atk): #vyhledove misto atk davat celeho utocnika
        atk = max(0, atk-self.stats['defense'])
        self.stats['hp'] += -atk
        blik = event_handling.EventChangeColor(self.me,libtcod.red,[0.1])
        gv.events.append(blik)
        blik.start()
        if self.stats['hp'] <= 0:
            self.death()


class Item:
    def __init__(self, owner):
        self.type = C.ITEM_CONSUM
        self.stats = {'heal':0}
        self.req = {'lvl': 0}
        self.me = owner

    def set_stats(self, add: bool=False, **kwargs): #available: heal (heal < 0 = dmg)
        for key, value in kwargs.items():
            self.stats[key] = value

    def set_requirement(self, **kwargs):
        for key, value in kwargs.items():
            self.stats[key] = value

    def use_item(self, user, target = None):
        if self.type == C.ITEM_CONSUM:
            user.fighter.stats['hp'] += self.stats['heal']
            print(user.fighter.stats['hp'])
        if self.type == C.ITEM_EQUIP:
            if user.equip['weap'] != None:
                user.inventory.add(user.equip['weap'])
            user.equip['weap'] = self

    def add_to_inventory(self,inv):
        done, x, y = inv.add(self)
        if done:
            self.me.x = x
            self.me.y = y
            gv.entities.remove(self.me)
        else:
            print('Predmet nelze pridat do intventare')
