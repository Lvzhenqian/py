#!/usr/bin/env python
# coding=utf-8
import os,time
dic = {'1':'a','2':'b','3':'c'}
def a():
    print('i am AAAAAAAAAA')
def b():
    print('i am bbbbbbbbbb')
def c():
    print('i am cccccccccc')
while True:
    print('''
    number:{0} <---> function name: {1}
    number:{2} <---> function name: {3}
    number:{4} <---> function name: {5}
    '''.format('1','a','2','b','3','c'))
    i = input("please input number or func name: ")
    if i.lower() == 'quit':
        break
    if i == '1' or i.upper() == 'A':
        a()
    elif i == '2' or i.upper() == 'B':
        b()
    elif i == '3' or i.upper() == 'C':
        c()
    time.sleep(1)
    os.system('clear')
