import json
from enum import StrEnum
from PySide6.QtCore import QTimer, Signal, QObject

class PetState(StrEnum):
    IDLE = "run" # Change this
    LOOK = "look"
    SLEEP = "sleep"
    CLICKED = "look" # Also this
    HOVERED = "hovered"

class stateManager(QObject):
    stateChanged = Signal()
    def __init__(self, widget):
        super().__init__()
        with open("config.json", "r") as f:
            self.settings = json.load(f)
            f.close()

        self.state = PetState.IDLE
        self.widget = widget

        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self.on_sleep)
        self.idle_timer.start(self.settings["sleep_time"]*1000) # 30 seconds


    def getState(self):
        return self.state

    def setState(self, state):
        if self.state == state:
            return
        
        self.state = state
        self.stateChanged.emit()

    def on_click(self):
        self.setState(PetState.CLICKED)

    def on_hover(self):
        self.setState(PetState.HOVERED)

    def on_unhover(self):
        self.setState(PetState.IDLE)

    def on_sleep(self):
        self.setState(PetState.SLEEP)

    def timer_reset(self):
        self.idle_timer.start(self.settings["sleep_time"]*1000)