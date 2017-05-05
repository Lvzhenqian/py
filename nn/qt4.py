from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QStyleFactory, QVBoxLayout
import sys


class RadioButton(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('RadioButton')
		self.setGeometry(400, 400, 300, 260)

		self._xpButton = QRadioButton('WindowsXP')
		self._vistaButton = QRadioButton('WindowsVista')
		self._windowSButton = QRadioButton('Windows')
		self._xpButton.toggled.connect(lambda: self.changeStyle('WindowsXP'))
		self._vistaButton.toggled.connect(lambda: self.changeStyle('WindowsVista'))
		self._windowSButton.toggled.connect(lambda: self.changeStyle('Windows'))

		layout = QVBoxLayout()
		layout.addWidget(self._xpButton)
		layout.addWidget(self._vistaButton)
		layout.addWidget(self._windowSButton)

		self.setLayout(layout)
		self._xpButton.setChecked(True)
		self.changeStyle('Windows')

	def changeSyle(self, styleName):
		QApplication.setStyle(QStyleFactory.create(styleName))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = RadioButton()
	ex.show()
	sys.exit(app.exec_())
