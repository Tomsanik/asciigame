from constants import Const as C


class CInventory:
    def __init__(self, owner):
        self.x, self.y = 0, 0
        self.tabs = [
            [C.ITEM_EQUIP, C.ITEM_CONSUM, C.ITEM_GARBAGE, C.ITEM_QUEST],
            [C.ITEM_CONSUM],
            [C.ITEM_EQUIP],
            [C.ITEM_GARBAGE]
        ]
        self.w = 4 #pocet zalozek
        self.h = 10 # pocet zobrazovanych predmetu v jedne zalozce
        self.owner = owner
        self.items = []

    def move(self, dx, dy):
        items = [] # items from chosen inventory section
        for i in self.items:
            if i.type in self.tabs[self.x]:
                items.append(i)

        if len(items) > 0:
            self.y = (self.y + dy) % len(items)

        if dx != 0:
            self.x = (self.x + dx) % self.w
            self.y = 0
        """self.y += dy
        if self.y < 0: self.y = self.h-1
        if self.y >= self.h: self.y = 0"""

    def add(self, item):
        if item not in self.items:
            self.items.append(item)
            y, x = divmod(len(self.items)-1,self.w)
            return {'done': True, 'x': x, 'y': y}
        else:
            return {'done': False, 'x': 0, 'y': 0}

    def drop(self, item):
        if item in self.items:
            self.items.remove(item)
