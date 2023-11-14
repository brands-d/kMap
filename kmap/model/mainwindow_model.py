from kmap import __version__, __date__


class MainWindowModel:
    def __init__(self, controller):
        self.controller = controller

    def get_about_text(self, path):
        title = "kMap.py"
        with open(path, "r") as file:
            text = file.read() % (__version__, __date__)

        return title, text
