import argparse, sys


def opt():
    opt = argparse.ArgumentParser(description='for linux cat command')
    opt.add_argument('file',
                     type=str,
                     nargs='*')
    opt.add_argument('-E',
                     '-e',
                     action='store_true',
                     default=False,
                     dest='last',
                     help='show ends. display $ at end of each line')
    opt.add_argument('-n',
                     '--number',
                     action='store_true',
                     default=False,
                     dest='number',
                     help='number all output lines')

    return opt.parse_args()


def args(x,y, **kwargs):
    if kwargs['last'] and kwargs['number']:
        print('{:>6}  {}'.format(y, x.replace('\n', '$')))
    elif kwargs['last']:
        print(x.replace('\n', '$'))
    elif kwargs['number']:
        print('{:>6}  {}'.format(y, x))


if __name__ == '__main__':
    opt = opt()
    js = 1
    if len(opt.file) == 0:
        read = sys.stdin
        for i in read.readlines():
            if not opt.last and not opt.number:
                print(i.strip())
            else:
                args(i,js, last=opt.last, number=opt.number)
                js += 1
    else:
        with open(opt.file[0], 'r') as a:
            for f in a.readlines():
                if not opt.last and not opt.number:
                    print(f.strip())
                else:
                    args(f.strip(),js, last=opt.last, number=opt.number)
                    js += 1
