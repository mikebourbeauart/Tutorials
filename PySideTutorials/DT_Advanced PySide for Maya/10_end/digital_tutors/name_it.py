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

        rename_splitter = Splitter()
        rename_widget.layout().addWidget(rename_splitter)

        rename_text_layout = qg.QHBoxLayout()
        rename_text_layout.setContentsMargins(4,0,4,0)
        rename_text_layout.setSpacing(2)
        rename_widget.layout().addLayout(rename_text_layout)

        rename_text_lb = qg.QLabel('New Name:')
        rename_le  = qg.QLineEdit()
        rename_text_layout.addWidget(rename_text_lb)
        rename_text_layout.addWidget(rename_le)

        rename_mult_layout = qg.QHBoxLayout()
        rename_mult_layout.setContentsMargins(4,0,4,0)
        rename_mult_layout.setSpacing(2)
        rename_widget.layout().addLayout(rename_mult_layout)

        rename_mult_method_lb = qg.QLabel('Multiples Naming Method:')
        rename_mult_method_combo = qg.QComboBox()
        rename_mult_method_combo.addItem('Numbers (0-9)')
        rename_mult_method_combo.addItem('Letters (a-z)')
        rename_mult_method_combo.setFixedWidth(100)

        rename_mult_layout.addWidget(rename_mult_method_lb)
        rename_mult_layout.addWidget(rename_mult_method_combo)

        mult_options_layout = qg.QHBoxLayout()
        mult_options_layout.setContentsMargins(4,0,4,0)
        mult_options_layout.setSpacing(2)
        rename_widget.layout().addLayout(mult_options_layout)

        frame_pad_lb = qg.QLabel('No. Padding:')
        frame_pad_spin = qg.QSpinBox()
        frame_pad_spin.setFixedWidth(40)
        frame_pad_spin.setMinimum(0)
        frame_pad_spin.setMaximum(10)

        lower_radio = qg.QRadioButton('Lowercase')
        upper_radio = qg.QRadioButton('Uppercase')
        lower_radio.setVisible(False)
        upper_radio.setVisible(False)
        lower_radio.setFixedHeight(19)
        upper_radio.setFixedHeight(19)
        lower_radio.setChecked(True)

        mult_options_layout.addWidget(frame_pad_lb)
        mult_options_layout.addWidget(lower_radio)
        mult_options_layout.addSpacerItem(qg.QSpacerItem(5,5,qg.QSizePolicy.Expanding))
        mult_options_layout.addWidget(frame_pad_spin)
        mult_options_layout.addWidget(upper_radio)

        fix_layout = qg.QHBoxLayout()
        fix_layout.setContentsMargins(4,0,4,0)
        fix_layout.setSpacing(2)
        rename_widget.layout().addLayout(fix_layout)

        prefix_check = qg.QCheckBox('Prefix:')
        prefix_le  = qg.QLineEdit()
        prefix_le.setEnabled(False)
        prefix_le.setFixedWidth(85)

        suffix_check = qg.QCheckBox('Suffix:')
        suffix_le  = qg.QLineEdit()
        suffix_le.setEnabled(False)
        suffix_le.setFixedWidth(85)

        fix_layout.addWidget(prefix_check)
        fix_layout.addWidget(prefix_le)
        fix_layout.addSpacerItem(qg.QSpacerItem(5,5,qg.QSizePolicy.Expanding))
        fix_layout.addWidget(suffix_check)
        fix_layout.addWidget(suffix_le)

        rename_lb = qg.QLabel('e.g.')
        rename_bttn = qg.QPushButton('Rename')
        rename_bttn.setFixedHeight(20)
        rename_bttn.setFixedWidth(55)
        rename_bttn_layout = qg.QHBoxLayout()
        rename_bttn_layout.setContentsMargins(4,0,4,0)
        rename_bttn_layout.setSpacing(0)
        rename_bttn_layout.addWidget(rename_lb)
        rename_bttn_layout.addWidget(rename_bttn)
        rename_widget.layout().addLayout(rename_bttn_layout)

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

        replace_lb = qg.QLabel('Find:')
        replace_le  = qg.QLineEdit()
        with_lb    = qg.QLabel('Replace:')
        with_le     = qg.QLineEdit()

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

        selection_mode_lb = qg.QLabel('Selection Mode:')
        all_radio = qg.QRadioButton('All')
        all_radio.setFixedHeight(19)
        all_radio.setChecked(True)
        selected_radio = qg.QRadioButton('Selected')
        selected_radio.setFixedHeight(19)

        selection_layout = qg.QHBoxLayout()
        selection_layout.setContentsMargins(4,0,4,0)
        selection_layout.setSpacing(2)
        selection_layout.addWidget(selection_mode_lb)
        spacer_item = qg.QSpacerItem(5,5,qg.QSizePolicy.Expanding)
        selection_layout.addSpacerItem(spacer_item)
        selection_layout.addWidget(all_radio)
        selection_layout.addWidget(selected_radio)
        replace_widget.layout().addLayout(selection_layout)

        replace_bttn = qg.QPushButton('Replace')
        replace_bttn.setFixedHeight(20)
        replace_bttn.setFixedWidth(55)
        replace_bttn_layout = qg.QHBoxLayout()
        replace_bttn_layout.setContentsMargins(4,0,4,0)
        replace_bttn_layout.setSpacing(0)
        replace_bttn_layout.setAlignment(qc.Qt.AlignRight)
        replace_bttn_layout.addWidget(replace_bttn)
        replace_widget.layout().addLayout(replace_bttn_layout)

#------------------------------------------------------------------------------#

class Splitter(qg.QWidget):
    def __init__(self, shadow=True, color=(150, 150, 150)):
        qg.QWidget.__init__(self)

        self.setMinimumHeight(2)
        self.setLayout(qg.QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignVCenter)

        main_line = qg.QFrame()
        main_line.setFrameStyle(qg.QFrame.HLine)
        self.layout().addWidget(main_line)

        main_color   = 'rgba( %s,  %s,  %s, 255)' %color
        shadow_color = 'rgba( 45,  45,  45, 255)'
        bottom_border = ''
        if shadow:
            bottom_border = 'border-bottom:1px solid %s;' %shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color:%s; \
                       max-height:1px; \
                       %s;" %(main_color, bottom_border)
        main_line.setStyleSheet(style_sheet)

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
