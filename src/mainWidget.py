from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication


class mainWidget(QtWidgets.QWidget):
    def __init__(self, image_path):
        super().__init__()

        # Making Window Transparent
        mainWidget.setWindowFlags(self, 
                                  QtCore.Qt.Window | 
                                  QtCore.Qt.Tool | 
                                  QtCore.Qt.WindowStaysOnTopHint | 
                                  QtCore.Qt.FramelessWindowHint)
        mainWidget.setAttribute(self, QtCore.Qt.WA_TranslucentBackground)
        mainWidget.setAttribute(self, QtCore.Qt.WA_ShowWithoutActivating)
        mainWidget.setAttribute(self, QtCore.Qt.WA_TransparentForMouseEvents)

        # Making the pixmap
        self.pixmap = QPixmap(image_path)

    def setSize(self, scale):
        # Sets the size of the asset to the desired scale
        target_scale = scale * self.pixmap.size()
        self.resize(target_scale)

    def paintEvent(self, event):
        # Drawing the pixmap
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(self.rect(), self.pixmap)