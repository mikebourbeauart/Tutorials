# Import PySide classes
import sys
from PySide.QtCore import *
from PySide.QtGui import *
 
 
class App:
  def __init__(self):
    # Create a Qt application  
    icon = QIcon("S:/ABC_TESTPROJECT_12345/Sequences/ANA30secService/Sh010/Modeling/Production/Maya/scenes/body/Sh010_Modeling_body_v001.0001.ma_image.png")
    menu = QMenu()
    settingAction = menu.addAction("setting")
    settingAction.triggered.connect(self.setting)
    exitAction = menu.addAction("exit")
    exitAction.triggered.connect(sys.exit)
    
    self.tray = QSystemTrayIcon()
    self.tray.setIcon(icon)
    self.tray.setContextMenu(menu)
    self.tray.show()
    self.tray.setToolTip("unko!")
    self.tray.showMessage("hoge", "moge")
    self.tray.showMessage("fuga", "moge")
    
 
  def setting(self):
    self.dialog = QDialog()
    self.dialog.setWindowTitle("Setting Dialog")
    self.dialog.show()
 
  
if __name__ == "__main__":
    # workaround for a bug in maya
    try:
        thing.close()
        thing.deleteLater()
    except:
        pass
        
    thing = App()
    thing.show()

    try:
        thing.show()
    except:
        thing.close()
        thing.deleteLater()
        