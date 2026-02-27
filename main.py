import sys
import os
import json
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication

from src.mainWidget import mainWidget
from src.configWidget import configWidget

# Reading config file
with open("config.json", "r") as f:
    settings = json.load(f)
    ASSETS_PATH = settings["assets_path"]
    f.close()

# Linux force x11
if sys.platform.startswith("linux") and settings["force_x11"]:
    print("Forcing xcb. To disable forcing specify it in config.")
    os.environ["QT_QPA_PLATFORM"] = "xcb"

def load_frames(prefix, count):
    frames = []
    for i in range(count):
        path = os.path.join(ASSETS_PATH, prefix, f"{prefix}_{i}.png")
        frames.append(QPixmap(path))
    return frames

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    screen = QGuiApplication.primaryScreen()
    geo = screen.availableGeometry()

    frames = load_frames(settings["animation"]["type"], settings["animation"]["count"])

    widget = mainWidget(frames, settings["size"], settings["animation"]["fps"], settings["pixel_art"])
    config_widget = configWidget()

    if settings["widget_placement"] == "bottom-right":
        x = geo.right() - widget.width() - settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    else:
        x = geo.left() + settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    widget.move(x, y)

    widget.show()
    config_widget.show() # Remove later and put only open on taskbar icon

    sys.exit(app.exec())