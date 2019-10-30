class CInventory:
    def __init__(self, owner):
        self.x, self.y = 0, 0
        self.w = 5
        self.h = 5
        self.owner = owner

    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        if self.x < 0: self.x = self.w-1
        if self.y < 0: self.y = self.h-1
        if self.x >= self.w: self.x = 0
        if self.y >= self.h: self.y = 0

    def add(self,items):
        self.item.extend(items)

    def drop(self,item):
        if item in self.items:
            self.items.remove(item)