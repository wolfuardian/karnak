import maya.OpenMayaUI as OpenMayaUI
from PySide2 import QtWidgets, QtGui
from shiboken2 import wrapInstance

# Get the main Maya window as a Qt widget
main_window = OpenMayaUI.MQtUtil.mainWindow()
window = wrapInstance(int(main_window), QtWidgets.QWidget)

for child in window.children()[:]:
    print(child.objectName())

# Create a new widget to hold the layout
widget = QtWidgets.QWidget(parent=window)

# Create a layout for the widget
layout = QtWidgets.QVBoxLayout(widget)

# Add a label to the layout
label = QtWidgets.QLabel("Hello, world!")
layout.addWidget(label)

# Add a push button to the layout
button = QtWidgets.QPushButton("Click me")
layout.addWidget(button)

# Show the widget
widget.show()
