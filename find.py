import re, os, argparse, stat
from datetime import datetime


def option():
    opt = argparse.ArgumentParser(description='linux find command')
    opt.add_argument('director',
                     nargs='?',
                     type=str,
                     help='source find director')
    opt.add_argument('-name',
                     nargs='?',
                     type=str,
                     dest='name',
                     help='Query by name')
    opt.add_argument('-type',
                     nargs='?',
                     type=str,
                     dest='type',
                     help='Query by file type')
    opt.add_argument('-ctime',
                     nargs='?',
                     type=str,
                     dest='ctime',
                     help='Query by file ctime')
    opt.add_argument('-mtime',
                     nargs='?',
                     type=str,
                     dest='mtime',
                     help='Query by file mtime')
    opt.add_argument('-cnewer',
                     nargs='?',
                     type=str,
                     dest='cnewer',
                     help='find cnewer file')
    opt.add_argument('-executable',
                     action='store_true',
                     default=False,
                     dest='executable',
                     help='find the executable file')
    opt.add_argument('-size',
                     nargs='?',
                     type=str,
                     dest='size',
                     help='Query by file size')
    opt.add_argument('-newer',
                     nargs='?',
                     type=str,
                     dest='newer',
                     help='File was modified more recently then file')
    opt.add_argument('-gid',
                     nargs='?',
                     type=str,
                     dest='gid',
                     help="-gid n File's numeric group ID is n")
    opt.add_argument('-uid',
                     nargs='?',
                     type=str,
                     dest='uid',
                     help="-uid n File's numeric user ID is n")
    return opt.parse_args()


def soure_list(x):
    lst = []
    for root, mi, f in os.walk(x):
        f.extend(mi)
        lst.extend([root + '/' + file for file in f])
    return lst


def Name(complie, source):
    ret = set()
    com = re.compile(complie)
    for st in source:
        if com.search(os.path.basename(st)):
            ret.add(st)
    return ret


def Type(arg, source):
    rule = {'d': stat.S_ISDIR, 'f': stat.S_ISREG, 'p': stat.S_ISFIFO, 'l': stat.S_ISLNK, 'b': stat.S_ISBLK,
            'c': stat.S_ISCHR, 's': stat.S_ISSOCK}
    ret = set()
    for src in source:
        t = os.stat(src)
        if rule[arg](t.st_mode):
            ret.add(src)
    return ret


def Time(which, arg, source):
    new = datetime.now().timestamp()
    ret = set()
    for src in [x for x in source if os.path.isfile(x)]:
        which_time = os.stat(src).st_ctime if which is 'ctime' else os.stat(src).st_mtime
        date = int((new - which_time) // (3600 * 24))
        if arg[0] == '+' and date > int(arg[1:]):
            ret.add(src)
        else:
            if arg[0] != '+' and date <= int(arg.lstrip('-')):
                ret.add(src)
    return ret


def ID(which, arg, source):
    uid, gid = {}, {}
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
    ret = set()
    for src in source:
        w = uid[str(os.stat(src).st_uid)] if which is 'uid' else gid[str(os.stat(src).st_gid)]
        if w == arg.strip():
            ret.add(src)
    return ret


def Executable(source):
    ret = set()
    for src in source:
        if os.access(src, os.X_OK):
            ret.add(src)
    return ret


def Newer(which, arg, source):
    ret = set()
    arg_mtime = os.stat(arg).st_mtime if which is 'newer' else os.stat(arg).st_ctime
    for src in source:
        src_mtime = os.stat(src).st_mtime
        if src_mtime > arg_mtime:
            ret.add(src)
    return ret


def Size(arg, source):
    rule = {'k': int(arg.strip('+-kK')) * 1024, 'm': int(arg.strip('+-mM')) * (1024 ** 2),
            'g': int(arg.strip('+-gG')) * (1024 ** 3), 'b': int(arg.strip('+-'))}
    ret = set()
    flag = int(arg.strip('+-')) if arg[-1].isdigit() else int(arg.strip('+-')) if arg[-1].lower() is 'c' else rule[
        arg[-1].lower()]
    for src in source:
        size = os.stat(src).st_blocks if arg[-1].isdigit() or arg[-1] is 'b' else os.stat(src).st_size
        if arg[0] is '+' and size > flag:
            ret.add(src)
        else:
            if arg[0] != '+' and size <= flag:
                ret.add(src)
    return ret


def Show(slist):
    opt = option()
    ret = set()
    if not [v for v in vars(opt).values() if v]:
        slist.insert(0, '.')
        ret = slist
    if opt.name:
        flag = Name(opt.name, slist)
        ret = ret & flag if ret else flag
    if opt.type:
        flag = Type(opt.type, slist)
        ret = ret & flag if ret else flag
    if opt.ctime:
        flag = Time('ctime', opt.ctime, slist)
        ret = ret & flag if ret else flag
    if opt.mtime:
        flag = Time('mtime', opt.mtime, slist)
        ret = ret & flag if ret else flag
    if opt.uid:
        flag = ID('uid', opt.uid, slist)
        ret = ret & flag if ret else flag
    if opt.gid:
        flag = ID('gid', opt.gid, slist)
        ret = ret & flag if ret else flag
    if opt.executable:
        flag = Executable(slist)
        ret = ret & flag if ret else flag
    if opt.newer:
        flag = Newer('newer', opt.newer, slist)
        ret = ret & flag if ret else flag
    if opt.cnewer:
        flag = Newer('cnewer', opt.cnewer, slist)
        ret = ret & flag if ret else flag
    if opt.size:
        flag = Size(opt.size, slist)
        ret = ret & flag if ret else flag

    return ret


def main():
    opt = option()

    if not opt.director or opt.director is '.':
        sl = soure_list('.')
        for p in Show(sl):
            print(p)
    else:
        sl = soure_list(opt.director)
        for fp in Show(sl):
            print(fp)


if __name__ == '__main__':
    main()
