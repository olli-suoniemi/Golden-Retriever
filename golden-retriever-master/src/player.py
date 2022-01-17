from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import random
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
class Player(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, bottom, world, view, music):
        super(Player, self).__init__()
        self.bottom = bottom
        self.world = world
        self.view = view
        self.music = music
        self.speed = 0.8
        self.fan_speed = 1
        self.counter_right, self.counter_left, self.counter_down = 0, 0, 0
        self.drill = 1
        self.finished = False
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_walking = False
        self.is_digging_down = False
        self.is_digging_right = False
        self.is_digging_left = False
        self.is_flying = False
        self.is_centering = False
        self.is_jumping = False
        self.is_falling = False
        self.high_fall = False
        self.facing = "right"
        self.timer = Qt.QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.timerEvent)
        self.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)

        self.spriteTimer = Qt.QTimer()
        self.spriteTimer.start(80)
        self.spriteTimer.timeout.connect(self.updateSprite)
        self.moving_number = 0
        self.standing_number = 0

        #Gravity
        self.gravity = 1.5
        self.y_speed = 0
        self.acceleration = 0

        self.hp = 100
        self.points = 0
        self.inventory = []
        self.weight = 0

        self.wuf = Qt.QSoundEffect()
        self.digging_sound = Qt.QSoundEffect()
        self.winning_bark = Qt.QSoundEffect()
        self.flying_sound = Qt.QSoundEffect()
        self.losing_music = Qt.QMediaPlayer()
        self.damage = Qt.QSoundEffect()
        self.wuf.setSource(Qt.QUrl.fromLocalFile("sounds/wuf.wav"))
        self.digging_sound.setSource(Qt.QUrl.fromLocalFile("sounds/digging.wav"))
        self.flying_sound.setSource(Qt.QUrl.fromLocalFile("sounds/fly_sound.wav"))
        self.damage.setSource(Qt.QUrl.fromLocalFile("sounds/damage.wav"))
        self.digging_sound.setVolume(0.2)
        self.flying_sound.setVolume(0.1)
        self.damage.setVolume(0.2)
        self.winning_bark.setSource(Qt.QUrl.fromLocalFile("sounds/winning_bark.wav"))
        self.losing_music.setMedia(Qt.QMediaContent(Qt.QUrl.fromLocalFile("sounds/game_over_music.mp3")))

        self.fond_id = QtGui.QFontDatabase.addApplicationFont("fonts/Freckle_Face/FreckleFace-Regular.ttf")
        self.font = QtGui.QFont(QtGui.QFontDatabase.applicationFontFamilies(self.fond_id)[0], 10)
        # self.font = Qt.QFont('Arial', 10)         # change font to this if game is laggy
        self.score = self.updateScore(self.points, self.font)
        self.health = self.updateHealth(self.hp, self.font)

        self.score.setPos(self.view.mapToScene(0, 0).x(), self.view.mapToScene(0, 0).y())
        self.health.setPos(self.view.mapToScene(0, 0).x() + 230, self.view.mapToScene(0, 0).y())

        self.world.addItem(self.score)
        self.world.addItem(self.health)

        self.game_over = False

    def roundup(self, x):
        return round(int((x + 9) / 20) * 20)

    def updateSprite(self):
        # animate idling
        if not self.is_digging_left and not self.is_digging_right and not self.is_digging_down and not self.is_moving_left and not self.is_flying and not self.is_moving_right:
            self.is_walking = False
            self.standing_number += 1
            if self.standing_number >= 10:
                if random.randint(1, 10) == self.standing_number:
                    self.wuf.play()
                if self.facing == "right":
                    self.setPixmap(QtGui.QPixmap("sprites/dog/standing_right.png"))
                else:
                    self.setPixmap(QtGui.QPixmap("sprites/dog/standing_left.png"))
                self.standing_number = 0

        # animate digging or walking to right
        if self.is_moving_right:
            self.standing_number = 0
            self.moving_number += 1
            if not self.is_digging_right:
                path = "sprites/dog/walking_right_" + str(self.moving_number) + ".png"
            else:
                path = "sprites/dog/digging_right_" + str(self.moving_number) + ".png"
            self.setPixmap(QtGui.QPixmap(path))
            if self.moving_number == 3:
                self.moving_number = 0

        # animate digging or walking to left
        if self.is_moving_left:
            self.standing_number = 0
            self.moving_number += 1
            if not self.is_digging_left:
                path = "sprites/dog/walking_left_" + str(self.moving_number) + ".png"
            else:
                path = "sprites/dog/digging_left_" + str(self.moving_number) + ".png"
            self.setPixmap(QtGui.QPixmap(path))
            if self.moving_number == 3:
                self.moving_number = 0

        # animate digging down
        if self.is_digging_down:
            self.standing_number = 0
            self.moving_number += 1
            path = "sprites/dog/digging_down_" + str(self.moving_number) + ".png"
            self.setPixmap(QtGui.QPixmap(path))
            if self.moving_number == 3:
                self.moving_number = 0

        # animate flying
        if self.is_flying:
            self.standing_number = 0
            self.moving_number += 1
            if self.facing == "right":
                path = "sprites/dog/flying_right_" + str(self.moving_number) + ".png"
            else:
                path = "sprites/dog/flying_left_" + str(self.moving_number) + ".png"
            self.setPixmap(QtGui.QPixmap(path))
            if self.moving_number == 3:
                self.moving_number = 0

        # animate falling
        if self.is_falling:
            self.standing_number = 0
            self.moving_number += 1
            if self.y_speed >= 1.4:
                self.high_fall = True
                if self.facing == "right":
                    path = "sprites/dog/falling_right_" + str(self.moving_number) + ".png"
                else:
                    path = "sprites/dog/falling_left_" + str(self.moving_number) + ".png"
                self.setPixmap(QtGui.QPixmap(path))
            if self.moving_number == 3:
                self.moving_number = 0

    def updateScore(self, points, font):
        score = Qt.QGraphicsTextItem("Points:" + str(points))
        score.setDefaultTextColor(Qt.QColor(240, 224, 0))       # yellow
        score.setFont(font)
        return score

    def updateHealth(self, hp, font):
        health = Qt.QGraphicsTextItem("Health:" + str(hp))
        health.setDefaultTextColor(Qt.QColor(254, 178, 183))    # pink
        health.setFont(font)
        return health

    def updateDiggingSprite(self, target, counter):
        for i in range(1, 6):
            if target.getDigtime() * ((i-1) / 5) < counter <= target.getDigtime() * (i / 5):
                if target.getType() == 's':
                    if target.getLevel() != 0:
                        target.setPixmap(QtGui.QPixmap("sprites/minerals/sand_digging_" + str(i) + ".png"))
                    else:
                        target.setPixmap(QtGui.QPixmap("sprites/minerals/top_sand_digging_" + str(i) + ".png"))
                elif target.getType() == 'b':
                    target.setPixmap(QtGui.QPixmap("sprites/minerals/bronze_digging_" + str(i) + ".png"))
                elif target.getType() == 'l':
                    target.setPixmap(QtGui.QPixmap("sprites/minerals/silver_digging_" + str(i) + ".png"))
                elif target.getType() == 'g':
                    target.setPixmap(QtGui.QPixmap("sprites/minerals/gold_digging_" + str(i) + ".png"))
                elif target.getType() == 'r':
                    target.setPixmap(QtGui.QPixmap("sprites/minerals/ruby_digging_" + str(i) + ".png"))
                elif target.getType() == 'd':
                    target.setPixmap(QtGui.QPixmap("sprites/minerals/diamond_digging_" + str(i) + ".png"))
                elif target.getType() == 'o':
                    target.setPixmap(QtGui.QPixmap("sprites/minerals/opal_digging_" + str(i) + ".png"))
                elif target.getType() == 'w':
                    target.setPixmap(QtGui.QPixmap("sprites/minerals/goldenbone_digging_" + str(i) + ".png"))

    def showGameOver(self):
        if 'w' in self.inventory:
            text = Qt.QGraphicsTextItem("             YOU WIN!\n   CONGRATULATIONS!")
            color = Qt.QColor(166, 235, 98)
            self.winning_bark.play()
        else:
            text = Qt.QGraphicsTextItem("              YOU LOSE!\n BETTER LUCK NEXT TIME!")
            color = Qt.QColor(255, 120, 120)
            self.music.stop()
            self.losing_music.play()

        # disable all items in scene
        for i in self.world.items():
            i.setEnabled(False)
        # draw a game over panel
        panel_background = self.drawPanel(self.view.mapToScene(0, 0).x(), self.view.mapToScene(0, 0).y(), self.view.viewport().size().width(), self.view.viewport().size().height(), Qt.QColor(0, 0, 0), 0.5)    # black background
        panel_foreground = self.drawPanel(self.view.mapToScene(0, 0).x() + 50, self.view.mapToScene(0, 0).y() + 50, 200, 100, color, 0.5)
        text.setFont(self.font)
        text.setPos(self.view.mapToScene(380 - text.boundingRect().width() / 2, 320 - text.boundingRect().height() / 2))
        self.world.addItem(panel_background)
        self.world.addItem(panel_foreground)
        self.world.addItem(text)

    def drawPanel(self, x_0, y_0, x, y, color, opacity):
        panel = Qt.QGraphicsRectItem(x_0, y_0, x, y)
        brush = Qt.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(color)
        panel.setBrush(brush)
        panel.setOpacity(opacity)
        return panel

    def timerEvent(self):
        if self.is_flying:
            if not self.flying_sound.isPlaying():
                # self.flying_sound.play()     # causes game to lag
                pass
        if not self.game_over:
            # check if player collides with hud in all directions, up, down, right, left:
            if self.score.collidesWithItem(self.world.itemAt(self.scenePos().x(), self.scenePos().y() - 1, QtGui.QTransform())) or self.score.collidesWithItem(self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() - 1, QtGui.QTransform())) \
                    or self.score.collidesWithItem(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform())) or self.score.collidesWithItem(self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform())) \
                    or self.score.collidesWithItem(self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform())) or self.score.collidesWithItem(self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform())) \
                    or self.score.collidesWithItem(self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform())) or self.score.collidesWithItem(self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform())):
                self.score.setVisible(0)
            else:
                self.score.setVisible(1)

            if self.health.collidesWithItem(self.world.itemAt(self.scenePos().x(), self.scenePos().y() - 1, QtGui.QTransform())) or self.health.collidesWithItem(self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() - 1, QtGui.QTransform())) \
                    or self.health.collidesWithItem(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform())) or self.health.collidesWithItem(self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform())) \
                    or self.health.collidesWithItem(self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform())) or self.health.collidesWithItem(self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform())) \
                    or self.health.collidesWithItem(self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform())) or self.health.collidesWithItem(self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform())):
                self.health.setVisible(0)
            else:
                self.health.setVisible(1)

            if self.y_speed > 0:
                self.is_falling = True
            else:
                self.is_falling = False
            if self.is_digging_down or self.is_digging_left or self.is_digging_right:
                if not self.digging_sound.isPlaying():
                    self.digging_sound.play()

            # if below is dug ground and not flying ->
            if self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug() and self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug() and not self.is_flying:
                # gravity affects
                y = self.scenePos().y()     # get current y coordinate
                self.y_speed = self.acceleration * self.gravity    # y_speed is based on acceleration and gravity
                y += self.y_speed       # y coordinate increases basing on y_speed
                self.setPos(self.scenePos().x(), y)     # setting player to new position
                if self.acceleration <= 6:
                    self.acceleration += 0.04           # amount acceleration increases per every loop

                # if hit floor
                if not self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug() or not self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug():
                    if self.high_fall:
                        if self.y_speed >= 3:
                            self.damage.play()
                            self.hp -= int(self.y_speed * 3)
                            self.world.removeItem(self.health)
                            self.health = self.updateHealth(self.hp, self.font)
                            self.world.addItem(self.health)

                            # animate damage
                            if self.facing == "right":
                                self.setPixmap(QtGui.QPixmap("sprites/dog/standing_right_damage.png"))
                            else:
                                self.setPixmap(QtGui.QPixmap("sprites/dog/standing_left_damage.png"))
                        else:
                            if self.facing == "right":
                                self.setPixmap(QtGui.QPixmap("sprites/dog/standing_right.png"))
                            else:
                                self.setPixmap(QtGui.QPixmap("sprites/dog/standing_left.png"))
                    self.is_falling = False
                    self.high_fall = False
                    self.y_speed = 0
                    self.acceleration = 0
                    self.setPos(self.world.itemAt(self.scenePos().x(), self.scenePos().y(), QtGui.QTransform()).scenePos().x(), self.roundup(self.world.itemAt(self.scenePos().x(), self.scenePos().y()+10, QtGui.QTransform()).scenePos().y()))
                    self.view.centerOn(self.scenePos())

            if self.is_centering:
                self.setPos(self.roundup(self.world.itemAt(self.scenePos().x()+10, self.scenePos().y(), QtGui.QTransform()).scenePos().x()), self.roundup(self.world.itemAt(self.scenePos().x(), self.scenePos().y()+10, QtGui.QTransform()).scenePos().y()))

            # is walking right ->
            if self.is_moving_right and self.scenePos().x() < 1780 and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getDug() and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform()).getDug():
                if not self.is_flying and not self.is_falling and not self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug():
                    self.is_walking = True
                else:
                    self.is_walking = False
                self.is_digging_right = False
                self.setPos(self.scenePos().x() + self.speed, self.scenePos().y())
                self.counter_left, self.counter_down = 0, 0

            # is digging right ->
            # if right_top is not dug or right_bottom is not dug and below is NOT dug ground
            if self.is_moving_right and self.scenePos().x() < 1780 \
                    and not self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform()).getDug() \
                    and not self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug()\
                    and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getType() != 'x' and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform()).getType() != 'x':
                self.counter_left, self.counter_down = 0, 0
                self.is_digging_right = True
                self.is_walking = False
                # focus on player
                self.view.centerOn(self.scenePos())
                # if on right is wall, do not dig !!
                if self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform()).getType() == 'x':
                    return

                # center the player
                self.setPos(self.roundup(self.world.itemAt(self.scenePos().x() + 10, self.scenePos().y(), QtGui.QTransform()).scenePos().x()), self.roundup(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 10, QtGui.QTransform()).scenePos().y()))
                # focus on player
                self.view.centerOn(self.scenePos())

                # if after centering the player, on right is wall, do not dig !!
                if self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform()).getType() == 'x':
                    return

                # dig
                self.counter_right += self.drill
                self.updateDiggingSprite(self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()), self.counter_right)
                if self.counter_right >= self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getDigtime():
                    self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).setPixmap(QtGui.QPixmap("sprites/minerals/dug_sand.png"))
                    self.points += self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getValue()
                    self.inventory.append(self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getType())

                    self.world.removeItem(self.score)
                    self.score = self.updateScore(self.points, self.font)
                    self.world.addItem(self.score)

                    self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).setDug()
                    self.is_digging_right = False
                    # center the player
                    self.setPos(self.roundup(self.world.itemAt(self.scenePos().x() + 10, self.scenePos().y(), QtGui.QTransform()).scenePos().x()), self.roundup(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 10, QtGui.QTransform()).scenePos().y()))
                    # focus on player
                    self.view.centerOn(self.scenePos())
                    self.counter_right = 0

            # is walking left ->
            if self.is_moving_left and self.scenePos().x() > 40 and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getDug() and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getDug():
                if not self.is_flying and not self.is_falling and not self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug() \
                        and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getType() != 'x' and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getType() != 'x' \
                        and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getType() != 'x' and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform()).getType() != 'x':
                    self.is_walking = True
                else:
                    self.is_walking = False
                self.is_digging_right = False
                self.is_digging_left = False
                self.setPos(self.scenePos().x() - self.speed, self.scenePos().y())
                self.counter_right, self.counter_down = 0, 0

            # digging left ->
            # if left_top is not dug or left_bottom is not dug and below is NOT dug ground
            if self.is_moving_left and self.scenePos().x() > 40 \
                    and not self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getDug() \
                    and not self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug() \
                    and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getType() != 'x' and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getType() != 'x':
                self.counter_right, self.counter_down = 0, 0
                self.is_walking = False
                # focus on player
                self.view.centerOn(self.scenePos())
                # if on left is wall, do not dig !!
                if self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getType() == 'x':
                    return

                # center the player
                self.setPos(self.roundup(self.world.itemAt(self.scenePos().x() + 10, self.scenePos().y(), QtGui.QTransform()).scenePos().x()), self.roundup(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 10, QtGui.QTransform()).scenePos().y()))
                self.is_digging_left = True
                # focus on player
                self.view.centerOn(self.scenePos())

                # if after centering the player, on left is wall, do not dig !!
                if self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getType() == 'x':
                    return

                # finally, if on left is not dug ground -> dig it
                if not self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getDug():
                    self.counter_left += self.drill
                    self.updateDiggingSprite(self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()), self.counter_left)

                    if self.counter_left >= self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getDigtime():
                        self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).setPixmap(QtGui.QPixmap("sprites/minerals/dug_sand.png"))
                        self.points += self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getValue()
                        self.inventory.append(self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getType())

                        self.world.removeItem(self.score)
                        self.score = self.updateScore(self.points, self.font)
                        self.world.addItem(self.score)

                        self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).setDug()
                        self.is_digging_left = False
                        # center the player
                        self.setPos(self.roundup(self.world.itemAt(self.scenePos().x() + 10, self.scenePos().y(), QtGui.QTransform()).scenePos().x()), self.roundup(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 10, QtGui.QTransform()).scenePos().y()))
                        # focus on player
                        self.view.centerOn(self.scenePos())
                        self.counter_left = 0

            # is digging down ->
            # if down_left is not dug or below_right is not dug
            if (self.is_digging_down and not self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug()) or (self.is_digging_down and not self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug()):
                self.counter_right, self.counter_left = 0, 0
                self.is_walking = False
                # focus on player
                self.view.centerOn(self.scenePos())
                # if below is wall, do not dig !!
                if self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getType() == 'x':
                    self.is_digging_down = False
                    return

                # center the player
                self.setPos(self.roundup(self.world.itemAt(self.scenePos().x() + 10, self.scenePos().y(), QtGui.QTransform()).scenePos().x()), self.roundup(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 10, QtGui.QTransform()).scenePos().y()))
                # focus on player
                self.view.centerOn(self.scenePos())

                # if after centering the player, below is wall, do not dig !!
                if self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getType() == 'x':
                    return

                # finally, if below is not dug ground -> dig it
                if not self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDug() and not self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() + 20, QtGui.QTransform()).getDug():
                    self.counter_down += self.drill

                    self.updateDiggingSprite(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()), self.counter_down)

                    if self.counter_down >= self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getDigtime():
                        self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).setPixmap(QtGui.QPixmap("sprites/minerals/dug_sand.png"))
                        self.points += self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getValue()
                        self.inventory.append(self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).getType())

                        self.world.removeItem(self.score)
                        self.score = self.updateScore(self.points, self.font)
                        self.world.addItem(self.score)

                        self.world.itemAt(self.scenePos().x(), self.scenePos().y() + 20, QtGui.QTransform()).setDug()
                        self.counter_down = 0

            # if above not ground -> fly
            if self.is_flying and self.world.itemAt(self.scenePos().x(), self.scenePos().y() - 1, QtGui.QTransform()).getDug() and self.world.itemAt(self.scenePos().x() + 19, self.scenePos().y() - 1, QtGui.QTransform()).getDug() and self.scenePos().y() > 20:
                self.is_walking = False
                self.setPos(self.scenePos().x(), self.scenePos().y() - self.fan_speed)
                self.acceleration = 0           # make zero, if not acceleration, would get stacked and never zeroed when not hitting floor or roof
                self.y_speed = 0

            # focus on player
            self.view.centerOn(self.scenePos())

            if self.hp < 0:
                self.world.removeItem(self.health)
                self.health = self.updateHealth(0, self.font)
                self.world.addItem(self.health)
                if self.facing == "right":
                    self.setPixmap(QtGui.QPixmap("sprites/dog/standing_right_damage.png"))
                else:
                    self.setPixmap(QtGui.QPixmap("sprites/dog/standing_left_damage.png"))
                self.game_over = True

            # update HUD
            self.score.setPos(self.view.mapToScene(0, 0).x(), self.view.mapToScene(0, 0).y())
            self.health.setPos(self.view.mapToScene(self.view.width(), 0).x() - 75, self.view.mapToScene(0, 0).y())
            if 'w' in self.inventory:
                self.game_over = True
        else:
            self.showGameOver()
            self.timer.stop()
            self.spriteTimer.stop()

    def keyPressEvent(self, event):
        if not self.game_over:
            if event.key() == QtCore.Qt.Key_Space:
                self.is_jumping = True
            if event.key() == QtCore.Qt.Key_C:
                if self.is_falling or self.is_flying:
                    self.is_centering = False
                else:
                    self.is_centering = True
            if event.key() == QtCore.Qt.Key_Right:
                if self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y() + 19, QtGui.QTransform()).getType() == 'x':
                    self.is_moving_right = False
                    self.is_walking = False
                elif self.world.itemAt(self.scenePos().x() + 20, self.scenePos().y(), QtGui.QTransform()).scenePos().x() > 1780:
                    self.is_moving_right = False
                else:
                    self.is_moving_right = True
                self.facing = "right"
            if event.key() == QtCore.Qt.Key_Left:
                if self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).getType() == 'x' and self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y() + 19, QtGui.QTransform()).getType() == 'x':
                    self.is_moving_left = False
                    self.is_walking = False
                elif self.world.itemAt(self.scenePos().x() - 1, self.scenePos().y(), QtGui.QTransform()).scenePos().x() < 40:
                    self.is_moving_left = False
                else:
                    self.is_moving_left = True
                self.facing = "left"
            if event.key() == QtCore.Qt.Key_Down:
                self.is_digging_down = True
            elif event.key() == QtCore.Qt.Key_Up:
                if self.world.itemAt(self.scenePos().x(), self.scenePos().y() - 1, QtGui.QTransform()).scenePos().y() < 20:
                    self.is_flying = False
                else:
                    self.is_flying = True

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_C:
            self.is_centering = False
        if event.key() == QtCore.Qt.Key_Right:
            self.is_moving_right = False
            self.is_digging_right = False
        if event.key() == QtCore.Qt.Key_Left:
            self.is_moving_left = False
            self.is_digging_left = False
        if event.key() == QtCore.Qt.Key_Down:
            self.is_digging_down = False
        elif event.key() == QtCore.Qt.Key_Up:
            self.is_flying = False


