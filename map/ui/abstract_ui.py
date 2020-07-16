class AbstractUI():

    def setupUi(self, widget):

        self._initialize_geometry(widget)
        self._initialize_misc(widget)
        self._initialize_content(widget)
        self._initialize_connections(widget)
        self._initialize_sub_content(widget)

    def _initialize_geometry(self, widget):
        pass

    def _initialize_misc(self, widget):
        pass

    def _initialize_content(self, widget):
        pass

    def _initialize_connections(self, widget):
        pass

    def _initialize_sub_content(self, widget):
        pass
