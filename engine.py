import tcod as libtcod
from entity import Entity, Fighter, Item
from input import handle_keys
from render_functions import clear_all, render_all
from event_handling import EventChangeColor, EventChangeChar, handle_events
from time import sleep
import threading
from global_vars import gv
from constants import *

def thread_timer():
    global timer
    while True:
        sleep(0.05)
        gv.timer += 0.05

def main():

    player = Entity(37, 30, 1, "O", EN_HUMAN, libtcod.green, "Hrac")
    player.fighter = Fighter(10, 100, 5, FR_PLAYER)

    npc =    Entity(30, 30, 1, "X", EN_HUMAN, libtcod.white, "NPC")
    npc.fighter = Fighter(10, 100, 5, FR_ENEMY)

    box =    Entity(15, 15, 1, 254, EN_MOVABLE, libtcod.white, "Box")
    pot =    Entity(30, 32, 1, '?', EN_ITEM, libtcod.white,"Healing Potion S")
    pot.item = Item(ITEM_HPPOT1)
    pot.item.add_stats(dmg = 0, heal = 20)

    gv.entities=[box, pot, player, npc ]

    event = EventChangeColor(box, libtcod.red, [1,1,1])
    event2 = EventChangeChar(player,"V",[1,1,0.5,1,0.5])
    gv.events = [event, event2]

    libtcod.console_set_custom_font('fonts/Cheepicus_15x15.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(gv.screen_width, gv.screen_height, 'libtcod tutorial revised',False,libtcod.RENDERER_OPENGL2,"F",True)

    con = libtcod.console.Console(gv.screen_width, gv.screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    casovac = threading.Thread(target=thread_timer, daemon=True)
    casovac.start()

    while not libtcod.console_is_window_closed():
        handle_events(gv.events, gv.timer)

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, gv.entities, gv.game_map, gv.screen_width, gv.screen_height, gv.colors)
        libtcod.console_flush()
        #clear_all(con,entities)

        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        swap = action.get('swap')
        inv = action.get('inv')

        if swap:
            npc.death()

        if inv:
            gv.GAME_STATE = const.GS_INVENTORY

        if move and gv.GAME_STATE == GS_PLAY:
            dx, dy, dh = move
            player.move(dx, dy, dh)
        elif move and gv.GAME_STATE == GS_INVENTORY:
            dx, dy, dh = move
            player.inventory.move(dx,dy)

        if exit:
            return True
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()