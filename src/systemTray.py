import json
import os
import sys
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Signal

class systemTray:
    #openConfig = Signal()
    def __init__(self, config_widget):
        with open("config.json", "r") as f:
            self.settings = json.load(f)
            f.close()

        self.config_widget = config_widget

        self.tray = QSystemTrayIcon(QIcon(os.path.join(self.settings["assets_path"], "icon.png")))

        self.menu = QMenu()

        self.configAction = QAction("Open Config")
        self.configAction.triggered.connect(self.config_widget.show)

        self.quitAction = QAction("Quit")
        self.quitAction.triggered.connect(QApplication.instance().quit)

        self.menu.addAction(self.configAction)
        self.menu.addSeparator()
        self.menu.addAction(self.quitAction)

        self.tray.setContextMenu(self.menu)
        self.tray.show()

if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    systray = systemTray()

    print("Tray available:", QSystemTrayIcon.isSystemTrayAvailable())
    print("Icon null:", systray.tray.icon().isNull())
    
    sys.exit(app.exec())