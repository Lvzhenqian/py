#!/usr/bin/env python
# coding=utf-8
import argparse

opt = argparse.ArgumentParser(description='test')
opt.add_argument('file',
                 nargs='*',
                 type=str)
opt.add_argument('-l',
                 action='store_true',
                 default=False,
                 help='hh')

opt.add_argument('-n',
                 '--number',
                 action='store_true',
                 default=False,
                 dest='number',
                 help='hh')

arg = opt.parse_args()
#print(opt.file)
print(arg.file)
print(arg)
print(arg.number)

