import argparse,os


def opt():
    opt = argparse.ArgumentParser(prog='list program', description='writing like the linux list command')
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
    return opt.parse_args()



if __name__ == '__main__':
    op = opt()

    if len(op.argvs) == 1:
        if op.argvs[0] == '.':
            if op.a:
                print('.')
                print('..')
                print('   '.join(os.listdir(op.argvs.pop())))
            else:
                for p in os.listdir(op.argvs.pop()):
                    if p[0] != '.':
                        print(p,end='   ')
                print()
        elif os.path.isfile(op.argvs[0]):
            print(op.argvs.pop())
        else:
            if op.a:
                print('.')
                print('..')
                print('   '.join(os.listdir(op.argvs.pop())))
            else:
                for k in os.listdir(op.argvs.pop()):
                    if k[0] != '.':
                        print(k,end='  ')
    else:
        for i in op.argvs:
            if os.path.isfile(i):
                print(i,end='  ')
            else:
                print('\n')
                print('%s:'%i)
                print('   '.join(os.listdir(i)))
