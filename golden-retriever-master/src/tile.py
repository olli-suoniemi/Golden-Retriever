from PyQt5 import QtWidgets
from PyQt5 import QtGui
# From most common to rare
# name = type = value = weight

# sand = s = 1..9 = 1

# bronze = b = 9 = 2
# silver = l = 15 = 4
# gold = g = 20 = 7

# ruby = r = 50 = 12
# diamond = d = 75 = 16
# opal = o = 120 = 20

# golden bone = w
class Tile(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, square_size, x_c, y_c, type, level):
        super().__init__()
        self.size = square_size
        self.type = type
        self.level = level
        self.value = 0
        self.weight = 0
        self.dig_time = 0
        self.dug = False
        self.setPos(x_c, y_c)
        if type == "x":
            if level == 0:
                self.setPixmap(QtGui.QPixmap("sprites/minerals/top_iron.png"))
            else:
                self.setPixmap(QtGui.QPixmap("sprites/minerals/iron.png"))
        elif type == "a":
            self.dug = True
            self.setPixmap(QtGui.QPixmap("sprites/minerals/air.png"))
        elif type == "s":
            self.dig_time = 100
            if (int(level/10)) == 0:
                self.value = 1
            else:
                self.value = int(level/10)
            if level == 0:
                self.setPixmap(QtGui.QPixmap("sprites/minerals/top_sand.png"))
            else:
                self.setPixmap(QtGui.QPixmap("sprites/minerals/sand.png"))
        elif type == 'b':
            self.value = 9
            self.weight = 2
            self.dig_time = 110
            self.setPixmap(QtGui.QPixmap("sprites/minerals/bronze.png"))
        elif type == 'l':
            self.value = 15
            self.weight = 4
            self.dig_time = 120
            self.setPixmap(QtGui.QPixmap("sprites/minerals/silver.png"))
        elif type == 'g':
            self.value = 20
            self.weight = 7
            self.dig_time = 130
            self.setPixmap(QtGui.QPixmap("sprites/minerals/gold.png"))
        elif type == 'r':
            self.value = 50
            self.weight = 12
            self.dig_time = 140
            self.setPixmap(QtGui.QPixmap("sprites/minerals/ruby.png"))
        elif type == 'd':
            self.value = 75
            self.weight = 16
            self.dig_time = 150
            self.setPixmap(QtGui.QPixmap("sprites/minerals/diamond.png"))
        elif type == 'o':
            self.value = 120
            self.weight = 20
            self.dig_time = 160
            self.setPixmap(QtGui.QPixmap("sprites/minerals/opal.png"))
        elif type == 'w':
            self.setPixmap(QtGui.QPixmap("sprites/minerals/goldenbone.png"))
            self.dig_time = 1000


    def getType(self):
        return self.type

    def getDug(self):
        return self.dug

    def getValue(self):
        return self.value

    def getLevel(self):
        return self.level

    def getDigtime(self):
        return self.dig_time

    def setDug(self):
        self.dug = True