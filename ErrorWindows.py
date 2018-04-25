"""
    GUI for popup error window
"""
from PyQt4.QtGui import QWidget, QLabel, QPushButton, QImage
import Style
from PyQt4.QtCore import Qt, QEvent, pyqtSignal
from MyDefinition import *


class PopUp(QWidget):
    keyPressed = pyqtSignal(QEvent)

    def keyPressEvent(self, event):
        super(PopUp, self).keyPressEvent(event)
        self.keyPressed.emit(event)

    def __init__(self, msg):
        QWidget.__init__(self)
        img = QImage("artwork/Butt-NO.png")
        self.setGeometry(100, 100, img.width()/2, img.height()/2)
        self.setWindowTitle(msg)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, img.width()/2, img.height()/2)
        self.label.setStyleSheet(Style.Label)
        self.keyPressed.connect(self.handleOkButton)

    def handleOkButton(self, event):
        if event.key() == Qt.Key_Enter:
            self.hide()
