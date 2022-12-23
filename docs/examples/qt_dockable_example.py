from PySide2 import QtWidgets

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class MyDockableButton(MayaQWidgetDockableMixin, QtWidgets.QPushButton):
    def __init__(self):
        super(MyDockableButton, self).__init__()

        self.setText("My Button")


if __name__ == "__main__":
    button = MyDockableButton()
    button.show(dockable=True)
