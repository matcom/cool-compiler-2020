import sys
import errno
import os.path

def main(argv):
    print("COOLCompiler 1.0.3")
    print("Copyright (C) 2019-2020: Liset Silva Oropesa, Pablo A. de Armas Suárez, Yenli Gil Machado")

    if len(argv) < 2:
        print("ERROR: no input filename")
        return sys.exit(errno.EPERM)

    if not os.path.isfile(argv[1]):
        print("ERROR: invalid input filename: " + argv[1])
        return sys.exit(errno.EPERM)

    input = NoTabsFileStream(argv[1])

    print("3rd line")

    return sys.exit(errno.EPERM)

if __name__ == '__main__':
    main(sys.argv)
