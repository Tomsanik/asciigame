import tcod as libtcod
from global_vars import gv
from constants import Const as C
from inventory import CInventory


def render_all(con, entities, gm, colors): #gm=game_map
    # Draw all the tiles in the game map
    c_map = con.get('map')
    c_inv = con.get('inv')
    c_info = con.get('info')
    c_gmst = con.get('gmst')
    if gv.redraw_map:
        for y in range(gm.h):
            for x in range(gm.w):
                nx = x + gm.x * gm.w
                ny = y + gm.y * gm.h
                b = gm.policko(nx, ny).block
                if max(b) - entities[0].h+1 in colors:
                    c = colors.get(max(b) - entities[0].h+1)
                else: c = libtcod.black
                #c = libtcod.white
                libtcod.console_set_default_foreground(c_map, c)
                libtcod.console_put_char(c_map, x, y, gm.tiles[nx][ny].char)
        gv.redraw_map = False
    libtcod.console_set_default_foreground(c_map, libtcod.white)

    draw_info(c_info)
    # Draw all visible entities in the list
    for entity in entities:
        if entity.visible:
            draw_entity(c_map, entity, gm)

    libtcod.console_blit(c_map, 0, 0, gv.map_width, gv.map_height, 0, 0, 0)

    if gv.GAME_STATE == C.GS_INVENTORY:
        draw_info(c_info, entities[0].inventory.get_selected())
        draw_inventory(c_inv, entities[0].inventory)
    else:
        cur = entities[-1]
        for ent in entities:
            if ent == cur: continue
            if (cur.x, cur.y, cur.h) == (ent.x, ent.y, ent.h):
                draw_info(c_info, ent)
    #libtcod.console.blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    if gv.GAME_STATE == C.GS_PAUSE:
        libtcod.console_print(c_gmst, 5, 0, "GAME PAUSED")
    libtcod.console_blit(c_gmst, -50, -2, gv.screen_width, 3, 0, 0, 0)
    libtcod.console_print(c_gmst, 5, 0, "           ")


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, gm):
    libtcod.console_set_default_foreground(con, entity.color)
    p = gm.policko(entity.x+gm.x*gm.w, entity.y+gm.y*gm.h)
    if entity.h < max(p.block):
        char = p.char
    else:
        char = entity.char
    libtcod.console_put_char(con, entity.x, entity.y, char, libtcod.BKGND_NONE)


def draw_inventory(con, inv: CInventory):

    i_w, i_h = 19, 20
    i_x = (gv.map_width-i_w-2) //2
    i_y = (gv.map_height-i_h-2) //2

    libtcod.console_rect(con, 1, 1, i_w, i_h, True)

    # print tabs
    libtcod.console_print(con, 1, 1, ' A ' + chr(179) + ' C ' + chr(179) + ' E ' + chr(179) + ' G ' + chr(179) + ' Q ')

    libtcod.console_hline(con, 1, 2, -1 + inv.x * 4)
    libtcod.console_put_char(con, inv.x * 4, 2, 217)
    libtcod.console_put_char(con, (inv.x + 1) * 4, 2, 192)
    libtcod.console_hline(con, (inv.x + 1) * 4 + 1, 2, 20 - (inv.x + 1) * 4)

    libtcod.console_put_char(con, 0, 0, 218)
    libtcod.console_hline(con, 1, 0, 20)
    libtcod.console_put_char(con, 1+i_w, 0, 191)

    libtcod.console_vline(con, 0, 1, 20)
    libtcod.console_vline(con, 1+i_w, 1, 20)

    libtcod.console_put_char(con, 0, 1+i_h, 192)
    libtcod.console_hline(con, 1, 1+i_h, 20)
    libtcod.console_put_char(con, 1+i_w, 1+i_h, 217)

    i = 0
    s = ""
    for item in inv.items:
        if item.type in inv.tabs[inv.x]:
            if i == inv.y:
                libtcod.console_set_default_foreground(con, libtcod.green)
            if item.equipped: s =  "(E)"
            else: s = ""
            libtcod.console_print(con, 1, 3+i, "{0:15} {1}".format(item.me.name, s))
            libtcod.console_set_default_foreground(con, libtcod.white)
            i += 1
    libtcod.console_blit(con, -i_x, -i_y, i_w+i_x+2, i_h+i_y+2, 0, 0, 0)


def draw_info(con, ent = None):
    i_w = 17
    i_h = 20
    libtcod.console_rect(con, 1, 1, i_w, i_h, True)

    """libtcod.console_put_char(con, 0, 0, 218)
    libtcod.console_hline(con, 1, 0, i_w)
    libtcod.console_put_char(con, 1 + i_w, 0, 191)

    libtcod.console_vline(con, 0, 1, i_h)
    libtcod.console_vline(con, 1 + i_w, 1, i_h)

    libtcod.console_put_char(con, 0, 1 + i_h, 192)
    libtcod.console_hline(con, 1, 1 + i_h, i_w)
    libtcod.console_put_char(con, 1 + i_w, 1 + i_h, 217)"""

    if ent != None:
        if ent.type == C.EN_ITEM:
            libtcod.console_set_default_foreground(con, libtcod.green)
            libtcod.console_print(con, 1, 1, ent.name)
            libtcod.console_set_default_foreground(con, libtcod.white)
            i = 2
            for key, val in ent.item.stats.items():
                if val != 0:
                    s = key + ': '+str(val)
                    libtcod.console_print(con, 3, i, s)
                    i += 1
        elif ent.type == C.EN_HUMAN:
            libtcod.console_set_default_foreground(con, libtcod.green)
            libtcod.console_print(con, 1, 1, ent.name)
            libtcod.console_set_default_foreground(con, libtcod.white)
            s = str(ent.fighter.stats['hp'])+'/'+str(ent.fighter.stats['maxhp'])
            libtcod.console_print(con, 3, 2, 'HP: '+s)
            i = 3
            for key, val in ent.fighter.stats.items():
                if key in ['hp','maxhp']: continue
                if val != 0:
                    s = key + ': ' + str(val)
                    libtcod.console_print(con, 3, i, s)
                    i += 1

    libtcod.console_blit(con, -50, -28, 67, 50, 0, 0, 0)


def clear_entity(con, entity):
    # erase the character that represents this object
    # vykresluje vždy bíle, při pohybu ve výčce to kreslí bílou cestičku
    libtcod.console_put_char(con, entity.x, entity.y,
    gv.game_map.policko(entity.x, entity.y).char,
    libtcod.BKGND_NONE)
