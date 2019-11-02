import tcod as libtcod
from global_vars import gv
from constants import Const as C


def render_all(con, entities, gm, screen_width, screen_height, colors): #gm=game_map
    # Draw all the tiles in the game map
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
                libtcod.console_set_default_foreground(con, c)
                libtcod.console_put_char(con, x, y, gm.tiles[nx][ny].char)
        gv.redraw_map = False

    # Draw all visible entities in the list
    for entity in entities:
        if entity.visible:
            draw_entity(con, entity, gm)

    if gv.GAME_STATE == C.GS_INVENTORY:
        draw_inventory(con, entities[0].inventory)

    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    #libtcod.console.blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


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


def draw_inventory(con, inv):
    i_x = 0 #tab
    i_y = 0
    i_w, i_h = 20, 20
    libtcod.console_rect(con, i_x+1, i_y+1, i_w, i_h, True)
    libtcod.console_put_char(con, i_x, i_y, 218)
    libtcod.console_hline(con, i_x+1, i_y, 20)
    libtcod.console_put_char(con, i_x+1+i_w, i_y, 191)

    libtcod.console_vline(con, i_x, i_y+1, 20)
    libtcod.console_vline(con, i_x+1+i_w, i_y+1, 20)

    libtcod.console_put_char(con, i_x, i_y+1+i_h, 192)
    libtcod.console_hline(con, i_x + 1, i_y+1+i_h, 20)
    libtcod.console_put_char(con, i_x+1+i_w, i_y+1+i_h, 217)

    i = 0
    for item in inv.items:
        if i == inv.y:
            libtcod.console_set_default_foreground(con, libtcod.green)
        libtcod.console_print(con, i_x+1, i_y+1+i, item.me.name)
        libtcod.console_set_default_foreground(con, libtcod.white)
        i += 1


def clear_entity(con, entity):
    # erase the character that represents this object
    # vykresluje vždy bíle, při pohybu ve výčce to kreslí bílou cestičku
    libtcod.console_put_char(con, entity.x, entity.y,
    gv.game_map.policko(entity.x, entity.y).char,
    libtcod.BKGND_NONE)
