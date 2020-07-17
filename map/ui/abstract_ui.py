class AbstractUI():

    def setupUi(self, model, *args, **kwargs):

        self.model = model

        self._initialize_misc(*args, **kwargs)
        self._initialize_content(*args, **kwargs)
        self._initialize_connections(*args, **kwargs)

    def _initialize_misc(self):
        pass

    def _initialize_content(self):
        pass

    def _initialize_connections(self):
        pass
