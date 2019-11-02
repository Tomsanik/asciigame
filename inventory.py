class CInventory:
    def __init__(self, owner):
        self.x, self.y = 0, 0
        self.w = 5 #pocet zalozek
        self.h = 5
        self.owner = owner
        self.items = []

    def move(self,dx,dy):
        self.y = (self.y + dy) % len(self.items)
        self.x = (self.x + dx) % self.w
        """self.y += dy
        if self.y < 0: self.y = self.h-1
        if self.y >= self.h: self.y = 0"""

    def add(self,item):
        if item not in self.items:
            self.items.append(item)
            y, x = divmod(len(self.items)-1,self.w)
        return {'done':True, 'x':x, 'y':y}

    def drop(self,item):
        if item in self.items:
            self.items.remove(item)
