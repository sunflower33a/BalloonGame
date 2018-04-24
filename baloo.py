# import pygame, sys
# from pygame.locals import *
# import pygame_textinput
# from MyFont import Peas, Orange, Slab
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QString
# from PyQt4.QtGui import QImage, QPainter
# from PyQt4.QtGui import QPixmap
import Style

from PyGame import *

class Window(QtGui.QWidget):
    def __init__(self, parentt):
        QtGui.QWidget.__init__(self, parent=parentt)
        self.next = self
        self.N = 10

    def show_error_message(self):
        pass

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
    def __init__(self):
        Window.__init__(self, mainWindow)
        self.next = self
        self.setWindowTitle('Window 1')
        pixmap = QtGui.QPixmap(START)
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
        self.button.setGeometry(W/2, H/2, 20, 20)

    def handleButton(self):
        print ('To Rule Window')
        self.SwitchToScene(RuleWindow())


class RuleWindow(Window):
    def __init__(self):
        Window.__init__(self, mainWindow)
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
        self.SwitchToScene(RandomWindow())


class RandomWindow(Window):
    def __init__(self):
        Window.__init__(self, mainWindow)
        pixmap = QtGui.QPixmap(BG)
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
        print ('To Game Window')
        self.SwitchToScene(GameWindow())


class Field(QtGui.QWidget):
    def __init__(self, parentt, value=0):
        super(Field, self).__init__(parentt)
        self.value = value
        self.gui = QtGui.QLabel(parentt)
        self.gui.setText(str(self.value))
        text = """QLabel{
                            font-weight: bold; 
                            color: blue;
                        }"""
        self.gui.setStyleSheet(text)

    def up(self):
        self.value += 1
        self.gui.setText(str(self.value))

    def down(self):
        self.value -= 1
        self.gui.setText(str(self.value))


class GameWindow(Window):
    def __init__(self):
        Window.__init__(self, mainWindow)
        # BACKGROUND + FROG ========================================
        self.bg = WriteImage(WATER, LILY, self)
        self.bg = WriteImage(self.bg, PLAYER, self, 485, 472)
        self.bg = WriteImage(self.bg, COMPA, self, 903, 81)
        self.current_bg = self.bg       # keep track of changing
        self.main_label = QtGui.QLabel(self)
        self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.bg))
        # STATIC ===================================================

        butt_w = 34
        butt_h = 35

        self.field_A = Field(self)
        self.field_B = Field(self)
        self.field_C = Field(self)
        my_font = QtGui.QFont("Times", 48, QtGui.QFont.Bold)

        self.buttonA_up = QtGui.QPushButton("", self)
        self.buttonA_up.clicked.connect(lambda: self.handleUpButton(A))
        self.buttonA_up.setStyleSheet(Style.YellowButton_up)
        self.buttonA_up.setGeometry(867, 502, butt_w, butt_h)

        self.buttonA_down = QtGui.QPushButton("", self)
        self.buttonA_down.clicked.connect(lambda: self.handleDownButton(A))
        self.buttonA_down.setStyleSheet(Style.YellowButton_down)
        self.buttonA_down.setGeometry(867, 542, butt_w, butt_h)

        self.field_A.setFixedSize(50, 70)
        self.field_A.gui.setFont(my_font)
        self.field_A.gui.setGeometry(800, 500, 90, 90)

        self.buttonB_up = QtGui.QPushButton("", self)
        self.buttonB_up.clicked.connect(lambda: self.handleUpButton(B))
        self.buttonB_up.setStyleSheet(Style.PinkButton_up)
        self.buttonB_up.setGeometry(496, 347, butt_w, butt_h)

        self.buttonB_down = QtGui.QPushButton("", self)
        self.buttonB_down.clicked.connect(lambda: self.handleDownButton(B))
        self.buttonB_down.setStyleSheet(Style.PinkButton_down)
        self.buttonB_down.setGeometry(496, 387, butt_w, butt_h)

        self.field_B.setFixedSize(50, 70)
        self.field_B.gui.setFont(my_font)
        self.field_B.gui.setGeometry(445, 340, 90, 90)

        self.buttonC_up = QtGui.QPushButton("", self)
        self.buttonC_up.clicked.connect(lambda: self.handleUpButton(C))
        self.buttonC_up.setStyleSheet(Style.YellowButton_up)
        self.buttonC_up.setGeometry(881, 286, butt_w, butt_h)

        self.buttonC_down = QtGui.QPushButton("", self)
        self.buttonC_down.clicked.connect(lambda: self.handleDownButton(C))
        self.buttonC_down.setStyleSheet(Style.YellowButton_down)
        self.buttonC_down.setGeometry(881, 326, butt_w, butt_h)

        self.field_C.setFixedSize(50, 70)
        self.field_C.gui.setFont(my_font)
        self.field_C.gui.setGeometry(820, 280, 90, 90)

        self.play_button = QtGui.QPushButton("", self)
        self.play_button.clicked.connect(self.handlePlayButton)
        # self.play_button.setStyleSheet()
        self.play_button.setGeometry(W/2, H/2, butt_w, butt_h)


    def handlePlayButton(self):
        player_choice = (self.field_A.value, self.field_B.value, self.field_C.value)
        sum=0
        for i in player_choice:
            sum += i
            if sum<0 or sum>self.N:
                self.show_error_message("Invalid numbers")

        print player_choice

    # def up(self):
    #     pass
    #
    # def down(self):
    #     pass

    def handleUpButton(self, field):
        # Show the number of balls on each field
        print ('Up arrow pressed')
        if field is A:
            self.field_A.up()
            if self.field_A.value == 1:
                self.current_bg = WritePartImage(self.current_bg, BALLA, self, 930, 460)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))
        elif field is B:
            self.field_B.up()
            if self.field_B.value == 1:
                self.current_bg = WriteImage(self.current_bg, BALLB, self, 540, 320)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.current_bg))

        elif field is C:
            self.field_C.up()

        # Event, number up, down
        # self.main_label.setPixmap(QtGui.QPixmap.fromImage(current_background))
        # self.SwitchToScene(EndWindow())

    def handleDownButton(self, field):
        print("Down Arrow pressed")
        # event,, number up, down
        if field is A:
            self.field_A.down()
            if self.field_A.value == 0:
                ball_w = QtGui.QImage(BALLA).width()
                ball_h = QtGui.QImage(BALLA).height()
                self.current_bg = WritePartImage(self.current_bg, self.bg, self, 920, 420, ball_w, ball_h)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.bg))
        elif field is B:
            self.field_B.down()
            if self.field_B.value == 0:
                ball_w = QtGui.QImage(BALLB).width()
                ball_h = QtGui.QImage(BALLB).height()
                self.current_bg = WritePartImage(self.current_bg, self.bg, self, 520, 300, ball_w, ball_h)
                self.main_label.setPixmap(QtGui.QPixmap.fromImage(self.bg))

        elif field is C:
            self.field_C.down()

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
        self.SwitchToScene(None)


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
    overlay = QtGui.QImage(over)
    # Rect with position x,y,w,h to crop of overlay
    if overlay.size() < image.size():
        rect = QtCore.QRect(0, 0, overlay.width(), overlay.height())
    else:
        rect = QtCore.QRect(x, y, over_w+5, over_h+5)
    overlay = overlay.copy(rect)

    painter = QtGui.QPainter()
    # painter.PixmapFragment(w, h)
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

if __name__ == '__main__':
    # s = PyGame.run((PyGame.W, PyGame.H), 6, PyGame.TitleScene())
    # import pygame
    # s = pygame.Surface((W, H))
    # s.fill(WHITE)
    # a = pygame.Surface(center)
    # a.fill((23,233,24))
    # s.blit(a, (0,0))
    # active_scene = TitleScene()
    # app = QtGui.QApplication(sys.argv)
    # # w = MainWindow(s)
    # w = TitleWindow(s)

    # while active_scene is not None:
    #     events = pygame.event.get()
    #     pressed_key = pygame.key.get_pressed()
    #     for event in events:
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #
    #     active_scene.HandleEvents(events, pressed_key)
    #     active_scene.Update()
    #     active_scene.Render(s)
    #     w = AnotherWindow(s)
    #
    #     w.resize(W, H)
    #     w.show()
    #     app.exec_()
    # s = pygame.surface.load
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    mainWindow.setCentralWidget(TitleWindow())
    mainWindow.setGeometry(0, 0, W, H)
    mainWindow.show()
    sys.exit(app.exec_())

    # w = AnotherWindow(s)
    # active_scene = active_scene.next


