from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QString, pyqtSlot
import Style
import MyGame


class Window(QtGui.QWidget):
    def __init__(self, game, parentt):
        QtGui.QWidget.__init__(self, parent=parentt)
        self.next = self
        self.N = 10
        self.Game = game

    def show_error_message(self, msg):
        print("msg")
        exit(1)

    def Render(self, screen):
        raise NotImplementedError

    def Update(self):
        raise NotImplementedError

    def HandleEvents(self, events, pressed_key):
        raise NotImplementedError

    def SwitchToScene(self, next_scene):
        self.next = next_scene
        self.close()
        if self.next is not None:
            self.parentWidget().setCentralWidget(self.next)

    def Terminate(self):
        self.SwitchToScene(None)

    def mousePressedEvent(self, QMouseEvent):
        print QMouseEvent.pos()

    def mouseReleaseEvent(self, QMouseEvent):
        cursor = QtGui.QCursor()
        print cursor.pos()


class TitleWindow(Window):
    def __init__(self, game):
        Window.__init__(self, game, mainWindow)
        self.next = self

        self.setWindowTitle('Window 1')
        pixmap = QtGui.QPixmap(START)
        self.bg = QtGui.QLabel(self)
        self.bg.setPixmap(pixmap)

        # User's Name Input
        self.textbox = QtGui.QLineEdit(self)
        self.textbox.resize(280, 40)
        self.textbox.move((W-self.textbox.width())/2, (H-self.textbox.height())/2)
        self.text_button = QtGui.QPushButton('', self)
        self.text_button.setStyleSheet(Style.PlayButton)
        self.text_button.move((W-self.text_button.width())/2, 40+((H-self.text_button.height())/2))
        self.text_button.clicked.connect(self.handleTextButton)

    def handleTextButton(self):
        # Get name from the player
        text_input = self.textbox.text()
        game.the_player.name = text_input
        self.handleButton()

    def handleButton(self):
        print ('To Rule Window')
        print "Player's name: ", game.the_player.name
        self.SwitchToScene(RuleWindow(game))


class RuleWindow(Window):
    def __init__(self, game):
        Window.__init__(self, game, mainWindow)
        pixmap = QtGui.QPixmap(RULE)
        self.bg = QtGui.QLabel(self)
        self.bg.setPixmap(pixmap)
        self.button = QtGui.QPushButton("", self)
        self.button.setFixedSize(80, 30)
        self.button.clicked.connect(self.handleButton)
        self.button.setStyleSheet("""QPushButton{
                    color: grey;
                    border-image: url(artwork/arrow-yel-1.png) 3 10 3 10;
                    border-top: 3px transparent;
                    border-bottom: 3px transparent;
                    border-right: 10px transparent;
                    border-left: 10px transparent;
                }""")
        self.button.setGeometry(W / 2, H / 2, 20, 20)

    def handleButton(self):
        print ('To Random Window')
        self.SwitchToScene(RandomWindow(game))


class RandomWindow(Window):
    def __init__(self, game):
        Window.__init__(self, game, mainWindow)

        # STATIC ===============================
        pixmap = QtGui.QPixmap(BG)
        self.bg = QtGui.QLabel(self)
        self.bg.setPixmap(pixmap)

        # WIDGET ===============================
        # Go to Next screen BUTTON
        self.next_button = QtGui.QPushButton("", self)
        self.next_button.setFixedSize(80, 30)
        self.next_button.clicked.connect(self.handleNextButton)
        self.next_button.setStyleSheet(Style.DefaultStyle)
        self.next_button.setGeometry(W / 2, H / 2, 20, 20)
        self.next_button.hide()

        # Random BUTTON
        self.random_button = QtGui.QPushButton("", self)
        self.random_button.setFixedSize(80, 30)
        self.random_button.clicked.connect(self.handleRandomButton)
        self.random_button.setStyleSheet(Style.DefaultStyle)
        self.random_button.setGeometry(600, 465, 20, 20)


    def handleRandomButton(self):
        random = game.randomize_k()
        game.random_ball()
        print random
        self.next_button.show()

    def handleNextButton(self):
        print ('To Game Window')
        self.SwitchToScene(GameWindow(game))


class Field(QtGui.QWidget):
    def __init__(self, parentt, value=0):
        super(Field, self).__init__(parentt)
        self.value = value
        self.gui = QtGui.QLabel(parentt)
        self.gui.setText(str(self.value))
        text = """QLabel{   
                            font-family: times
                            font-weight: bold; 
                            color: rgb(247, 115, 109);
                        }"""
        self.gui.setStyleSheet(text)
        # X, Y of the image ball
        self.x = 0
        self.y = 0

    def up(self):
        self.value += 1
        self.gui.setText(str(self.value))

    def down(self):
        self.value -= 1
        self.gui.setText(str(self.value))


class GameWindow(Window):
    def __init__(self, game):
        Window.__init__(self, game, mainWindow)

        # STATIC: BACKGROUND + FROG ========================================
        self.bg = WriteImage(WATER, LILY, self)
        self.bg = WriteImage(self.bg, PLAYER, self, 485, 472)
        self.bg = WriteImage(self.bg, COMPA, self, 903, 81)
        self.current_bg = self.bg       # keep track of changing
        self.main_label = QtGui.QLabel(self)
        self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.bg))

        # ON/OFF/DRAWING ===================================================
        butt_w = 34
        butt_h = 35
        my_font = QtGui.QFont("Times", 48, QtGui.QFont.Bold)

        # Initiate Coordinates of the three battlefields
        self.field_A = Field(self)
        self.field_A.x = 930
        self.field_A.y = 460
        self.field_B = Field(self)
        self.field_B.x = 608
        self.field_B.y = 344
        self.field_C = Field(self)
        self.field_C.x = 700
        self.field_C.y = 230

        # Draw button A
        self.buttonA_up = QtGui.QPushButton("", self)
        self.buttonA_up.clicked.connect(lambda: self.handleUpButton(A))
        self.buttonA_up.setStyleSheet(Style.YellowButton_up)
        self.buttonA_up.setGeometry(867, 502, butt_w, butt_h)

        self.buttonA_down = QtGui.QPushButton("", self)
        self.buttonA_down.clicked.connect(lambda: self.handleDownButton(A))
        self.buttonA_down.setStyleSheet(Style.YellowButton_down)
        self.buttonA_down.setGeometry(867, 542, butt_w, butt_h)

        # Draw field A
        self.field_A.setFixedSize(50, 70)
        self.field_A.gui.setFont(my_font)
        self.field_A.gui.setGeometry(800, 500, 90, 90)

        # Draw button B
        self.buttonB_up = QtGui.QPushButton("", self)
        self.buttonB_up.clicked.connect(lambda: self.handleUpButton(B))
        self.buttonB_up.setStyleSheet(Style.PinkButton_up)
        self.buttonB_up.setGeometry(496, 347, butt_w, butt_h)

        self.buttonB_down = QtGui.QPushButton("", self)
        self.buttonB_down.clicked.connect(lambda: self.handleDownButton(B))
        self.buttonB_down.setStyleSheet(Style.PinkButton_down)
        self.buttonB_down.setGeometry(496, 387, butt_w, butt_h)

        # Draw field B
        self.field_B.setFixedSize(50, 70)
        self.field_B.gui.setFont(my_font)
        self.field_B.gui.setGeometry(445, 340, 90, 90)

        # Draw button C
        self.buttonC_up = QtGui.QPushButton("", self)
        self.buttonC_up.clicked.connect(lambda: self.handleUpButton(C))
        self.buttonC_up.setStyleSheet(Style.YellowButton_up)
        self.buttonC_up.setGeometry(881, 286, butt_w, butt_h)

        self.buttonC_down = QtGui.QPushButton("", self)
        self.buttonC_down.clicked.connect(lambda: self.handleDownButton(C))
        self.buttonC_down.setStyleSheet(Style.YellowButton_down)
        self.buttonC_down.setGeometry(881, 326, butt_w, butt_h)

        # Draw field C
        self.field_C.setFixedSize(50, 70)
        self.field_C.gui.setFont(my_font)
        self.field_C.gui.setGeometry(950, 280, 90, 90)

        # Draw PLAY BUTTON
        self.play_button = QtGui.QPushButton("", self)
        self.play_button.clicked.connect(self.handlePlayButton)
        self.play_button.setStyleSheet(Style.PlayButton)
        self.play_button.setGeometry(300, 556, 140, 70)

    @pyqtSlot(bool)
    def handlePlayButton(self):
        player_choice = (self.field_A.value, self.field_B.value, self.field_C.value)
        sum = 0
        for i in player_choice:
            sum += i
            if sum<0 or sum>self.N:
                self.show_error_message("Invalid numbers")
        game.the_player.choice = player_choice
        self.game_logic()

    def game_logic(self):
        game.the_player.choice
        game.current_level.round

    def handleUpButton(self, field):
        # Show the number of balls on each field
        print ('Up arrow pressed')
        if field is A:
            self.field_A.up()
            if self.field_A.value == 1:
                self.current_bg = WritePartImage(self.current_bg, BALLA, self, self.field_A.x, self.field_A.y)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))
        elif field is B:
            self.field_B.up()
            if self.field_B.value == 1:
                self.current_bg = WritePartImage(self.current_bg, BALLB, self, self.field_B.x, self.field_B.y)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))

        elif field is C:
            self.field_C.up()
            if self.field_C.value == 1:
                self.current_bg = WritePartImage(self.current_bg, BALLC, self, self.field_C.x, self.field_C.y)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))

        # Event, number up, down
        # self.main_label.setPixmap(QtGui.QPixmap.fromImage(current_background))
        # self.SwitchToScene(EndWindow())

    def handleDownButton(self, field):
        print("Down Arrow pressed")
        # event,, number up, down
        if field is A:
            self.field_A.down()
            if self.field_A.value == 0:
                ball_w = QtGui.QImage(BALLA).width()+50
                ball_h = QtGui.QImage(BALLA).height()+50
                self.current_bg = WritePartImage(self.current_bg, self.bg,
                                                 self, self.field_A.x-20, self.field_A.y-20, ball_w, ball_h)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))
        elif field is B:
            self.field_B.down()
            if self.field_B.value == 0:
                ball_w = QtGui.QImage(BALLB).width()+60
                ball_h = QtGui.QImage(BALLB).height()+60
                self.current_bg = WritePartImage(self.current_bg, self.bg,
                                                 self, self.field_B.x-40, self.field_B.y, ball_w, ball_h)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))

        elif field is C:
            self.field_C.down()
            if self.field_C.value == 0:
                ball_w = QtGui.QImage(BALLC).width()+60
                ball_h = QtGui.QImage(BALLC).height()+60
                self.current_bg = WritePartImage(self.current_bg, self.bg,
                                                 self, self.field_C.x-40, self.field_C.y-40, ball_w, ball_h)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))

    def drawEvent(self, curr_bg, img):
        label = QtGui.QLabel(self)
        label.setPixmap(QtGui.QPixmap.fromImage(curr_bg))
        return label


class EndWindow(Window):
    def __init__(self):
        Window.__init__(self, mainWindow)
        pixmap = QtGui.QPixmap(RULE)
        self.bg = QtGui.QLabel(self)
        self.bg.setPixmap(pixmap)
        self.button = QtGui.QPushButton("", self)
        self.button.setFixedSize(80, 30 )
        self.button.clicked.connect(self.handleButton)
        self.button.setStyleSheet("""QPushButton{
                    color: grey;
                    border-image: url(artwork/arrow-yel-1.png) 3 10 3 10;
                    border-top: 3px transparent;
                    border-bottom: 3px transparent;
                    border-right: 10px transparent;
                    border-left: 10px transparent;
                }""")
        self.button.setGeometry(W / 2, H / 2, 20, 20)

    def handleButton(self):
        print ('Hello World')
        self.SwitchToScene(a)


class Label(QtGui.QLabel):
    def __init__(self, img, parent=None):
        super(Label, self).__init__(parent=parent)
        self.overlay = QtGui.QImage(img)

    def paintEvent(self, x=0, y=0):
        qp = QtGui.QPainter(self)
        qp.drawPixmap(x, y, QtGui.QPixmap(self.overlay))
        return qp

# def WriteLabel(label, over_img, parent, x=0, y=0):
#     overlay = QtGui.QImage(over_img)
#     qp = QtGui.QPainter(label)
#     qp.drawPixmap(x, y, QtGui.QPixmap(overlay))
#     return qp


# CHECL WRITEPARTIMAGE
def WritePartImage(img, over, parent, x, y, over_w=0, over_h=0):
    # image = img
    # over_w and h are for delete ball, over_w and h are the dimension of the areas you want to erase
    image = QtGui.QImage(img)
    over1 = QtGui.QImage(over)
    # Rect with position x,y,w,h to crop of overlay
    if over1.size() < image.size():
        rect = QtCore.QRect(0, 0, over1.width(), over1.height())
    else:
        rect = QtCore.QRect(x, y, over_w, over_h)

    #crop the desireable part to draw on the image
    overlay = over1.copy(rect)

    painter = QtGui.QPainter()
    painter.begin(image)
    painter.drawImage(x, y, overlay)
    painter.end()

    return image    #QPixmap


def WriteImage(img, over, parent, x=0, y=0):
    # image = img
    image = QtGui.QImage(img)
    overlay = QtGui.QImage(over)

    if overlay.size() > image.size():
        overlay = overlay.scaled(image.size(), Qt.KeepAspectRatio)

    painter = QtGui.QPainter()
    painter.begin(image)
    painter.drawImage(x, y, overlay)
    painter.end()
    return image
    # label = QtGui.QLabel(parent)
    # label.setPixmap(QtGui.QPixmap.fromImage(image))
    # return label

# class MainWindow(QtGui.QMainWindow):
#     def __init__(self, surface, parent=None):
#         super(MainWindow, self).__init__(parent)
#         # self.layout = None
#         self.initUI(surface)
#
#     def initUI(self,surface):
#         self.setWindowTitle('Window 1')
#         # background.setStyleSheet("""
#         #                         .QtGui.QMainWindow {
#         #
#         #                             background-image: url(:/artwork/BG/bg-background.png);}
#         #
#         #                     """)
#
#         background = QtGui.QHBoxLayout(self)
#         background.addWidget(ImageWidget(surface), Qt.AlignHCenter)
#
#         # button = QtGui.QPushButton('Next')
#         # button.clicked.connect(self.handleButton)
#         # button_layout = QtGui.QHBoxLayout()
#         # button_layout.addWidget(button, Qt.AlignHCenter)
#
#         layout = QtGui.QVBoxLayout(self)
#         layout.addLayout(background)
#         # layout.addLayout(button_layout)
#
#         # self.setLayout(layout)
#
#     def handleButton(self):
#
#         print("He")
#         # self.setCentralWidget(ImageWidget(surface))


import sys

from MyGame import *
from MyDefinition import *


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    game = Game()   # Initiate main Game
    mainWindow = QtGui.QMainWindow()
    mainWindow.setCentralWidget(TitleWindow(game))
    mainWindow.setGeometry(0, 0, W, H)
    mainWindow.show()
    sys.exit(app.exec_())
