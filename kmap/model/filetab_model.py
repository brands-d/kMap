class FileViewerTabModel():

    def __init__(self):

        self.text = ''

    def read_file(self, path):

        with open(path, 'r') as file:
            self.text = file.read()


class FileEditorTabModel(FileViewerTabModel):

    def save_file(self, text, path):

        with open(path, 'wt') as file:
            file.write(text)
