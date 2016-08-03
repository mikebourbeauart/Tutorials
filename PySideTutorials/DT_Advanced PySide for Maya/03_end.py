import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

from functools import partial


class simpleUI(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setFixedWidth(300)

        self.setLayout(qg.QVBoxLayout())
        self.stacked_layout = qg.QStackedLayout()
        self.layout().addLayout(self.stacked_layout)

        button_layout = qg.QHBoxLayout()
        layout_1_bttn = qg.QPushButton('Layout_1')
        layout_2_bttn = qg.QPushButton('Layout_2')
        layout_3_bttn = qg.QPushButton('Layout_3')
        layout_4_bttn = qg.QPushButton('Layout_4')
        button_layout.addWidget(layout_1_bttn)
        button_layout.addWidget(layout_2_bttn)
        button_layout.addWidget(layout_3_bttn)
        button_layout.addWidget(layout_4_bttn)

        self.layout().addLayout(button_layout)

        # VBOX AND HBOX
        hbox_widget = qg.QWidget()
        hbox_widget.setLayout(qg.QHBoxLayout())

        bttn_1 = qg.QPushButton('Button 1')
        bttn_2 = qg.QPushButton('Button 2')
        bttn_3 = qg.QPushButton('Button 3')
        bttn_4 = qg.QPushButton('Button 4')
        bttn_5 = qg.QPushButton('Button 5')

        hbox_widget.layout().addWidget(bttn_1)
        hbox_widget.layout().addWidget(bttn_2)
        hbox_widget.layout().addWidget(bttn_3)
        hbox_widget.layout().addWidget(bttn_4)
        hbox_widget.layout().addWidget(bttn_5)

        vbox_widget = qg.QWidget()
        vbox_widget.setLayout(qg.QVBoxLayout())

        bttn_1 = qg.QPushButton('Button 1')
        bttn_2 = qg.QPushButton('Button 2')
        bttn_3 = qg.QPushButton('Button 3')
        bttn_4 = qg.QPushButton('Button 4')
        bttn_5 = qg.QPushButton('Button 5')

        vbox_widget.layout().addWidget(bttn_1)
        vbox_widget.layout().addWidget(bttn_2)
        vbox_widget.layout().addWidget(bttn_3)
        vbox_widget.layout().addWidget(bttn_4)
        vbox_widget.layout().addWidget(bttn_5)

        # FORM
        form_widget = qg.QWidget()
        form_widget.setLayout(qg.QFormLayout())

        name_le  = qg.QLineEdit()
        email_le = qg.QLineEdit()
        age_le   = qg.QSpinBox()

        form_widget.layout().addRow('Name:', name_le)
        form_widget.layout().addRow('Email:', email_le)
        form_widget.layout().addRow('Age:', age_le)

        # GRID
        grid_widget = qg.QWidget()
        grid_widget.setLayout(qg.QGridLayout())

        font_names_lb = qg.QLabel('Font')
        font_style_lb = qg.QLabel('Font Style')
        font_size_lb  = qg.QLabel('Size')

        font_names_list = qg.QListWidget()
        font_names_list.addItem('Times')
        font_names_list.addItem('Helvetica')
        font_names_list.addItem('Courier')
        font_names_list.addItem('Palatino')
        font_names_list.addItem('Gill Sans')

        font_style_list = qg.QListWidget()
        font_style_list.addItem('Roman')
        font_style_list.addItem('Italic')
        font_style_list.addItem('Oblique')

        font_size_list  = qg.QListWidget()
        for index in range(10, 30, 2):
            font_size_list.addItem(str(index))

        grid_widget.layout().addWidget(font_names_lb,   0, 0)
        grid_widget.layout().addWidget(font_names_list, 1, 0)

        grid_widget.layout().addWidget(font_style_lb,   0, 1)
        grid_widget.layout().addWidget(font_style_list, 1, 1)

        grid_widget.layout().addWidget(font_size_lb,   0, 2)
        grid_widget.layout().addWidget(font_size_list, 1, 2)


        self.stacked_layout.addWidget(vbox_widget)
        self.stacked_layout.addWidget(hbox_widget)
        self.stacked_layout.addWidget(form_widget)
        self.stacked_layout.addWidget(grid_widget)

        layout_1_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 0))
        layout_2_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 1))
        layout_3_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 2))
        layout_4_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 3))


dialog = simpleUI()
dialog.show()
