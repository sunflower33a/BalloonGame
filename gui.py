"""
Create a Window
learn about PyQt4

"""
import sys
from PyQt4 import QtGui
#import PyQt4.QtGui

def main():
    app = QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    window.resize(1280, 800)
    window.move(300, 250)
    window.setWindowTitle("Colonel Balloon")

    window.show()

    sys.exit(app.exec_())

if __name__=='__main__':
    main()