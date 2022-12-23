import functools

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class QtDefaultWidget(QtWidgets.QWidget):
    """QWidgetの自動削除Attribute設定
    """

    def __init__(self, parent=None, *args, **kwargs):
        super(QtDefaultWidget, self).__init__(parent=parent, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class FrameLayoutWidget(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FrameLayoutWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setObjectName('FrameLayoutWidget')

        # # PySideで作成したFrameLayout
        # self.__dummy_frame = qt.FrameLayout(self)
        # # FrameLayoutが閉じた状態になった時の処理を登録
        # self.__dummy_frame.frame_btn.collapsed.add(lambda: print('collapsed'))
        # # FrameLayoutが開いた状態になった時の処理を登録
        # self.__dummy_frame.frame_btn.expanded.add(lambda: print('expanded'))
        # # FrameLayoutをWidgetに追加
        # self.layout().addWidget(self.__dummy_frame)

        # for i in range(5):
        #     # FrameLayoutに追加するボタンを作成
        #     btn = QtWidgets.QPushButton(str(i))
        #     # ボタンが押されたときの処理を登録
        #     btn.clicked.connect(functools.partial(print, i))
        #
        #     # FrameLayoutにボタンを追加
        #     self.__dummy_frame.frame_layout.addWidget(btn)


if __name__ == "__main__":
    button = FrameLayoutWidget()
    button.show(dockable=True)
