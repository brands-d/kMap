class AbstractUI():

    def setupUi(self, model):

        self.model = model

        self._initialize_misc()
        self._initialize_content()
        self._initialize_connections()

    def _initialize_misc(self):
        pass

    def _initialize_content(self):
        pass

    def _initialize_connections(self):
        pass
