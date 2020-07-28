import sys
from kmap.kMap import kMap


if __name__ == '__main__':
    app = kMap(sys.argv)
    sys.exit(app.run())
