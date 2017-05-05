from PyQt5.QtWidgets import QApplication,QWidget,QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys

class PushButton(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('PushButton')
		self.setGeometry(400,400,300,260)
		self.closeButton = QPushButton(self)
		self.closeButton.setText('Close')
		self.closeButton.setShortcut('Ctrl+D')
		self.closeButton.setIcon(QIcon(r'd:\ico\2.ico'))
		self.closeButton.clicked.connect(self.close)
		self.closeButton.setToolTip('close the widget')
		self.closeButton.move(100,100)
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = PushButton()
	ex.show()
	sys.exit(app.exec_())