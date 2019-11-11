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
        if self.type == C.EN_CURSOR:
            return True
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
        self.stats = {'attack': 0, 'hp': 0, 'maxhp':0, 'defense': 0, 'fraction': 0}
        self.equip = {'weap': None, 'armor': None}
        self.me = owner

    def set_props(self, add: bool=False, **kwargs): #available: heal (heal < 0 = dmg)
        for key, value in kwargs.items():
            if add: # pricitani do statu
                self.stats[key] += value
            else: # nahrazovani hodnot statu
                self.stats[key] = value
            if key == 'maxhp':
                self.stats['hp'] += value
            elif key == 'hp':
                if value > 0:
                    self.take_dmg(value)
                else:
                    self.heal(value)

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

    def take_dmg(self, atk: int): #vyhledove misto atk davat celeho utocnika
        #atk = attacker.fighter.stats.get('attack')
        atk = max(0, atk-self.stats.get('defense'))
        self.stats['hp'] += -atk
        print(self.stats['hp'])
        blik = event_handling.EventChangeColor(self.me,libtcod.red,[0.1])
        gv.events.append(blik)
        blik.start()
        if self.stats.get('hp') <= 0:
            self.death()

    #def heal_dmg(self, healer: Entity):


class Item:
    def __init__(self, owner):
        self.type = C.ITEM_GARBAGE
        #self.id = 0
        self.props = {'id':0}
        self.stats = {'heal': 0, 'hp': 0, 'attack': 0}
        self.req = {'lvl': 0}
        self.equipped = False
        self.me = owner

    def set_props(self, add: bool=False, **kwargs):
        #available props: heal (heal < 0 = dmg), require = {...}, id
        for key, value in kwargs.items():
            if key == 'type':
                self.type = value
            elif key == 'requires':
                self.req = value
            else:
                self.stats[key] = value

    def use_item(self, user: Entity, target: Entity = None):
        if self.type == C.ITEM_CONSUM:
            user.fighter.stats['hp'] += self.stats['hp']
            print(user.fighter.stats['hp'])

        elif self.type in [C.ITEM_WEAP, C.ITEM_ARMOR]:
            if self.type == C.ITEM_ARMOR: # zkusit zjednodusit
                typ = 'armor'
            else:
                typ = 'weap'

            st = user.fighter.stats
            if user.fighter.equip[typ] != None: # presunuti equipnute zbrane zpet do inv
                # odecist staty stareho equip itemu
                for key, val in user.fighter.equip[typ].stats.items():
                    if key in st:
                        st[key] += -val
                #user.inventory.add(user.fighter.equip[typ])
                user.fighter.equip[typ].equipped = False
            user.fighter.equip[typ] = self
            self.equipped = True

            for key, val in self.stats.items():
                if key in st:
                    # udelat pomoci set_stats
                    #if key == 'hp':
                    st[key] += val
            print(user.fighter.stats)


    def collect(self, inv):
        done, x, y = inv.add(self)
        if done:
            self.me.x = x
            self.me.y = y
            gv.entities.remove(self.me)
        else:
            print('Predmet nelze pridat do inventare')

    def drop(self, inv):
        print('Žuch na zem')
        # projit gv.entities, jestli na necem nestojim
        # vratit item do gv.entities

