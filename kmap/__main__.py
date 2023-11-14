import sys

from kmap.kMap import kMap


def main():
    app = kMap(sys.argv)
    sys.exit(app.run())


if __name__ == "__main__":
    main()
