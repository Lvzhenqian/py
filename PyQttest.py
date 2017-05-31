from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QHBoxLayout,QPushButton,QLineEdit,QVBoxLayout,QMessageBox
import sys

class ShowWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.inputLabel = QLabel('INPUT you text')
		self.editLine = QLineEdit()
		self.printButton = QPushButton('print')
		self.cleanButton = QPushButton('Clear')

		self.printButton.clicked.connect(self.printText)
		self.cleanButton.clicked.connect(self.clearText)

		inputLayout = QHBoxLayout()
		inputLayout.addWidget(self.inputLabel)
		inputLayout.addWidget(self.editLine)

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(self.printButton)
		buttonLayout.addWidget(self.cleanButton)

		mainLayout = QVBoxLayout()
		mainLayout.addLayout(inputLayout)
		mainLayout.addLayout(buttonLayout)

		self.setLayout(mainLayout)
		self.setWindowTitle('fristWindow')
		self.show()

	def printText(self):
		text = self.editLine.text()
		if text == '':
			QMessageBox.information(self,'empty text','please enter the letter.')
		else:
			QMessageBox.information(self,"print Success",'text:%s' % text)
	def clearText(self):
		test = self.editLine.text()
		if test =='':
			return
		else:
			self.editLine.clear()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = ShowWindow()
	sys.exit(app.exec_())
