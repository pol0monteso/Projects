class IISWindow:
    ID = "3a425f07-e7d6-4595-8111-52d01dc6a2c8"
    MenuEnabled = "True"
    TraceWindow = "True"
    MainWindow = "True"
    VisibleWindow = "True"
    AllowResizing = "True"

    def __init__(self, Header, WindowWidth, WindowHeight, Background):
        self.MainWindow = None
        self.TraceWindow = None
        self.MenuEnabled = None
        self.ID = None
        self.VisibleWindow = None
        self.Header = Header
        self.WindowWidth = WindowWidth
        self.WindowHeight = WindowHeight
        self.Background = Background

    @classmethod
    def default(cls):
        return cls(Header="MainCanvas", WindowHeight=800, WindowWidth=600, Background="#FFA9A9A9", )

    def initWindowFromXaml(self, root):
        for key, value in root.attrib.items():

            if key == "Name":
                self.Header = value
            if key == "Width":
                self.WindowWidth = value
            if key == "Height":
                self.WindowHeight = value
            if key == "Background":
                self.Background = value
            if key == "Width":
                self.WindowWidth = value

            # Add Standard Window values
            self.ID = "3a425f07-e7d6-4595-8111-52d01dc6a2c8"
            self.MenuEnabled = "True"
            self.TraceWindow = "True"
            self.MainWindow = "True"
            self.VisibleWindow = "True"
            self.AllowResizing = "True"

    def set_Header(self, new_header):
        self.Header = new_header

    def get_Header(self):
        return self.Header

    def set_WindowWidth(self, new_width):
        self.WindowWidth = new_width

    def get_WindowWidth(self):
        return self.WindowWidth

    def set_WindowHeight(self, new_height):
        self.WindowHeight = new_height

    def get_WindowHeight(self):
        return self.WindowHeight

    def set_Background(self, new_background):
        self.Background = new_background

    def get_Background(self):
        return self.Background