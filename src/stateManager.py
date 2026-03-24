from enum import StrEnum

class PetState(StrEnum):
    IDLE = "run" # Change this
    LOOK = "look"
    SLEEP = "sleep"
    CLICKED = "clicked"
    HOVERED = "hovered"

class stateManager:
    def __init__(self, widget):
        self.state = PetState.IDLE
        self.widget = widget

    def getState(self):
        return self.state

    def setState(self, state):
        if self.state == state:
            return
        
        self.state = state
        #self.widget.set_state()