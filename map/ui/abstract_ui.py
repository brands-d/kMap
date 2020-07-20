class AbstractUI():

    def setupUi(self, *args):

        self._initialize_misc(*args)
        self._initialize_content(*args)
        self._initialize_connections(*args)

    def _initialize_misc(self, *args):
        pass

    def _initialize_content(self, *args):
        pass

    def _initialize_connections(self, *args):
        pass
