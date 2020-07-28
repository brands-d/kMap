class AbstractUI():
    """Defines an abstract UI class.

    This class defines an abstract UI model to be inherited from by all
    UI-classes. UI classes are classes that are intended to encapsulate
    the individual GUI elements look, it's connections and other
    "boring" stuff. It should not handle any type of buisness logic.

    Calling the setupUI of this class will then call three abstract
    methods to be overwritten by the subclass. Those methods are not
    explicitly declared abstract to give the user the option to not use
    any particular one.
    """

    def setupUI(self):
        """Sets up the GUI elements by calling the _initialize_misc,
        _initialize_misc and _initialize_connections method in this
        order. In general do not overwrite this method and call it
        in the constructor of your UI class after setting other
        important variables.
        """

        self._initialize_misc()
        self._initialize_content()
        self._initialize_connections()

    def _initialize_misc(self):
        """Abstract method to be overwritten but not directly called.
        Please put any miscellaneous code in here that is necessary,
        like window title or geometry of windows.
        """
        pass

    def _initialize_content(self):
        """Abstract method to be overwritten but not directly called.
        Main method to put in all the code that creates and defines the
        individual parts of GUI like spinboxes or plot items. Please
        define all of the elements to be accessed outside as class
        members and elements like layouts can usually have a local
        scope.
        """
        pass

    def _initialize_connections(self):
        """Abstract method to be overwritten but not directly called.
        Set up all the connections and signals here. The slots can be
        defined here in this class but plase do not implemented them
        here. The complete buisness logic is to be performed in the
        corresponding view class.
        """
        pass
