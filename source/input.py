import tcod as libtcod


def handle_keys(key):
    # Movement keys
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1, 0)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1, 0)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0, 0)}
    elif key.vk == libtcod.KEY_SPACE:
        return {'swap': True}
    elif chr(key.c) == "e":
        return {'grab': True}
    elif chr(key.c) == "i":
        return {'inv': True}

    elif chr(key.c) == "w":
        return {'move': (0, 0, 1)}
    elif chr(key.c) == "s":
        return {'move': (0, 0, -1)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
