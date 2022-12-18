import os

from PySide2.QtCore import QFile, Slot, QMetaObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox


# SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class UiLoader(QUiLoader):
    def __init__(self, baseinstance, customWidgets=None):

        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance
        self.customWidgets = customWidgets

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            return self.baseinstance

        else:
            if class_name in self.availableWidgets():
                widget = QUiLoader.createWidget(self, class_name, parent, name)

            else:

                try:
                    widget = self.customWidgets[class_name](parent)

                except (TypeError, KeyError) as e:
                    raise Exception(
                        'No custom widget ' + class_name + ' found in customWidgets param of UiLoader __init__.')

            if self.baseinstance:
                setattr(self.baseinstance, name, widget)

            return widget


def load_ui(uifile, baseinstance=None, customWidgets=None, workingDirectory=None):
    loader = UiLoader(baseinstance, customWidgets)
    print(loader)

    if workingDirectory is not None:
        loader.setWorkingDirectory(workingDirectory)

    widget = loader.load(uifile)
    QMetaObject.connectSlotsByName(widget)
    return widget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        load_ui('C:/Users/eos/PycharmProjects/karnak/eil/tool/karnak/ui/file_resolver.ui', self)


window = MainWindow()
window.show()

# def load_ui_from(path):
#     file = QFile(path)
#     file.open(QFile.ReadOnly)
#
#     ui = QUiLoader().load(file)
#
#     file.close()
#     return ui
#
#
# w = load_ui_from('C:/Users/eos/PycharmProjects/karnak/eil/tool/karnak/ui/file_resolver.ui')
# ww = UIFileResolver(w)
# ww.show()

#
# class UIFileResolver(object):
#     @staticmethod
#     def set_to(self):
#         self.setObjectName('MainWindow')
#         self.setWindowTitle('Karnak')
#         display = 1
#         screen_size = (1920, 1080)
#         windows_size = (720, 640)
#         pivot = (
#             (display * screen_size[0]) + screen_size[0] / 2 - windows_size[0] / 2,
#             screen_size[1] / 2 - windows_size[1] / 2
#         )
#         self.setGeometry(pivot[0], pivot[1], windows_size[0], windows_size[1])

#
# window = None


# def main_process():
#     delete_dialog()
#
#     global window
#
#     if window is None:
#         window = load_ui_from('C:/Users/eos/PycharmProjects/karnak/eil/tool/karnak/ui/file_resolver.ui')
#         UIFileResolver.set_to(window)
#
#     window.show()
#
#
# def delete_dialog():
#     global window
#
#     if window is None:
#         return
#
#     window.deleteLater()
#     window = None
#
#
# main_process()
