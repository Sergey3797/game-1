from enum import Enum
from utils import randobool, randcell, randNeigbor

class MapFields(Enum):
    FIELD = "🟩"
    TREE = "🌲"
    WAVE = "🌊"
    HOSPITAL = "🏥"
    SHOP = "🏢"
    FIRE = "🔥"
    HELICOPTER = "🚁"

CELL_TYPES = [MapFields.FIELD.value, 
              MapFields.TREE.value,
              MapFields.WAVE.value,
              MapFields.HOSPITAL.value,
              MapFields.SHOP.value,
              MapFields.FIRE.value,
              MapFields.HELICOPTER.value]

TREE_BONUS = 100
UPGRADE_COST = 5000
LIFE_COST = 1000

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(5, 10)
        self.generate_river(11)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
            if (x < 0 or y < 0 or x >= self.h or y >= self.w):
                return False
            else: 
                return True
            
    def getMapFieldId(self, string):
        return CELL_TYPES.index(string)
            
    def print_map(self, helico, clouds):
        print("⬛" * (self.w + 2))
        for ri in range(self.h):
            print("⬛", end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (clouds.cells[ri][ci] == 1):
                    print("⚪", end="")
                elif (clouds.cells[ri][ci] == 2):
                    print("🟡", end="")
                elif (helico.x == ri and helico.y == ci):
                    print(MapFields.HELICOPTER.value, end="")
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print("⬛")
        print("⬛" * (self.w + 2))

    # Генерация реки
    def generate_river(self, l):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = self.getMapFieldId(MapFields.WAVE.value)
        while l > 0:
            rc2 = randNeigbor(rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if (self.check_bounds(rx2, ry2)):
                self.cells[rx2][ry2] = self.getMapFieldId(MapFields.WAVE.value)
                rx, ry = rx2, ry2
                l -= 1

    # Генерация леса
    def generate_forest(self, r, mxr):
        for rowPosVal in range(self.h):
            for cellPosVal in range(self.w):
                if randobool(r, mxr):
                    self.cells[rowPosVal][cellPosVal] = self.getMapFieldId(MapFields.TREE.value)

    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] == self.getMapFieldId(MapFields.FIELD.value)):
            self.cells[cx][cy] = self.getMapFieldId(MapFields.TREE.value)

    # Генерация зданий
    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = self.getMapFieldId(MapFields.SHOP.value)

    def generate_hospital(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] != self.getMapFieldId(MapFields.SHOP.value)):
            self.cells[cx][cy] = self.getMapFieldId(MapFields.HOSPITAL.value)
        else:
            self.generate_hospital()

    # Генерация огня
    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] == self.getMapFieldId(MapFields.TREE.value)):
            self.cells[cx][cy] = self.getMapFieldId(MapFields.FIRE.value)

    def update_fires(self):
        for rowPosVal in range(self.h):
            for cellPosVal in range(self.w):
                cell = self.cells[rowPosVal][cellPosVal]
                if cell == self.getMapFieldId(MapFields.FIRE.value):
                    self.cells[rowPosVal][cellPosVal] = self.getMapFieldId(MapFields.FIELD.value)
        for i in range(5):
            self.add_fire()


    # Обработка вертолета
    def process_helicopter(self, helico, clouds):
        cur_cell = self.cells[helico.x][helico.y]
        cloud_cell = clouds.cells[helico.x][helico.y]
        if (cur_cell == self.getMapFieldId(MapFields.WAVE.value)):
            helico.tank = helico.mxtank

        if (cur_cell == self.getMapFieldId(MapFields.FIRE.value) and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = self.getMapFieldId(MapFields.TREE.value)
        
        if (cur_cell == self.getMapFieldId(MapFields.SHOP.value) and helico.score >= UPGRADE_COST):
            helico.mxtank += 1
            helico.score -= UPGRADE_COST

        if (cur_cell == self.getMapFieldId(MapFields.HOSPITAL.value) and helico.score >= LIFE_COST):
            helico.lives += 10
            helico.score -= LIFE_COST

        if (cloud_cell == 2):
            helico.lives -= 1
            if (helico.lives == 0):
                helico.game_over()

    def export_data(self):
        return {"cells": self.cells}
    
    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]