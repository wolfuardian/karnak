# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets

#
# class UIMainWindow(object):
#     @staticmethod
#     def setup_ui(main_window):
#         main_window.setObjectName("MainWindow")


window = None


def create_dialog():
    delete_dialog()
    global window
    if dialog is None:
        dialog = Dialog()
    dialog.show()


def delete_dialog():
    global window
    if dialog is None:
        return
    dialog.deleteLater()
    dialog = None


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QApplication.activeWindow()):
        super(Dialog, self).__init__(parent)

        display = 1
        screen_size = (1920, 1080)
        windows_size = (720, 640)
        pivot = (
            (display * screen_size[0]) + screen_size[0] / 2 - windows_size[0] / 2,
            screen_size[1] / 2 - windows_size[1] / 2
        )

        self.setObjectName('MainWindow')
        self.setWindowTitle(u'Windows Title {}'.format('0.2.6'))
        self.setGeometry(pivot[0], pivot[1], windows_size[0], windows_size[1])
        # self.setFixedWidth(720)
        # self.setFixedHeight(640)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        def add_widget(_widget, _parent, _layout, ):
            _widget.setLayout(_layout)
            _widget.layout().setContentsMargins(0, 0, 0, 0)
            _widget.layout().setSpacing(0)
            _parent.layout().add_widget(_widget)
            return _widget

        self.header = add_widget
        (
            QtWidgets.QFrame(),
            self,
            QtWidgets.QVBoxLayout()
        )


create_dialog()