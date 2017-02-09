#!/usr/bin/env python
# coding=utf-8

str = [str(x) for x in range(20)]
for i in range(6,len(str),6):
    print('\t'.join(str[(i-6):i])+'\n',end='')
