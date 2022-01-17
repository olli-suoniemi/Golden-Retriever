import random
from PyQt5 import QtWidgets, QtCore, Qt
Y = 600

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

class World(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.width = 30
        self.height = 0
        self.bottom = 0
        self.pool = []
        self.map = self.generateMap()

    def setWorld(self):
        self.generateMap()

    def generateMap(self):
        self.pool.clear()
        file = open("map.txt", "w")
        hole1_1, hole2_1, hole3_1 = 1, 1, 1
        hole1_2, hole2_2, hole3_2 = self.width-1, self.width-1, self.width-2
        running_number = 0
        mineral = 's'
        for i in range(10):
            file.write("a"*self.width*3 + "\n")
        for i in range(Y):
            first_impermeable1, permeable1, last_impermeable1 = self.calculateBlock(self.width, 1, False)
            first_impermeable2, permeable2, last_impermeable2 = self.calculateBlock(self.width, last_impermeable1, False)
            first_impermeable3, permeable3, last_impermeable3 = self.calculateBlock(self.width, last_impermeable2, True)

            if first_impermeable1 + (permeable1 - 2) <= hole1_1 or first_impermeable1 >= hole1_2:
                continue
            if first_impermeable2 + (permeable2 - 2) <= hole2_1 or first_impermeable2 >= hole2_2:
                continue
            if first_impermeable3 + (permeable3 - 1) <= hole3_1 or first_impermeable3 >= hole3_2:
                continue

            if running_number == 1:
                self.pool.append('b')
            if running_number == 5:
                self.pool.append('b')
                self.pool.append('l')
            if running_number == 10:
                self.pool.append('b')
                self.pool.append('l')
                self.pool.append('g')
            if running_number == 20:
                self.pool.append('l')
                self.pool.append('g')
            if running_number == 30:
                self.pool.append('g')
            if running_number == 40:
                self.pool.append('r')
            if running_number == 50:
                self.pool.append('r')
            if running_number == 60:
                self.pool.append('r')
                self.pool.append('d')
            if running_number == 80:
                self.pool.append('d')
            if running_number == 100:
                self.pool.append('d')
                self.pool.append('o')
                self.pool.append('w')
            if running_number == 120 or running_number == 140 or running_number == 160 or running_number == 180:
                self.pool.append('g')
                self.pool.append('r')
                self.pool.append('d')
                self.pool.append('o')

            # select one random mineral from pool per every loop
            if len(self.pool) != 0:
                mineral = random.choice(self.pool)
                if mineral == 'w':
                    self.pool.remove(mineral)
            # if winning golden bone doesn't exist in level 130, put in there (this is the last level it can be)
            if running_number == 130 and 'w' in self.pool:
                mineral = 'w'
                self.pool.remove(mineral)

            sand_1, sand_2, sand_3 = list('s'*permeable1), list('s'*permeable2), list('s'*permeable3)
            # calculate length of all sands
            length_of_sands = len(sand_1) + len(sand_2) + len(sand_3)
            # get random index for the mineral
            mineral_insert_index = random.randint(1, length_of_sands - 1)

            # if index in not in first sand
            if mineral_insert_index > len(sand_1):
                mineral_insert_index -= len(sand_1)

                # if mineral not in second sand
                if mineral_insert_index > len(sand_2):
                    mineral_insert_index -= len(sand_2)
                    # insert in third sand
                    sand_3[mineral_insert_index - 1] = mineral
                else:
                    # insert in second sand
                    sand_2[mineral_insert_index - 1] = mineral
            else:
                # insert in first sand
                sand_1[mineral_insert_index - 1] = mineral

            # sum the lines back together
            line = "x"*first_impermeable1 + ''.join(sand_1) + "x"*last_impermeable1 +\
                   "x"*first_impermeable2 + ''.join(sand_2) + "x"*last_impermeable2 +\
                   "x"*first_impermeable3 + ''.join(sand_3) + "x"*last_impermeable3 + "\n"
            # write the line to file
            file.write(line)

            hole1_1, hole2_1, hole3_1 = first_impermeable1, first_impermeable2, first_impermeable3
            hole1_2, hole2_2, hole3_2 = permeable1-2, permeable2-2, permeable3-2

            running_number += 1

        self.height = running_number
        self.bottom = 180 + self.height*20
        file.write("x"*self.width*3)
        file.close()
        return file

    def calculateBlock(self, x, length_of_last_impermeable_wall, last_block):
        if last_block:
            length_of_permeable_wall = random.randint(3, (x - 2))       # length of permeable wall
            correction_factor = 1                   # correction factor, which only affects if this is last block
        else:
            length_of_permeable_wall = random.randint(4, (x - 1))
            correction_factor = 0
        imperm = x - length_of_permeable_wall
        if length_of_last_impermeable_wall == 0:
            first_imperm = 0                        # length of the first impermeable wall is zero if the length of the last block last wall was zero
        else:
            first_imperm = random.randint(1, imperm - correction_factor)
        last_imperm = imperm - first_imperm         # length of the last impermeable wall. Can be zero if the length of first impermeable wall = length of all impermeable wall
        return first_imperm, length_of_permeable_wall, last_imperm