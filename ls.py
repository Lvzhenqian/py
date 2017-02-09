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


def color(x):
    st = os.stat(x, follow_symlinks=False)
    if stat.S_ISLNK(st.st_mode):
        return '\033[1;36m{}\033[0m'.format(x)
    if os.path.isdir(x):
        return '\033[1;34m{}\033[0m'.format(x)
    else:
        return '{}'.format(x)


def more(x, h=False):
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
    st = os.stat(x, follow_symlinks=False)
    time = datetime.datetime.fromtimestamp(st.st_ctime)
    lst[0] = stat.filemode(st.st_mode)
    lst[1] = '{:>2}'.format(st.st_nlink)
    lst[2] = uid[str(st.st_uid)]
    lst[3] = gid[str(st.st_gid)]
    if h:
        for n, i in enumerate([(1024 ** 3, 'G'), (1024 ** 2, 'M'), (1024, 'K'), (0, '')]):
            if st.st_size > i[0]:
                size = st.st_size / 1024 ** (3 - n)
                if size > 100 and i[0] != 0 and os.path.isfile(x):
                    lst[4] = '{:>4.4}{}'.format('%d' % (size), i[1])
                elif i[0] == 0:
                    lst[4] = '{:>5}'.format(str(int(st.st_size)))
                else:
                    lst[4] = '{:>4.4}{}'.format('%0.2f' % (size), i[1])
                break
    else:
        lst[4] = '{:>5}'.format(str(st.st_size))
    lst[5] = time.strftime('%b')
    lst[6] = time.strftime('%d')
    lst[7] = time.strftime('%H:%M')
    lst[8] = '{} -> {}'.format(color(os.path.basename(x)), os.readlink(x)) if os.path.islink(x) else color(os.path.basename(x))
    return ' '.join(lst)


def show_all(x):
    if os.path.isfile(x):
        print(color(x))
    f = ['.', '..']
    if x == '.':
        f.extend(os.listdir('.'))
        pf=sorted([color(x) for x in f])
        for st in range(6, len(pf) + 1, 6):
            print('  '.join(pf[st - 6:st]))
    elif os.path.isdir(x):
        f.extend(os.listdir(x))
        pf = sorted([color(x) for x in f])
        for st in range(6, len(pf) + 1, 6):
            print('  '.join(pf[st - 6:st]))
    else:
        print(color(x))


def Show(x):
    if os.path.isfile(x):
        print(color(x))
    else:
        for i in os.listdir(x):
            if i[0] != '.':
                print(color(i), end='  ')
        print()


def _more(x):
    o = opt()
    if os.path.isfile(x) or os.path.islink(x):
        print(more(x))
        return

    if o.h and o.a:
        total = 0
        for l in os.listdir(x):
            total += os.stat(x + '/' + l).st_size
        for n, p in enumerate([(1024 ** 3, 'G'), (1024 ** 2, 'M'), (1024, 'K'), (0, '')]):
            if total > p[0]:
                print('total: %s%s' % (int(total // 1024 ** (3 - n)), p[1]))
                break
        print(more('.'))
        print(more('..'))
        for i in os.listdir(x):
            print(more(x + '/' + i, h=True))
    elif o.h:
        total = 0
        for l in os.listdir(x):
            total += os.stat(x + '/' + l).st_size
        for n, p in enumerate([(1024 ** 3, 'G'), (1024 ** 2, 'M'), (1024, 'K'), (0, '')]):
            if total > p[0]:
                print('total: %s%s' % (int(total // 1024 ** (3 - n)), p[1]))
                break
        for i in os.listdir(x):
            if os.path.basename(i)[0] != '.':
                print(more(x + '/' + i, h=True))
    elif o.a:
        total = 4096 * 2
        for l in os.listdir(x):
            total += os.stat(x + '/' + l).st_size
        print('total: %s' % (int(total // 1024)))
        print(more('.'))
        print(more('..'))
        for i in os.listdir(x):
            print(more(i))
    else:
        total = 0
        for l in os.listdir(x):
            total += os.stat(x + '/' + l).st_size
        print('total: %s' % int(total // 1024))
        for i in os.listdir(x):
            if os.path.basename(i)[0] != '.':
                print(more(x + '/' + i))


def option_stat(dest):
    op = opt()
    if not [v for v in vars(op).values() if v]:
        Show(dest)
    if op.l:
        _more(dest)
    elif op.a:
        show_all(dest)
    elif op.h:
        if os.path.isfile(dest):
            print(color(dest))
        else:
            for k in os.listdir(dest):
                print(color(k), end='  ')
            print()


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
