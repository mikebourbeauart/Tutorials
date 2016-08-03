import PyQt4.QtCore as qc
import PyQt4.QtGui  as qg

import utils.names as names
import maya.cmds   as mc

dialog = None

#------------------------------------------------------------------------------#

class NameIt(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Name It')
        self.setFixedHeight(285)
        self.setFixedWidth(320)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignTop)

        # RENAME Widget
        #
        rename_widget = qg.QWidget()
        rename_widget.setLayout(qg.QVBoxLayout())
        rename_widget.layout().setContentsMargins(0,0,0,0)
        rename_widget.layout().setSpacing(2)
        rename_widget.setSizePolicy(qg.QSizePolicy.Minimum,
                                    qg.QSizePolicy.Fixed)
        self.layout().addWidget(rename_widget)

        rename_splitter = Splitter("RENAME")
        rename_widget.layout().addWidget(rename_splitter)

        rename_text_layout = qg.QHBoxLayout()
        rename_text_layout.setContentsMargins(4,0,4,0)
        rename_text_layout.setSpacing(2)
        rename_widget.layout().addLayout(rename_text_layout)

        rename_text_lb = qg.QLabel('New Name:')
        self.rename_le      = qg.QLineEdit()
        rename_text_layout.addWidget(rename_text_lb)
        rename_text_layout.addWidget(self.rename_le)

        reg_ex = qc.QRegExp("^(?!^_)[a-zA-Z_]+") #############################################################
        text_validator = qg.QRegExpValidator(reg_ex, self.rename_le)
        self.rename_le.setValidator(text_validator)

        rename_widget.layout().addLayout(SplitterLayout())

        rename_mult_layout = qg.QHBoxLayout()
        rename_mult_layout.setContentsMargins(4,0,4,0)
        rename_mult_layout.setSpacing(2)
        rename_widget.layout().addLayout(rename_mult_layout)

        rename_mult_method_lb    = qg.QLabel('Multiples Naming Method:')
        self.rename_mult_method_combo = qg.QComboBox()
        self.rename_mult_method_combo.addItem('Numbers (0-9)')
        self.rename_mult_method_combo.addItem('Letters (a-z)')
        self.rename_mult_method_combo.setFixedWidth(100)

        rename_mult_layout.addWidget(rename_mult_method_lb)
        rename_mult_layout.addWidget(self.rename_mult_method_combo)

        mult_options_layout = qg.QHBoxLayout()
        mult_options_layout.setContentsMargins(4,0,4,0)
        mult_options_layout.setSpacing(2)
        rename_widget.layout().addLayout(mult_options_layout)

        self.frame_pad_lb   = qg.QLabel('No. Padding:')
        self.frame_pad_spin = qg.QSpinBox()
        self.frame_pad_spin.setFixedWidth(40)
        self.frame_pad_spin.setMinimum(0)
        self.frame_pad_spin.setMaximum(10)

        self.lower_radio = qg.QRadioButton('Lowercase')
        self.upper_radio = qg.QRadioButton('Uppercase')
        self.lower_radio.setVisible(False)
        self.upper_radio.setVisible(False)
        self.lower_radio.setFixedHeight(19)
        self.upper_radio.setFixedHeight(19)
        self.lower_radio.setChecked(True)

        mult_options_layout.addWidget(self.frame_pad_lb)
        mult_options_layout.addWidget(self.lower_radio)
        mult_options_layout.addSpacerItem(qg.QSpacerItem(5,5,qg.QSizePolicy.Expanding))
        mult_options_layout.addWidget(self.frame_pad_spin)
        mult_options_layout.addWidget(self.upper_radio)

        rename_widget.layout().addLayout(SplitterLayout())

        fix_layout = qg.QHBoxLayout()
        fix_layout.setContentsMargins(4,0,4,0)
        fix_layout.setSpacing(2)
        rename_widget.layout().addLayout(fix_layout)

        self.prefix_check = qg.QCheckBox('Prefix:')
        self.prefix_le    = qg.QLineEdit()
        self.prefix_le.setEnabled(False)
        self.prefix_le.setFixedWidth(85)
        self.prefix_le.setValidator(text_validator)

        self.suffix_check = qg.QCheckBox('Suffix:')
        self.suffix_le    = qg.QLineEdit()
        self.suffix_le.setEnabled(False)
        self.suffix_le.setFixedWidth(85)
        self.suffix_le.setValidator(text_validator)

        fix_layout.addWidget(self.prefix_check)
        fix_layout.addWidget(self.prefix_le)
        fix_layout.addSpacerItem(qg.QSpacerItem(5,5,qg.QSizePolicy.Expanding))
        fix_layout.addWidget(self.suffix_check)
        fix_layout.addWidget(self.suffix_le)

        rename_widget.layout().addLayout(SplitterLayout())

        rename_bttn_layout = qg.QHBoxLayout()
        rename_bttn_layout.setContentsMargins(4,0,4,0)
        rename_bttn_layout.setSpacing(0)
        rename_widget.layout().addLayout(rename_bttn_layout)

        self.rename_lb = qg.QLabel('e.g.')
        rename_bttn = qg.QPushButton('Rename')
        rename_bttn.setFixedHeight(20)
        rename_bttn.setFixedWidth(55)

        rename_bttn_layout.addWidget(self.rename_lb)
        rename_bttn_layout.addWidget(rename_bttn)

        spacer_item = qg.QSpacerItem(20, 20, qg.QSizePolicy.Fixed)
        self.layout().addSpacerItem(spacer_item)

        # REPLACE Widget
        #
        replace_widget = qg.QWidget()
        replace_widget.setLayout(qg.QVBoxLayout())
        replace_widget.layout().setContentsMargins(0,0,0,0)
        replace_widget.layout().setSpacing(2)
        replace_widget.setSizePolicy(qg.QSizePolicy.Minimum,
                                     qg.QSizePolicy.Fixed)
        self.layout().addWidget(replace_widget)

        replace_splitter = Splitter("FIND/REPLACE")
        replace_widget.layout().addWidget(replace_splitter)

        replace_lb = qg.QLabel('Find:')
        replace_le = qg.QLineEdit()
        with_lb    = qg.QLabel('Replace:')
        with_le    = qg.QLineEdit()

        reg_ex = qc.QRegExp("[a-zA-Z_]+") ##############################################################
        text_validator = qg.QRegExpValidator(reg_ex, replace_le)
        replace_le.setValidator(text_validator)
        with_le.setValidator(text_validator)

        replace_lb.setFixedWidth(55)
        with_lb.setFixedWidth(55)

        replace_layout = qg.QHBoxLayout()
        replace_layout.setContentsMargins(4,0,4,0)
        replace_layout.setSpacing(2)
        replace_layout.addWidget(replace_lb)
        replace_layout.addWidget(replace_le)
        replace_widget.layout().addLayout(replace_layout)

        with_layout = qg.QHBoxLayout()
        with_layout.setContentsMargins(4,0,4,0)
        with_layout.setSpacing(2)
        with_layout.addWidget(with_lb)
        with_layout.addWidget(with_le)
        replace_widget.layout().addLayout(with_layout)

        replace_widget.layout().addLayout(SplitterLayout())

        selection_layout = qg.QHBoxLayout()
        selection_layout.setContentsMargins(4,0,4,0)
        selection_layout.setSpacing(2)
        replace_widget.layout().addLayout(selection_layout)

        selection_mode_lb = qg.QLabel('Selection Mode:')
        all_radio = qg.QRadioButton('All')
        all_radio.setFixedHeight(19)
        all_radio.setChecked(True)
        selected_radio = qg.QRadioButton('Selected')
        selected_radio.setFixedHeight(19)

        selection_layout.addWidget(selection_mode_lb)
        spacer_item = qg.QSpacerItem(5,5,qg.QSizePolicy.Expanding)
        selection_layout.addSpacerItem(spacer_item)
        selection_layout.addWidget(all_radio)
        selection_layout.addWidget(selected_radio)

        replace_widget.layout().addLayout(SplitterLayout())

        replace_bttn = qg.QPushButton('Replace')
        replace_bttn.setFixedHeight(20)
        replace_bttn.setFixedWidth(55)
        replace_bttn_layout = qg.QHBoxLayout()
        replace_bttn_layout.setContentsMargins(4,0,4,0)
        replace_bttn_layout.setSpacing(0)
        replace_bttn_layout.setAlignment(qc.Qt.AlignRight)
        replace_bttn_layout.addWidget(replace_bttn)
        replace_widget.layout().addLayout(replace_bttn_layout)

        # connect modifiers
        #
        self.prefix_check.stateChanged.connect(self.prefix_le.setEnabled)
        self.suffix_check.stateChanged.connect(self.suffix_le.setEnabled)
        self.prefix_check.stateChanged.connect(self._updateExampleRename)
        self.suffix_check.stateChanged.connect(self._updateExampleRename)

        self.rename_mult_method_combo.currentIndexChanged.connect(self._toggleMultNamingMethod)

        self.lower_radio.clicked.connect(self._updateExampleRename)
        self.upper_radio.clicked.connect(self._updateExampleRename)
        self.frame_pad_spin.valueChanged.connect(self._updateExampleRename)

        self.rename_le.textChanged.connect(self._updateExampleRename)
        self.prefix_le.textChanged.connect(self._updateExampleRename)
        self.suffix_le.textChanged.connect(self._updateExampleRename)

        self._updateExampleRename()

    #----------------------------------------------------------------------#

    def _toggleMultNamingMethod(self, index):
        self.lower_radio.setVisible(index)
        self.upper_radio.setVisible(index)
        self.frame_pad_lb.setVisible(not(index))
        self.frame_pad_spin.setVisible(not(index))

    #----------------------------------------------------------------------#

    def _getRenameSettings(self):
        text = str(self.rename_le.text()).strip()

        naming_method = bool(self.rename_mult_method_combo.currentIndex())
        padding = 0; upper = True
        if naming_method == 0:
            padding = self.frame_pad_spin.value()
        else:
            upper   = self.upper_radio.isChecked()

        prefix = ''; suffix = ''
        if self.prefix_check.isChecked():
            prefix = self.prefix_le.text()
        if self.suffix_check.isChecked():
            suffix = self.suffix_le.text()

        return text, prefix, suffix, padding, naming_method, upper

    #----------------------------------------------------------------------#

    def _updateExampleRename(self):
        example_text = ''

        text, prefix, suffix, padding, naming_method, upper = self._getRenameSettings()

        if not text:
            self.rename_lb.setText('<font color=#646464>e.g.</font>')
            return

        if prefix: example_text += '%s_' %prefix

        example_text += '%s_' %text

        if naming_method:
            if upper: example_text += 'A'
            else:     example_text += 'a'
        else:
            example_text += (padding * '0') + '1'

        if suffix: example_text += '_%s' %suffix

        self.rename_lb.setText('<font color=#646464>e.g. \'%s\'</font>' %example_text)


#------------------------------------------------------------------------------#

class Splitter(qg.QWidget):
    def __init__(self, text=None, shadow=True, color=(150, 150, 150)):
        qg.QWidget.__init__(self)

        self.setMinimumHeight(2)
        self.setLayout(qg.QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignVCenter)

        first_line = qg.QFrame()
        first_line.setFrameStyle(qg.QFrame.HLine)
        self.layout().addWidget(first_line)

        main_color   = 'rgba( %s, %s, %s, 255)' %color
        shadow_color = 'rgba( 45,  45,  45, 255)'

        bottom_border = ''
        if shadow:
            bottom_border = 'border-bottom:1px solid %s;' %shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:1px; \
                       %s" %(main_color, bottom_border)

        first_line.setStyleSheet(style_sheet)

        if text is None:
            return

        first_line.setMaximumWidth(5)

        font = qg.QFont()
        font.setBold(True)

        text_width = qg.QFontMetrics(font)
        width = text_width.width(text) + 6

        label = qg.QLabel()
        label.setText(text)
        label.setFont(font)
        label.setMaximumWidth(width)
        label.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        self.layout().addWidget(label)

        second_line = qg.QFrame()
        second_line.setFrameStyle(qg.QFrame.HLine)
        second_line.setStyleSheet(style_sheet)
        self.layout().addWidget(second_line)


class SplitterLayout(qg.QHBoxLayout):
    def __init__(self):
        qg.QHBoxLayout.__init__(self)
        self.setContentsMargins(40,2,40,2)

        splitter = Splitter(shadow=False, color=(60,60,60))
        splitter.setFixedHeight(1)

        self.addWidget(splitter)


#------------------------------------------------------------------------------#

def create():
    global dialog
    if dialog is None:
        dialog = NameIt()
    dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None

