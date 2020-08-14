class AbstractData():

    def __init__(self, ID, name, meta_data):

        self.name = name
        self.ID = ID
        self.meta_data = meta_data

    def __str__(self):

        rep = 'Name:\t%s\nID:\t%s\n\nMeta Data\n' % (self.name, self.ID)

        for key, value in self.meta_data.items():
            rep += '%s:\t\t%s\n' % (key, str(value))

        # Don't pass last new line
        return rep[:-2]
