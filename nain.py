#!/usr/bin/env python
# coding=utf-8

year = int(input('please input the year: '))
month = int(input('please input the month: '))
day = int(input("please input the day: "))

months = (0,31,59,90,120,151,181,212,243,273,304,334)

if 0<= month <=12:
    sum = months[month - 1]
else:
    print("month is input error.")

sum += day
leap = 0
if (year % 400 == 0 ) or ((year % 4 == 0) and (year % 100 != 0)):
    leap = 1
if (leap == 1) and (month >2):
    sum += 1
print('this day from the year %d day' % sum)



