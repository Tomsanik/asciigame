from map_objects.tile import CTile
import csv
import random as rd

class CGameMap:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.world_w = 100
        self.world_h = 100
        self.x = 0
        self.y = 0
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = []

        with open('mapa.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',',quotechar='"')
            pom = []
            for row in csv_reader:
                if row == []: continue
                lst = eval(row[3])
                pom.append(CTile(int(row[2]),lst))
                if int(row[1])==self.world_h:
                    tiles.append(pom)
                    pom = []
        return tiles

    def policko(self,x,y):
        return self.tiles[x][y]
