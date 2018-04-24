# from pygame.font import Font
#
#
# class Peas(Font):
#     def __init__(self, size=10):
#         Font.__init__(self,'font/PeasCarrots.ttf', size)  # call Sprite initializer
#
#
# class Orange(Font):
#     def __init__(self, size=10):
#         Font.__init__(self,'font/OrangeJuice.ttf', size)  # call Sprite initializer
#
#
# class Slab(Font):
#     def __init__(self, size=10):
#         Font.__init__(self,'font/SlabThing.ttf', size)  # call Sprite initializer

from PyQt4.QtGui import QFont, QFontDatabase
from PyQt4.QtCore import QString
# "font/PeasCarrots.ttf"

#
# class Font():
#     def __init__(self, file):
#         database = QFontDatabase()
#         font_id = database.addApplicationFont(file)
#         # families = database.applicationFontFamilies(font_id)
#         self.ttf = QFont(families)
#
#
# Peas = Font("font/PeasCarrots.ttf")