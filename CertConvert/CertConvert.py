import os
import re
import subprocess

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget


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

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Certificate convertor')
        self.setWindowIcon(QIcon(self.__base_path + '/../resources/icons/16x16/padlock.png'))
        self.__layout = QGridLayout()
        self.setLayout(self.__layout)

    def create_ui(self):
        # Input file
        input_file_label = QLabel('Input file:')
        select_input_file = QPushButton('Select...')
        select_input_file.clicked.connect(self.__on_select_input_file_clicked)

        # Select convert to
        convert_to_label = QLabel('Convert to:')
        self.__convert_to_select = QComboBox()
        self.__convert_to_select.addItems(['.pem', '.crt'])

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
        self.__layout.addWidget(password_label, 2, 0)
        self.__layout.addWidget(self.__password_field, 2, 1)
        self.__layout.addWidget(convert_btn, 6, 2)

    @pyqtSlot()
    def __on_select_input_file_clicked(self):
        input_file = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Certificate file (*.p12 *.psx *.pfx)")
        self.__input_file_path = input_file[0]
        self.__layout.addWidget(QLabel(self.__input_file_path), 0, 2)

    @pyqtSlot()
    def __on_convert_clicked(self):
        cert_ext = self.__convert_to_select.currentText()
        password = self.__password_field.text()
        output_key_file = re.sub(r'[a-z0-9.]*$', 'privateKey.key', self.__input_file_path)
        output_cert_file = re.sub(r'[a-z0-9.]*$', 'certificate' + cert_ext, self.__input_file_path)
        extract_key_command = [
            'openssl',
            'pkcs12',
            '-in',
            self.__input_file_path,
            '-nocerts',
            '-out',
            output_key_file,
            '-passin',
            'pass:' + password,
            '-passout',
            'pass:' + password
        ]
        remove_key_pass = [
            'openssl',
            'rsa',
            '-in',
            output_key_file,
            '-out',
            output_key_file,
            '-passin',
            'pass:' + password
        ]
        extract_certificate = [
            'openssl',
            'pkcs12',
            '-in',
            self.__input_file_path,
            '-clcerts',
            '-nokeys',
            '-out',
            output_cert_file,
            '-passin',
            'pass:' + password
        ]
        subprocess.call(extract_key_command)
        subprocess.call(remove_key_pass)
        subprocess.call(extract_certificate)
        self.__layout.addWidget(QLabel('Certificate file: '), 4, 0)
        self.__layout.addWidget(QLabel(output_cert_file), 4, 1)
        self.__layout.addWidget(QLabel('Private key'), 5, 0)
        self.__layout.addWidget(QLabel(output_key_file), 5, 1)

