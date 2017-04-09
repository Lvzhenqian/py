import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.setWindowTitle('haha')
    def closeEvent(self, QCloseEvent):
        ret = QMessageBox.question(
            self,'message','Did you wan to exit?',
            QMessageBox.Yes,QMessageBox.No
        )
        if ret == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


myapp = QApplication(sys.argv)
mywidget = MyWidget()
mywidget.show()
sys.exit(myapp.exec_())