#########################################################
## customize Title bar
## dotpy.ir
## iraj.jelo@gmail.com
#########################################################
import sys
from PySide import QtGui
from PySide import QtCore


class TitleBar(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TitleBar, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        css = """
        QWidget{
            Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            Background-image:url('img/titlebar bg.png');
            font-size:12px;
            color: black;

        }
        QToolButton{
            Background:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #FF00FF;
            font-size:11px;
        }
        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        self.minimize=QtGui.QToolButton(self)
        self.minimize.setIcon(QtGui.QIcon('img/min.png'))
        self.maximize=QtGui.QToolButton(self)
        self.maximize.setIcon(QtGui.QIcon('img/max.png'))
        close=QtGui.QToolButton(self)
        close.setIcon(QtGui.QIcon('img/close.png'))
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)
        label=QtGui.QLabel(self)
        label.setText("Window Title")
        self.setWindowTitle("Window Title")
        hbox=QtGui.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        #hbox.insertStretch(1,1000)
        #hbox.setSpacing(0)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        self.maxNormal=False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        box.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            box.showNormal()
            self.maxNormal= False
            self.maximize.setIcon(QtGui.QIcon('img/max.png'))
            print '1'
        else:
            box.showMaximized()
            self.maxNormal=  True
            print '2'
            self.maximize.setIcon(QtGui.QIcon('img/max2.png'))

    def close(self):
        box.close()

    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            box.moving = True; box.offset = event.pos()

    def mouseMoveEvent(self,event):
        if box.moving: box.move(event.globalPos()-box.offset)


class Frame(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.m_mouse_down= False

        self.setFrameShape(QtGui.QFrame.StyledPanel)
        css = """
        QFrame{
            Background: #D700D7;
            color:white;
            font:13px ;
            font-weight:bold;
            }
        """
        self.setStyleSheet(css)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar= TitleBar(self)
        self.m_content= QtGui.QWidget(self)
        vbox=QtGui.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setSpacing(0)
        layout=QtGui.QVBoxLayout(self)
        layout.addWidget(self.m_content)
        layout.setSpacing(5)
        vbox.addLayout(layout)
        # Allows you to access the content area of the frame
        # where widgets and layouts can be added

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self,event):
        self.m_old_pos = event.pos();
        self.m_mouse_down = event.button()== Qt.LeftButton;

    def mouseMoveEvent(self,event):
        x=event.x();
        y=event.y();

    def mouseReleaseEvent(self,event):
        m_mouse_down=False;

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv);
    box = Frame()
    box.move(60,60);
    l=QtGui.QVBoxLayout(box.contentWidget());
    l.setSpacing(0);
    edit=QtGui.QLabel("""I would've did anything for you to show you how much I adored you
But it's over now, it's too late to save our loveJust promise me you'll think of me
Every time you look up in the sky and see a star 'cuz I'm  your star.""");
    l.addWidget(edit)
    box.show()
    app.exec_()