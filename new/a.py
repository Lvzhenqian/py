#!/usr/bin/env python
# coding=utf-8
import sys, time,os
for i in range(1,101):
    size = os.get_terminal_size().columns
    sys.stdout.write(' '*size + '\r')
    sys.stdout.flush()
    sys.stdout.write('['+'#'*(i*(100//size)-8)+']'+str(i)+'%'+'\r')
    sys.stdout.flush()
    time.sleep(0.3)
sys.stdout.write(' '*110 + '\r')
