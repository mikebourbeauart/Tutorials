import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

class simpleUI(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setFixedWidth(300)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(5)

        text_layout = qg.QHBoxLayout()
        text_layout.setSpacing(5)
        self.layout().addLayout(text_layout)

        example_lb = qg.QLabel('Title:')
        bold_font = qg.QFont()
        bold_font.setBold(True)
        example_lb.setFont(bold_font)

        example_le = qg.QLineEdit()
        example_le.setPlaceholderText("Type Something...")

        reg_ex = qc.QRegExp("[a-zA-Z_]+")
        text_validator = qg.QRegExpValidator(reg_ex, example_le)
        example_le.setValidator(text_validator)

        self.example_te = qg.QTextEdit()
        self.example_te.setWordWrapMode(qg.QTextOption.WrapAtWordBoundaryOrAnywhere)

        text_layout.addWidget(example_lb)
        text_layout.addWidget(example_le)
        text_layout.addWidget(self.example_te)

        button_layout = qg.QHBoxLayout()
        button_layout.setSpacing(5)
        self.layout().addLayout(button_layout)

        example_bttn = qg.QPushButton('Button')

        a_radio = qg.QRadioButton('a')
        b_radio = qg.QRadioButton('b')
        c_radio = qg.QRadioButton('c')
        d_radio = qg.QRadioButton('d')

        button_grp_1 = qg.QButtonGroup(self)
        button_grp_2 = qg.QButtonGroup(self)

        button_grp_1.addButton(a_radio)
        button_grp_1.addButton(b_radio)

        button_grp_2.addButton(c_radio)
        button_grp_2.addButton(d_radio)

        example_check = qg.QCheckBox('Check')

        button_layout.addWidget(example_bttn)
        button_layout.addWidget(a_radio)
        button_layout.addWidget(b_radio)
        button_layout.addWidget(c_radio)
        button_layout.addWidget(d_radio)
        button_layout.addWidget(example_check)

        counter_layout = qg.QHBoxLayout()
        counter_layout.setSpacing(5)
        self.layout().addLayout(counter_layout)

        example_slider = qg.QSlider()
        example_slider.setOrientation(qc.Qt.Horizontal)
        example_slider.setRange(0, 10)

        example_spin = qg.QSpinBox()
        example_spin.setRange(0, 10)

        counter_layout.addWidget(example_slider)
        counter_layout.addWidget(example_spin)

        example_slider.valueChanged.connect(example_spin.setValue)
        example_spin.valueChanged.connect(example_slider.setValue)

        example_bttn.clicked.connect(self.printText)
        example_check.stateChanged.connect(example_bttn.setDisabled)

        button_grp_1.buttonClicked.connect(self.addToTextEdit)


    def printText(self):
        print self.example_te.toPlainText()


    def addToTextEdit(self, button):
        button_text = button.text()
        self.example_te.setText(self.example_te.toPlainText() + button_text)



dialog = simpleUI()
dialog.show()
