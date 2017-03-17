import os
import re
import subprocess

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

from CertConvert.Commands import Commands


class CertConvert(QWidget):
    """Main applicatin widget.

    Attributes:
        :attr __base_path: File base path.
        :attr __layout: Layout.
        :attr __password_field: Password for certificate file.
        :attr __convert_to_select: Dropdown to select convert type."""

    __base_path = os.path.realpath(__file__)
    __layout = None
    __input_file_path = None
    __password_field = None
    __convert_to_select = None
    __strip_password = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Certificate converter')
        self.setWindowIcon(QIcon(self.__base_path + '/../resources/icons/16x16/padlock.png'))
        self.__layout = QGridLayout()
        self.setLayout(self.__layout)

    def create_ui(self):
        """
        Creates the UI.

        :return:
        """

        # Input file
        input_file_label = QLabel('Input file:')
        select_input_file = QPushButton('Select...')
        select_input_file.clicked.connect(self.__on_select_input_file_clicked)

        # Select convert to
        convert_to_label = QLabel('Convert to:')
        self.__convert_to_select = QComboBox()
        self.__convert_to_select.addItems(['.pem', '.crt'])

        # Strip password
        strip_pass_label = QLabel('Strip password:')
        strip_pass_label.setToolTip('Strip certificate key password.')
        self.__strip_password = QCheckBox()
        self.__strip_password.setCheckable(True)
        self.__strip_password.setChecked(True)

        # Password
        password_label = QLabel('Password:')
        self.__password_field = QLineEdit()
        self.__password_field.setPlaceholderText('Password')
        self.__password_field.setToolTip('Leave blank for none.')
        self.__password_field.setEchoMode(self.__password_field.Password)

        # Convert button
        convert_btn = QPushButton('Convert')
        convert_btn.clicked.connect(self.__on_convert_clicked)

        self.__layout.addWidget(input_file_label, 0, 0)
        self.__layout.addWidget(select_input_file, 0, 1)
        self.__layout.addWidget(convert_to_label, 1, 0)
        self.__layout.addWidget(self.__convert_to_select, 1, 1)
        self.__layout.addWidget(self.__strip_password, 2, 1)
        self.__layout.addWidget(strip_pass_label, 2, 0)
        self.__layout.addWidget(password_label, 3, 0)
        self.__layout.addWidget(self.__password_field, 3, 1)
        self.__layout.addWidget(convert_btn, 8, 2)

    @pyqtSlot()
    def __on_select_input_file_clicked(self):
        """
        Handles source file attachment.

        :return:
        """

        input_file = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Certificate file (*.p12 *.psx *.pfx)")
        self.__input_file_path = input_file[0]
        self.__layout.addWidget(QLabel(self.__input_file_path), 0, 2)

    @pyqtSlot()
    def __on_convert_clicked(self):
        """
        Converts the certificate

        :return:
        """
        cert_ext = self.__convert_to_select.currentText()
        password = self.__password_field.text()
        output_key_file = re.sub(r'[a-z0-9.]*$', 'privateKey.key', self.__input_file_path)
        output_cert_file = re.sub(r'[a-z0-9.]*$', 'certificate' + cert_ext, self.__input_file_path)

        subprocess.call(Commands.extract_key(self.__input_file_path, output_key_file, password))

        if self.__strip_password.isChecked():
            subprocess.call(Commands.remove_key_pass(output_key_file, password))

        subprocess.call(Commands.extract_certificate(self.__input_file_path, output_cert_file, password))
        self.__layout.addWidget(QLabel('Certificate file: '), 4, 0)
        self.__layout.addWidget(QLabel(output_cert_file), 4, 1)
        self.__layout.addWidget(QLabel('Private key'), 5, 0)
        self.__layout.addWidget(QLabel(output_key_file), 5, 1)

        return True
