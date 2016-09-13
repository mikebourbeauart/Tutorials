from PySide.QtCore import *
from PySide.QtGui import *
import sys
 
def redoClicked():
  msg_box = QMessageBox()
  msg_box.setText('Redo will be performed')
  msg_box.exec_()
 
app = QApplication(sys.argv)
 
window = QWidget()
vbox = QVBoxLayout()
 
menu_bar = QMenuBar()
file_menu = menu_bar.addMenu('File')
edit_menu = menu_bar.addMenu('Edit')
exit_action = QAction('Exit', window)
exit_action.triggered.connect(exit)
file_menu.addAction(exit_action)
redo_action = QAction('Redo', window)
redo_action.triggered.connect(redoClicked)
edit_menu.addAction(redo_action)
 
window.setLayout(vbox)
vbox.addWidget(menu_bar)
window.show()
app.exec_()