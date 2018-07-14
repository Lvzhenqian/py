#!/usr/bin/env python 
#coding:utf-8
import sys,os
from optparse import OptionParser
def opt():
    parser = OptionParser(add_help_option=False)
    parser.add_option("-h","--human",
	          dest="humans",
	          action="store_true",
	          default=False,
	          help="easy to read the file size")
    parser.add_option("-s","--count",
	          dest="counts",
	          action="store_true",
	          default=False,
	          help="count the file size")
    option,arg2 = parser.parse_args()
    return option,arg2
def Get_dir(topdir):
    dir = os.walk(topdir)
    for p,d,f in dir:
        yield p
def Get_file_size(sz):
    size = 0
    wk = os.walk(sz)
    for p,d,f in wk:
        for i in f:
            fn = os.path.join(p,i)
            size += os.path.getsize(fn)
    return size
def print_size(size,filename):
    option,arg2=opt()
    if option.humans:
        if int(size) >= int(1024*1024*1024):
            print "%s  %s" % (str(round(float(size)/int(1024*1024*1024),1))+'G',filename)
        if int(size) < int(1024*1024*1024) and int(size) >= int(1024*1024):
            print "%s  %s" % (str(int(round(float(size)/int(1024*1024))))+'M',filename)
        if int(size) < int(1024*1024) and int(size) >= 1024 :
            print "%s  %s" % (str(int(round(float(size)/1024)))+'K',filename)

    else:
        print "%s  %s" % (int(round(float(size)/1024)),filename)

def main():
    args = sys.argv
    option,arg2=opt()
    del args[0]
    if option.counts:
        if len(args) > 1:
            file1=[i for i in args if os.path.isfile(os.path.abspath(i))]
            dir1=[i for i in args if os.path.isdir(os.path.join('.',i))]
            if file1:
                for f in file1:
                    size = os.path.getsize(f)
                    print_size(size,f)
            if dir1:
                for dir2 in dir1:
                    size = Get_file_size(dir2)
                    print_size(size,dir2)
        if len(args) == 1:
            for ar in args:
                if os.path.isfile(ar):
                    size = os.path.getsize(ar)
                    print_size(size,ar)
                if os.path.isdir(ar):
                    for dir3 in Get_dir(ar):
                        size=Get_file_size(dir3)
                        print_size(size,dir3)
    else:
        if len(args) > 1:
            file_1=[i for i in args if os.path.isfile(os.path.abspath(i))]
            dir_2=[os.path.join('.',i) for i in args if os.path.isdir(os.path.join('.',i))]
            if file_1:
                for f in file_1:
                    size = os.path.getsize(f)
                    print_size(size,f)
            if dir_2:
                for get1 in dir_2:
                    for dir_3 in Get_dir(get1):
                        size=Get_file_size(dir_3)
                        print_size(size,dir_3)
        if len(args) == 1:
            for ar in args:
                if os.path.isfile(ar):
                    size = os.path.getsize(ar)
                    print_size(size,ar)
                if os.path.isdir(ar):
                    for i in Get_dir(ar):
                        size=Get_file_size(i)
                        print_size(size,i)
if __name__ == '__main__':
    try:
        main()
    except IndexError:
        print "%s need a argument" % __file__
        sys.exit()
