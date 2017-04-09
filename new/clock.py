import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *

app = QCoreApplication(sys.argv)

try:
    due  = QTime.currentTime()
    message = 'Alert!'
    if len(sys.argv)<2:
        raise ValueError
    hours,mins = sys.argv[1].split(":")
    due = QTime(int(hours),int(mins))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) >2:
        message = " ".join(sys.argv[2:])
except ValueError:
    message = "Usage: {} HH:MM [optional message]".format(sys.argv[0])
while QTime.currentTime() < due:
    time.sleep(10)

