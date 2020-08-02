class IDGenerator():

    def __init__(self):

        self.id = 0

    def new_ID(self):

        self.id += 1

        return self.id

ID = IDGenerator()
