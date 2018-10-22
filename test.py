import time
import os
import sys

def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print(sys.path[0])
    print(dname)

    time.sleep(100000)

if __name__ == '__main__':
    main()