import sys

def tailf(x):
    with open(x,'rt') as f:
        while True:
            try:
                print(f.readline(),end='')
            except KeyboardInterrupt:
                break
            except Exception:
                pass

if __name__ == '__main__':
    tailf(sys.argv[1])