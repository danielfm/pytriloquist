class Dialog(object):
    """
    Dialog base class.
    """
    def __init__(self, app, parent=None):
        """Creates a new dialog.
        """
        self.initialized = False
        self.app, self.parent = app, parent

    def execute(self, force=False):
        """Executes this dialog.
        """
        self.app.set_title(self.get_title())

        if force or not self.initialized:
            self.initialized = True
            self.init_ui()

        self.display()

    def back(self):
        """Executes the parent dialog.
        """
        if self.parent:
            self.parent.execute()

    def init_ui(self):
        """Creates the UI elements.
        """
        raise NotImplementedError

    def display(self):
        """Displays the UI on the screen.
        """
        raise NotImplementedError

    def get_title(self):
        """Returns the dialog title. This default implementation raises
        NotImplementedError.
        """
        raise NotImplementedError
