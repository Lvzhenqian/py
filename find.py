import re,os,argparse

def option():
    opt = argparse.ArgumentParser(description='linux find command')
    opt.add_argument('-name',
                     action='store_true',
                     default=False,
                     dest='name',
                     help='Query by name')
    opt.add_argument('-type',
                     action='store_true',
                     default=False,
                     dest='type',
                     help='Query by file type')
    opt.add_argument('-ctime',
                     action='stort_true',
                     default=False,
                     dest='ctime',
                     help='Query by file ctime')
    opt.add_argument('-mtime')