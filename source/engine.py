import tcod as libtcod
from entity import Entity, Fighter, Item
from input import handle_keys
from render_functions import clear_all, render_all
from event_handling import EventChangeColor, EventChangeChar, handle_events
from time import sleep
import threading
from global_vars import gv
from constants import Const as C

def thread_timer():
    global timer
    while True:
        sleep(0.05)
        gv.timer += 0.05

def main():
    cursor = Entity(37, 30, 1, "+", C.EN_CURSOR, libtcod.white, "")
    cursor.visible = False

    player = Entity(37, 30, 1, "O", C.EN_HUMAN, libtcod.green, "Hrac")
    player.fighter.set_props(attack=10, defense=1, maxhp=100)

    npc =    Entity(30, 30, 1, "X", C.EN_HUMAN, libtcod.white, "NPC")
    npc.fighter.set_props(attack=10, defense=1, maxhp=50)

    box =    Entity(15, 15, 1, 254, C.EN_MOVABLE, libtcod.white, "Box")

    pot =    Entity(30, 32, 1, '+', C.EN_ITEM, libtcod.white,"Healing Potion S")
    pot.item.set_props(hp = 20, price = 10, type=C.ITEM_CONSUM)
    #pot.item.add_to_inventory(player.inventory)

    sword = Entity(25, 30, 1, '?', C.EN_ITEM, libtcod.white, "Weak sword")
    sword.item.set_props(attack=20, price=10, type=C.ITEM_WEAP)

    sword2 = Entity(25, 30, 1, '?', C.EN_ITEM, libtcod.white, "Super sword")
    sword2.item.set_props(attack=30, price=10, type=C.ITEM_WEAP)

    armor = Entity(20, 30, 1, '?', C.EN_ITEM, libtcod.white, "Super Armor")
    armor.item.set_props(maxhp=20, defense=5, price=10, type=C.ITEM_ARMOR, requires = {'lvl':1, 'eyes':2})

    # na 1. miste hrac, na -1. miste kurzor
    gv.entities=[player, box, pot, npc, sword, sword2, armor, cursor]

    event = EventChangeColor(box, libtcod.red, [1,1,1])
    event2 = EventChangeChar(player,"V",[1,1,0.5,1,0.5])
    gv.events = [event, event2]

    libtcod.console_set_custom_font('../fonts/Cheepicus_15x15.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(gv.screen_width, gv.screen_height, 'libtcod tutorial revised',False,libtcod.RENDERER_OPENGL2,"F",True)

    c_map = libtcod.console.Console(gv.screen_width, gv.screen_height)
    c_inv = libtcod.console.Console(22, 22)
    c_info = libtcod.console.Console(22, 32)
    c_gmst = libtcod.console.Console(22, 3)
    cons = {'map':c_map, 'inv':c_inv, 'info':c_info, 'gmst':c_gmst}

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    casovac = threading.Thread(target=thread_timer, daemon=True)
    casovac.start()

    while not libtcod.console_is_window_closed():
        handle_events(gv.events, gv.timer)

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        render_all(cons, gv.entities, gv.game_map, gv.colors)
        libtcod.console_flush()
        clear_all(c_map,gv.entities)

        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        grab = action.get('grab')
        swap = action.get('swap')
        inv = action.get('inv')

        if grab:
            if gv.GAME_STATE == C.GS_PLAY:
                for i in gv.entities:
                    if (i != player) and (i.type == C.EN_ITEM):
                        if i.x == player.x and i.y == player.y:
                            i.item.collect(player.inventory)
            elif gv.GAME_STATE == C.GS_INVENTORY:
                player.inventory.items[player.inventory.y].use_item(player,player)

        if swap:
            if gv.GAME_STATE == C.GS_PLAY:
                gv.GAME_STATE = C.GS_PAUSE
                cursor.visible = True
            elif gv.GAME_STATE == C.GS_PAUSE:
                gv.GAME_STATE = C.GS_PLAY
                cursor.visible = False
                cursor.x = player.x
                cursor.y = player.y
                cursor.h = player.h

        if inv:
            if gv.GAME_STATE == C.GS_INVENTORY:
                gv.GAME_STATE = C.GS_PLAY
                gv.redraw_map = True
            elif gv.GAME_STATE == C.GS_PLAY:
                gv.GAME_STATE = C.GS_INVENTORY

        if move:
            if gv.GAME_STATE == C.GS_PLAY:
                dx, dy, dh = move
                if player.move(dx, dy, dh):
                    cursor.move(dx, dy, dh)
                #if dh != 0:
                    #gv.redraw_map = True
            elif gv.GAME_STATE == C.GS_INVENTORY:
                dx, dy, dh = move
                player.inventory.move(dx,dy)
            elif gv.GAME_STATE == C.GS_PAUSE:
                dx, dy, dh = move
                cursor.move(dx, dy, dh)

        if exit:
            if gv.GAME_STATE != C.GS_PLAY:
                gv.GAME_STATE = C.GS_PLAY
                gv.redraw_map = True
            else:
                return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
