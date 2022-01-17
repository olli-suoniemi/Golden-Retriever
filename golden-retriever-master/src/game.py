from world import World
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from player import Player
from tile import Tile
import sys

class Game(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGame()

    def initGame(self):
        self.world = World()
        self.world.setSceneRect(20, 0, self.world.width * 20 * 3, 220 + self.world.height * 20)
        self.view = QtWidgets.QGraphicsView(self.world)
        self.view.setFixedSize(1200, 800)
        self.timer = Qt.QTimer()
        self.square_size = 20


        while self.world.height < 150:
            self.world.map = self.world.generateMap()
        self.draw_world(self.world.map)

        self.view.adjustSize()
        self.view.scale(4, 4)
        self.view.setVerticalScrollBarPolicy(1)
        self.view.setHorizontalScrollBarPolicy(1)
        self.view.setWindowTitle("GoldenBone")
        self.view.setWindowIcon(Qt.QIcon("sprites/minerals/goldenbone.png"))

        self.playlist = Qt.QMediaPlaylist()
        self.playlist.addMedia(Qt.QMediaContent(Qt.QUrl.fromLocalFile("sounds/music.mp3")))
        self.playlist.setPlaybackMode(Qt.QMediaPlaylist.Loop)
        self.music_player = Qt.QMediaPlayer()
        self.music_player.setPlaylist(self.playlist)
        self.music_player.setVolume(30)
        self.music_player.play()

        self.player = Player(self.world.bottom, self.world, self.view, self.music_player)  # QGraphicsPixMapItem
        self.player.setPos(40, 180)
        self.player.setPixmap(QtGui.QPixmap("sprites/dog/standing_right.png"))
        self.world.addItem(self.player)
        self.view.centerOn(self.player.scenePos())

        self.player.grabKeyboard()

        self.view.show()

    def draw_world(self, map):
        x_c = -self.square_size
        y_c = -self.square_size
        level = -1
        try:
            with open(map.name) as file:
                while True:
                    line = file.readline()
                    y_c += self.square_size
                    x_c = 0
                    if not line:
                        break
                    if line != "\n":
                        if line[0] != 'a':
                            level += 1
                        line = line.rstrip()
                        for i in line:
                            x_c += self.square_size
                            if i == "a":
                                air = Tile(self.square_size, x_c, y_c, "a", level)
                                self.world.addItem(air)
                            elif i == "x":
                                wall = Tile(self.square_size, x_c, y_c, "x", level)
                                self.world.addItem(wall)
                            elif i == 's':
                                sand = Tile(self.square_size, x_c, y_c, "s", level)
                                self.world.addItem(sand)
                            elif i == 'b':
                                bronze = Tile(self.square_size, x_c, y_c, "b", level)
                                self.world.addItem(bronze)
                            elif i == 'l':
                                silver = Tile(self.square_size, x_c, y_c, "l", level)
                                self.world.addItem(silver)
                            elif i == 'g':
                                gold = Tile(self.square_size, x_c, y_c, "g", level)
                                self.world.addItem(gold)
                            elif i == 'r':
                                ruby = Tile(self.square_size, x_c, y_c, "r", level)
                                self.world.addItem(ruby)
                            elif i == 'd':
                                diamond = Tile(self.square_size, x_c, y_c, "d", level)
                                self.world.addItem(diamond)
                            elif i == 'o':
                                opal = Tile(self.square_size, x_c, y_c, "o", level)
                                self.world.addItem(opal)
                            elif i == 'w':
                                golden_bone = Tile(self.square_size, x_c, y_c, "w", level)
                                self.world.addItem(golden_bone)


        except OSError:
            print("Could not open {}".format(map.name), file=sys.stderr)