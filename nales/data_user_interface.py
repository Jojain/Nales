class NalesPublicAPI:
    # This class is used to separate what's available to the user through the console
    # all the methods defined in this class are supposed to be accessible to the user so that he can retrieve
    # data from the app

    def __init__(self, mainwindow):
        self.mw = mainwindow

    def get_parameter(self, name):
        parameters = self.mw.param_model.parameters

        for param_name in parameters.keys():
            if param_name == name:
                return parameters[param_name]

    def get_part(self, name):
        nparts = self.mw.model.parts

        for npart in nparts:
            if npart.name == name:
                return npart.part

    def get_shape(self, name):
        pass

    def fitview(self) -> None:
        """
        Fit the view on objects in the viewer
        """
        self.mw.viewer.fit()

    def save(self, path: str = None) -> None:
        """
        Save the session is to `path` if provided else opens a filedialog
        """
        self.mw.save_file(path)

    def load(self, path: str = None) -> None:
        """
        If provided loads the file `path` in the session else opens a filedialog
        """
        self.mw.open_file(path)
