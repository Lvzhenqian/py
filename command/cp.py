import argparse, sys, os
from functools import partial


def option():
    opt = argparse.ArgumentParser(description='Linux copy command')
    opt.add_argument('source',
                     nargs='?',
                     type=str,
                     help='source from a file')
    opt.add_argument('destination',
                     nargs='?',
                     type=str,
                     help='destination file or direction')
    opt.add_argument('-p',
                     '--preserve',
                     action='store_true',
                     default=False,
                     dest='preserve',
                     help='retain permission')
    opt.add_argument('-r',
                     '--recursive',
                     action='store_true',
                     default=False,
                     dest='r',
                     help='recursion copy file')
    return opt.parse_args()


def read(file):
    with open(file, 'rb') as fd:
        yield from fd


def write(sour, file):
    if os.path.exists(file):
        rqe = input('did you wan to overwrit "%s"! ' % (file))
        if rqe.lower() == 'yes':
            with open(file, mode='wb') as rev:
                while True:
                    try:
                        rev.write(next(sour))
                    except StopIteration:
                        break
    else:
        with open(file, mode='xb') as f:
            while True:
                try:
                    f.write(next(sour))
                except StopIteration:
                    break
    return True


def tree(source2, destination):
    s = source2.rstrip('/')
    d = destination.rstrip('/')
    new_sour = os.path.basename(s)
    dirs = []
    files = []
    for root, _, file in os.walk(s):
        top = d + '/' + new_sour + root.split(s)[1] if os.path.exists(d) else d + root.split(s)[1]
        dirs.append((root, top))
        if file:
            for f in file:
                files.append((root + '/' + f, top + '/' + f))
    return dirs, files


def preserve(s, det):
    s2 = os.stat(s)
    os.chmod(det, s2.st_mode)
    os.chown(det, s2.st_uid, s2.st_gid)
    os.utime(det, (s2.st_atime, s2.st_mtime))
    return True


def main():
    op = option()
    if not op.source or not op.destination:
        print('not source or not destination....error')
        sys.exit()
    if os.path.isfile(op.source):
        source = read(op.source)
        write_file = partial(write, source)
        dst = op.destination
        if os.path.isfile(dst):
            write_file(dst)
        else:
            dst = op.destination + '/' + os.path.basename(op.source)
            write_file(dst)
        if op.preserve:
            preserve(op.source, dst)
    elif op.r and os.path.isdir(op.source):
        mkdir = partial(os.makedirs, mode=511, exist_ok=True)
        dirs, files = tree(op.source, op.destination)
        print(dirs)
        for d in dirs:
            if not os.path.exists(d[1]):
                mkdir(d[1])
            if op.preserve:
                preserve(d[0], d[1])
        for f in files:
            s = read(f[0])
            write(s, f[1])
            if op.preserve:
                preserve(f[0], f[1])
    else:
        print('{} is a director please use -r or --recursive'.format(op.source))
        sys.exit()


if __name__ == '__main__':
    main()
