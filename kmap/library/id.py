class IDGenerator:
    def __init__(self):
        self.id = 0

    def new_ID(self):
        self.id += 1

        return self.id

    def update(self, new_id):
        if self.id <= new_id:
            self.id = new_id + 1


ID = IDGenerator()
