# import os
# #import pygame, sys
# #from pygame.locals import *
# # before any pygame objects
# # pygame.init()
# #
# # DISPLAYSURF = pygame.display.set_mode(900, 1000)
# # pygame.display.set_caption("Blotto Game")
# #
# # while True:
# #     for event in pygame.event.get()
# #         if event.type == QUIT:
# #             pygame.quit()
# #             sys.exit
# #         pygame.display.update() # surface object doesnt change
#
# import gambit
# # create an extensive game or create a list of game? or extension game
# """
# g = gambit.Game.new_tree()
# g.title = "Blotto Game"
# # Players
# p1 = g.players.add("Anna")
# p2 = g.players.add("Computer")
# print str(g.title)
# print str(p1.label)+ " vs. "+ str(p2.label)
# for p in g.players:
#     print p.label
# """
#
# # Strategies of each player:
# # Games in strategic form are created using Game.new_table(),
# # which takes a list of integers specifying the number of strategies for each player
# # An extensive game in which each node is a strategic game
# g = gambit.Game.new_table([3,3])    # each has 3 strategies
# g.title = "Blotto Game"
# p1 = g.players.add("Anna")
# p2 = g.players.add("Computer")
#
# print str(g.title)
# print "{0} vs. {1}".format(str(p1.label), str(p2.label))
#
# for p in g.players:
#     for s in p.strategies:
#         s.label = 1

from PyQt4 import QtGui
import pygame
import sys


class ImageWidget(QtGui.QWidget):
    def __init__(self,surface,parent=None):
        super(ImageWidget,self).__init__(parent)
        w=surface.get_width()
        h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QtGui.QImage(self.data,w,h,QtGui.QImage.Format_RGB32)

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0,0,self.image)
        qp.end()


class MainWindow(QtGui.QMainWindow):
    def __init__(self,surface,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setCentralWidget(ImageWidget(surface))


pygame.init()
s = pygame.Surface((640,480))
s.fill((64,128,192,224))
pygame.draw.circle(s,(255,255,255,255),(100,100),50)

app = QtGui.QApplication(sys.argv)
w = MainWindow(s)
w.show()
app.exec_()
