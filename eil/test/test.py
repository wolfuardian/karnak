from PySide2 import QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set the window title and size
        self.setWindowTitle("My Window")
        self.resize(400, 300)

        # Create a widget to hold the layout
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)

        # Create a layout for the widget
        layout = QtWidgets.QVBoxLayout(widget)

        # Add a label to the layout
        label = QtWidgets.QLabel("Hello, world!")
        layout.addWidget(label)

        # Add a push button to the layout
        button = QtWidgets.QPushButton("Click me")
        layout.addWidget(button)


# Create an instance of the main window
window = MainWindow()

# Show the window
window.show()