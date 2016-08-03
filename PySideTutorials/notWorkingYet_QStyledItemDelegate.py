from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui

def maya_main_window():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   

class MyWindow(QtGui.QDialog): 
    def __init__( self, parent=maya_main_window() ):
        super( MyWindow, self ).__init__(  )
        
        self.word_list = ['alpha', 'beta', 'car', 'hello', 'bye']
        # create objects
        self.la = QtGui.QLabel("Press tab in this box:")
        self.le = MyLineEdit()
        self.completer = QtGui.QCompleter(self.word_list)
        self.le.setCompleter(self.completer)
        self.la2 = QtGui.QLabel("\nLook here:")
        self.le2 = QtGui.QLineEdit()

        # layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.la)
        layout.addWidget(self.le)
        layout.addWidget(self.la2)
        layout.addWidget(self.le2)
        self.setLayout(layout)

class HTMLDelegate(QtGui.QStyledItemDelegate):
    def paint( self,painter, option, index,  parent=maya_main_window() ):
        super( HTMLDelegate, self ).__init__(  )

        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options,index)

        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)

        options.text = ""
        style.drawControl(QtGui.QStyle.CE_ItemViewItem, options, painter);

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected
        #if (optionV4.state & QStyle::State_Selected)
            #ctx.palette.setColor(QPalette::Text, optionV4.palette.color(QPalette::Active, QPalette::HighlightedText));

        textRect = style.subElementRect(QtGui.QStyle.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options,index)

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QtCore.QSize(doc.idealWidth(), doc.size().height())
        
if __name__ == "__main__": 
# Development stuff
    try:
        myWindow_ui.close()
        myWindow_ui.deleteLater()
    except:
        pass

    myWindow_ui = MyWindow()
    myWindow_ui.show()

    # Development stuff
    try:
        myWindow_ui.show()
    except:
        myWindow_ui.close()
        myWindow_ui.deleteLater()
