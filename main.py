import sys
import os
import json
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication

from src.mainWidget import mainWidget

# Reading config file
with open("config.json", "r") as f:
    settings = json.load(f)
    ASSETS_PATH = settings["assets_path"]

# Linux force x11
if sys.platform.startswith("linux") and settings["force_x11"]:
    print("Forcing xcb. To disable forcing specify it in config.")
    os.environ["QT_QPA_PLATFORM"] = "xcb"

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    screen = QGuiApplication.primaryScreen()
    geo = screen.availableGeometry()

    widget = mainWidget(os.path.join(ASSETS_PATH, "idle_main"))
    widget.setFixedSize(160, 160) #Deafault size (might change it later)

    widget.setSize(settings["size"])

    if settings["widget_placement"] == "bottom-right":
        x = geo.right() - widget.width() - settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    else:
        x = geo.left() + settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    widget.move(x, y)

    if sys.platform == "win32":
        make_click_through(self.winId())

    widget.show()

    sys.exit(app.exec())