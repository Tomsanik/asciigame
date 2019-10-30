import tcod as libtcod
from global_vars import gv


def render_all(con, entities, gm, screen_width, screen_height, colors): #gm=game_map
    # Draw all the tiles in the game map
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

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, gm)

    libtcod.console_set_default_foreground(con, libtcod.white)
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, gm):
    libtcod.console_set_default_foreground(con, entity.color)
    p=gm.policko(entity.x+gm.x*gm.w, entity.y+gm.y*gm.h)
    if entity.h<max(p.block): chr = p.char
    else: chr = entity.char
    libtcod.console_put_char(con, entity.x, entity.y, chr, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)