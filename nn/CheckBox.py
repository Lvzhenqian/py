from PyQt5.QtWidgets import QApplication,QWidget,QCheckBox,QGroupBox,QStyleFactory,QVBoxLayout,QTextBrowser
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CheckBox(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('CheckBox')
		self.setGeometry(400,400,300,260)

		groupBox = QGroupBox('Non-Exclusive CheckBoxes')
		groupBox.setFlat(True)

		self.checkBox1 = QCheckBox('&Checkbox 1')
		self.checkBox2 = QCheckBox("C&checkbox 2")
		self.checkBox2.setChecked(True)
		self.tristateBox = QCheckBox("Tri-&state button")
		self.tristateBox.setTristate(True)
		self.tristateBox.setCheckState(Qt.PartiallyChecked)

		self.checkBox1.stateChanged.connect(self.changeCheckBoxStatus)
		self.checkBox2.stateChanged.connect(self.changeCheckBoxStatus)
		self.tristateBox.stateChanged.connect(self.changeCheckBoxStatus)

		vbox = QVBoxLayout()
		vbox.addWidget(self.checkBox1)
		vbox.addWidget(self.checkBox2)
		vbox.addWidget(self.tristateBox)
		vbox.addStretch(1)
		groupBox.setLayout(vbox)

		self.lcd = QTextBrowser()
		self.lcd.setFixedHeight(190)
		self.lcd.setFont(QFont("microsoft YaHei",20))
		self.lcd.setText(self.getCheckBoxStatus())

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(groupBox)
		mainLayout.addWidget(self.lcd)
		self.setLayout(mainLayout)

	def changeCheckBoxStatus(self):
		self.lcd.setText(self.getCheckBoxStatus())
	def getCheckBoxStatus(self):
		status = self.checkBox1.text() + ":  " + str(
			self.checkBox1.checkState()) + "\n" + self.checkBox2.text() + ":  " + str(self.checkBox2.checkState()) \
		         + "\n" + self.tristateBox.text() + ":  " + str(self.tristateBox.checkState())
		return status


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = CheckBox()
	ex.show()
	sys.exit(app.exec_())

