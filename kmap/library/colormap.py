class Colormap:
    def __init__(self, name, pos, colors):
        self.name = name
        self.pos = pos
        self.colors = colors

    def toList(self):
        return [self.name, self.pos, self.colors]
