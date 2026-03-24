import sys
import os
import json
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication

from src.mainWidget import mainWidget
from src.configWidget import configWidget
from src.systemTray import systemTray
from src.stateManager import PetState, stateManager

# Reading config file
def read_config():
    with open("config.json", "r") as f:
        global settings
        settings = json.load(f)
        f.close()

def read_animation_config(prefix):
    with open(os.path.join(settings["assets_path"], prefix, "settings.json"), "r") as f:
        global animation_settings
        animation_settings = json.load(f)
        f.close()

def load_config():
    read_config()
    read_animation_config(state_manager.getState())

    widget.setFrames(animations[str(state_manager.getState())]) # FIX evrything atp
    widget.setFps(animation_settings["fps"])
    widget.setSize(settings["size"])

    widget.setPixelArt(animation_settings["pixel_art"])

    set_location()

def set_location():
    if settings["widget_placement"] == "bottom-right":
        x = geo.right() - widget.width() - settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    else:
        x = geo.left() + settings["margins"][0]
        y = geo.bottom() - widget.height() - settings["margins"][1]
    widget.move(x, y)

def load_frames(loadPath):
    frames = []
    for path in os.listdir(loadPath):
        if os.path.splitext(path)[1] != ".png": continue 
        
        realPath = os.path.join(loadPath, path)
        
        frames.append(QPixmap(realPath))
    return frames

def load_animations():
    animations = {}

    for dir in os.listdir(settings["assets_path"]):
        actualPath = os.path.join(settings["assets_path"], dir)
        if os.path.isdir(actualPath):
            animations[dir] = load_frames(actualPath)

    return animations

if __name__ == "__main__":
    read_config()

    # Linux force x11
    if sys.platform.startswith("linux") and settings["force_x11"]:
        print("Forcing xcb. To disable forcing specify it in config.")
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)

    screen = QGuiApplication.primaryScreen()
    geo = screen.availableGeometry()

    animations = load_animations()

    frames = animations[str(PetState.IDLE)] # Startup state
    read_animation_config(str(PetState.IDLE))

    widget = mainWidget(frames, settings["size"], animation_settings["fps"], animation_settings["pixel_art"])

    state_manager = stateManager(widget)
    
    config_widget = configWidget()
    config_widget.configChanged.connect(load_config)
    
    sysTray = systemTray(config_widget)
    
    set_location()

    widget.show()

    sys.exit(app.exec())