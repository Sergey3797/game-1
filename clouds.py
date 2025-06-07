from utils import randobool

class Clouds:
    def __init__(self, w, h):
        self.h = h
        self.w = w
        self.cells = [[0 for i in range(w)] for j in range(h)]

    def update_clouds(self, r = 1, mxr = 20, g = 1, mxg = 10):
        for rowPosVal in range(self.h):
            for cellPosVal in range(self.w):
                if randobool(r, mxr):
                    self.cells[rowPosVal][cellPosVal] = 1
                    if randobool(g, mxg):
                        self.cells[rowPosVal][cellPosVal] = 2
                else:
                    self.cells[rowPosVal][cellPosVal] = 0

    def export_data(self):
        return {"cells": self.cells}
    
    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]