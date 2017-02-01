import argparse, os, stat
import datetime
from functools import partial


def opt():
    opt = argparse.ArgumentParser(prog='list program', add_help=False,
                                  description='writing like the linux list command')
    opt.add_argument('argvs',
                     type=str,
                     nargs='*')
    opt.add_argument('-l',
                     action='store_true',
                     default=False,
                     dest='l',
                     help='more than infomation to list')
    opt.add_argument('-a',
                     action='store_true',
                     default=False,
                     dest='a',
                     help='list all file')
    opt.add_argument('-h',
                     action='store_true',
                     default=False,
                     dest='h',
                     help='count size')
    return opt.parse_args()


def lsmore(x):
    uid = {}
    gid = {}
    with open('/etc/passwd') as f:
        ne = f.readline()
        while ne:
            tu = ne.split(':')
            uid[tu[2]] = tu[0]
            ne = f.readline()
    with open('/etc/group') as g:
        gn = g.readline()
        while gn:
            gt = gn.split(':')
            gid[gt[2]] = gt[0]
            gn = g.readline()
    lst = [str(i) for i in range(9)]
    st = os.stat(x)
    time = datetime.datetime.fromtimestamp(st.st_ctime)
    lst[0] = stat.filemode(st.st_mode)
    if os.path.isdir(x):
        lst[1] = str(len(os.listdir(x)))
    lst[2] = uid[str(st.st_uid)]
    lst[3] = gid[str(st.st_gid)]
    lst[4] = str(st.st_size)
    lst[5] = time.strftime('%b')
    lst[6] = time.strftime('%d')
    lst[7] = time.strftime('%H:%M')
    lst[8] = os.path.basename(x)
    return ' '.join(lst)


def alllist(x):
    f = ['.', '..']
    if x == '.':
        f.extend(os.listdir('.'))
        for st in range(6, len(f) + 1, 6):
            print(' '.join(f[st - 6:st]))
    elif os.path.isdir(x):
        f.extend(os.listdir(x))
        for st in range(6, len(f) + 1, 6):
            print(f[st - 6:st])
    else:
        print(x)


def option_stat(opt, y):
    if not opt.a and not opt.h and not opt.l:
        if os.path.isfile(y):
            print(y)
        else:
            for j in os.listdir(y):
                if j[0] != '.':
                    print(j, end='  ')
            print()
    elif opt.a:
        if os.path.isfile(y):
            print(y)
        else:
            alllist(y)
    elif opt.l:
        if os.path.isfile(y):
            print(lsmore(y))
        else:
            total=0
            for l in os.listdir(y):
                total += os.stat(y+'/'+l).st_size
            print('total: %s'% total)
            for i in os.listdir(y):
                print(lsmore(i))
    elif opt.l and opt.h:
        pass
    elif opt.a and opt.h:
        if os.path.isfile(y):
            print(y)
        else:
            alllist(y)


def main():
    op = opt()
    st = partial(option_stat, op)
    if not op.argvs:
        st('.')
    else:
        if len(op.argvs) == 1:
            if op.argvs[0] == '.':
                st('.')
            else:
                st(op.argvs[0])
        else:
            for k in op.argvs:
                st(k)


if __name__ == '__main__':
    main()
