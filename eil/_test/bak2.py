import os

from PySide2.QtCore import QFile, Slot, QMetaObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox


def load_ui_from(path):
    file = QFile(path)
    file.open(QFile.ReadOnly)

    ui = QUiLoader().load(file)

    file.close()
    return ui


class UIFileResolver(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

    @staticmethod
    def set_to(self):
        self.setObjectName('MainWindow')
        self.setWindowTitle('Karnak')
        display = 1
        screen_size = (1920, 1080)
        windows_size = (720, 640)
        pivot = (
            (display * screen_size[0]) + screen_size[0] / 2 - windows_size[0] / 2,
            screen_size[1] / 2 - windows_size[1] / 2
        )
        self.setGeometry(pivot[0], pivot[1], windows_size[0], windows_size[1])


window = None


def main_process():
    delete_dialog()

    global window

    if window is None:
        window = load_ui_from('C:/Users/eos/PycharmProjects/karnak/eil/tool/karnak/ui/file_resolver.ui')
        UIFileResolver.set_to(window)

    window.show()


def delete_dialog():
    global window

    if window is None:
        return

    window.deleteLater()
    window = None


main_process()
