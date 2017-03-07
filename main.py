import sys

from PyQt5.QtWidgets import QApplication

from CertConvert.CertConvert import CertConvert

app = QApplication(sys.argv)

if __name__ == '__main__':
    main = CertConvert()
    main.create_ui()
    main.show()
    sys.exit(app.exec_())
