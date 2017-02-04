import argparse, os, stat
import datetime


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


def more(x):
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
    lst[1] = '{:>2}'.format(str(len([v for v in os.listdir(x) if v[0] != '.']) if os.path.isdir(x) else 1))
    lst[2] = uid[str(st.st_uid)]
    lst[3] = gid[str(st.st_gid)]
    lst[4] = '{:>6}'.format(str(st.st_size))
    lst[5] = time.strftime('%b')
    lst[6] = time.strftime('%d')
    lst[7] = time.strftime('%H:%M')
    lst[8] = os.path.basename(x)
    return ' '.join(lst)


def show_all(x):
    if os.path.isfile(x):
        print(x)
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


def Show(x):
    if os.path.isfile(x):
        print(x)
    else:
        for i in os.listdir(x):
            if i[0] != '.':
                print(i, end='  ')
        print()


def _more(x):
    o = opt()
    if os.path.isfile(x):
        print(more(x))
    if o.a:
        total = 4096 * 2
        for l in os.listdir(x):
            total += os.stat(x + '/' + l).st_size
        print('total: %s' % (int(total // 1024)))
        print(more('.'))
        print(more('..'))
        for i in os.listdir(x):
            print(more(i))
    elif o.h:
        pass
    else:
        total = 0
        for l in os.listdir(x):
            total += os.stat(x + '/' + l).st_size
        print('total: %s' % int(total // 1024))
        for i in os.listdir(x):
            if i[0] != '.':
                print(more(i))


def option_stat(dest):
    op = opt()
    if not [v for v in vars(op).values() if v]:
        Show(dest)
    if op.l:
        _more(dest)
    elif op.a:
        show_all(dest)


def main():
    op = opt()
    if not op.argvs:
        option_stat('.')
    else:
        if len(op.argvs) == 1:
            if op.argvs[0] == '.':
                option_stat('.')
            else:
                option_stat(op.argvs[0])
        else:
            for k in op.argvs:
                option_stat(k)


if __name__ == '__main__':
    main()
