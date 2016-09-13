import math, sys
from PySide import QtGui
from PySide import QtCore


class Overlay(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.move(5,50)
        self.label = QtGui.QLabel('hey')
        self.label.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # position the widgets
        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.label)
        self.setLayout(main_layout)

        # use an animated gif file you have in the working folder
        # or give the full file path
        ag_file = "S:\_Studio\_ASSETS\Tutorials\Maya\Coding\Python\_PySide\GIF\dragonGif.gif"
        self.movie = QtGui.QMovie(ag_file, QtCore.QByteArray(), self)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setScaledSize(QtCore.QSize(200,105) )
        self.movie.setSpeed(100)
        self.label.setMovie(self.movie)
        # optionally display first frame
        self.movie.start()




class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        widget = QtGui.QWidget(self)
        self.editor = QtGui.QTextEdit()
        self.editor.setPlainText("0123456789"*100)
        layout = QtGui.QGridLayout(widget)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        button = QtGui.QPushButton("Wait")
        layout.addWidget(button, 1, 1, 1, 1)

        self.setCentralWidget(widget)
        self.overlay = Overlay(self.centralWidget())
        self.overlay.show

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())