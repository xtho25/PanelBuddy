import sys
import os
import json
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication

# Constants
# Platform specific fixes
try:
    os.environ["QT_QPA_PLATFORM"] = "xcb"
except:
    pass

# Reading config file
with open("config.json", "r") as f:
    settings = json.load(f)
    ASSETS_PATH = settings["assets_path"]

class mainWidget(QtWidgets.QWidget):
    def __init__(self, image_path, scale=1.0):
        super().__init__()

        # Making Window Transparent
        mainWidget.setWindowFlags(self, QtCore.Qt.Window | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        mainWidget.setAttribute(self, QtCore.Qt.WA_TranslucentBackground)
        mainWidget.setAttribute(self, QtCore.Qt.WA_ShowWithoutActivating)

        # Making the pixmap
        self.pixmap = QPixmap(os.path.join(ASSETS_PATH, image_path))
        self.scale = scale
        self.setSize(scale)

    def setSize(self, scale):
        # Sets the size of the asset to the desired scale
        target_scale = scale * self.pixmap.size()
        print(target_scale)
        self.pixmap.scaled(target_scale)
        
        #self.resize(target_scale)

    def paintEvent(self, event):
        # Drawing the pixmap
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(self.rect(), self.pixmap) # fix cordinates based on bottom right left

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    screen = QGuiApplication.primaryScreen()
    geo = screen.availableGeometry()

    widget = mainWidget("idle_main", 0.5)
    widget.resize(160, 160)

    if settings["widget_placement"] == "bottom-right":
        x = geo.right() - widget.width() - settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    else:
        x = geo.left() + settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    widget.move(x, y)

    widget.show()

    sys.exit(app.exec())