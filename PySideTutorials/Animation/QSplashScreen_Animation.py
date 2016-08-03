#!/usr/bin/env python2
from PySide import QtCore
from PySide import QtGui
from multiprocessing import Pool

class Form(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QtGui.QTextBrowser()
        self.setWindowTitle('Just a dialog')
        self.move(500,500)
class MySplashScreen(QtGui.QSplashScreen):
    def __init__(self, animation, flags):
        # run event dispatching in another thread
        QtGui.QSplashScreen.__init__(self, QtGui.QPixmap(), flags)
        self.movie = QtGui.QMovie(animation)
        self.movie.frameChanged.connect(self.onNextFrame)
        #self.connect(self.movie, SIGNAL('frameChanged(int)'), SLOT('onNextFrame()'))
        self.movie.start()
        self.move(500, 500)

    def onNextFrame(self):

        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
        self.move(500, 500)

# Put your initialization code here
def longInitialization(arg):
    time.sleep(args)
    return 0
if __name__ == "__main__":
    import sys, time

    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
#   splash_pix = QPixmap('a.gif')
    splash = MySplashScreen('S:\_Studio\_ASSETS\Tutorials\Maya\Coding\Python\_PySide\GIF\dragonGif.gif',
                            QtCore.Qt.WindowStaysOnTopHint)
#   splash.setMask(splash_pix.mask())
    #splash.raise_()
    splash.move(500, 500)
    splash.show()

    # this event loop is needed for dispatching of Qt events
    initLoop = QtCore.QEventLoop()
    pool = Pool(processes=1)
    pool.apply_async(longInitialization, [2], callback=lambda exitCode: initLoop.exit(exitCode))
    initLoop.exec_()

    form = Form()
    form.show()
    splash.finish(form)
    app.exec_()