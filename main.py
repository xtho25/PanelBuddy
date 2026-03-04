import sys
import os
import json
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication

from src.mainWidget import mainWidget
from src.configWidget import configWidget

# Reading config file
def read_config():
    with open("config.json", "r") as f:
        global settings
        settings = json.load(f)
        f.close()

def load_config():
    read_config()
    widget.setFrames(load_frames(settings["animation"]["type"], settings["animation"]["count"]))
    widget.setFps(settings["animation"]["fps"])
    widget.setSize(settings["size"])
    widget.setPixelArt(settings["pixel_art"])
    set_location()

def set_location():
    if settings["widget_placement"] == "bottom-right":
        x = geo.right() - widget.width() - settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    else:
        x = geo.left() + settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    widget.move(x, y)

def load_frames(prefix, count):
    frames = []
    for i in range(count):
        path = os.path.join(settings["assets_path"], prefix, f"{prefix}_{i}.png")
        frames.append(QPixmap(path))
    return frames

if __name__ == "__main__":
    read_config()

    # Linux force x11
    if sys.platform.startswith("linux") and settings["force_x11"]:
        print("Forcing xcb. To disable forcing specify it in config.")
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QtWidgets.QApplication([])

    screen = QGuiApplication.primaryScreen()
    geo = screen.availableGeometry()

    frames = load_frames(settings["animation"]["type"], settings["animation"]["count"])

    widget = mainWidget(frames, settings["size"], settings["animation"]["fps"], settings["pixel_art"])

    config_widget = configWidget()
    config_widget.configChanged.connect(load_config)

    set_location()

    widget.show()
    config_widget.show() # Remove later and put only open on taskbar icon

    sys.exit(app.exec())