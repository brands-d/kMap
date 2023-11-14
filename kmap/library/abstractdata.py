class AbstractData:
    def __init__(self, ID, name, meta_data):
        self.name = name
        self.ID = ID
        self.meta_data = meta_data

    def __str__(self):
        rep = f"Name:\t{self.name}\nID:\t{self.ID}\n\nMeta Data\n"

        for key, value in self.meta_data.items():
            rep += f"{key}:\t\t{str(value)}\n"

        # Don't pass last new line
        return rep[:-2]
