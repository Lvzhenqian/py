import threading
import time,sys,shutil
def sleep(x):
    time.sleep(x)
    shutil.move(r'd:\nb\testc.py',r'd:\testc.py')
if __name__ == '__main__':
    p = threading.Thread(target=sleep,args=(3,))
    p.start()
    sys.exit()
