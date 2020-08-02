from kmap import __version__


class MainWindowModel():

    def __init__(self, controller):

        self.controller = controller

    def get_about_text(self, path):

        title = 'kMap'
        with open(path, 'r') as file:
            text = file.read() % __version__

        return title, text

    def reload_settings(self):
        pass
