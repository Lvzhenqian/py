import os

logFile = r'f:/tmp/new.txt'

with open(logFile) as f:
    pos = len(f.readline().strip())
    f.seek(0, os.SEEK_END)
    cur = f.tell()
    while cur > 0:
        f.seek(cur - pos, os.SEEK_SET)
        print f.readline().strip(),
        cur -= pos
        f.seek(cur, os.SEEK_SET)