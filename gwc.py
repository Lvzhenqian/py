#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import,division,print_function,unicode_literals
import os,time,sys
if sys.version_info.major == 3:
    unicode = str
else:
    bytes = str

lst = [('car',5000),('apple',500),('pan',50),('book',20)]
shoplist = []
money = int(input("please input your money: "))
while True:
    print(
    '''
    shopping list:
    -------------
    1. %s   %s
    2. %s   %s
    3. %s   %s
    4. %s   %s
    -------------
    input quit to exit.
    ''' % (lst[0][0],lst[0][1],lst[1][0],lst[1][1],lst[2][0],lst[2][1],lst[3][0],lst[3][1])
    )
    print('shoplist: %s  money: %s' %(shoplist,money))
    select = input('please input you wan to buy.>>> ')
    if select.lower() == 'quit' or money <= 0:
        break
    if select.strip() == '1' or select.lower() == 'car':
        if money >lst[0][1]: 
            money -=  lst[0][1]
            shoplist.append(lst[0][0])
        else:
            print("Money Not Enough! you have %s and by a car need %s" % (money,lst[0][1]))

    elif select.strip() == '2' or select.lower() == 'apple': 
        if money >lst[1][1]:
            money -=  lst[1][1]
            shoplist.append(lst[1][0])
        else:
            print("Money Not Enough! you have %s and by a apple need %s" % (money,lst[1][1]))

    elif select.strip() == '3' or select.lower() == 'pan':
        if money >lst[2][1]:
            money -=  lst[2][1]
            shoplist.append(lst[2][0])
        else:
            print("Money Not Enough! you have %s and by a pan need %s" % (money,lst[2][1]))

    elif select.strip() == '4' or select.lower() == 'book':
        if money >lst[3][1]:
            money -=  lst[3][1]
            shoplist.append(lst[3][0])
        else:
            print("Money Not Enough! you have %s and by a book need %s" % (money,lst[3][1]))

    else:
        print('not this shop..try again..')
    time.sleep(1)
    os.system('clear')
