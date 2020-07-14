import sys
from map.Map import Map


if __name__ == '__main__':
    app = Map(sys.argv)
    sys.exit(app.run())
