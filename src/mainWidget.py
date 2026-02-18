from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication
from PySide6.QtCore import QTimer

class mainWidget(QtWidgets.QWidget):
    def __init__(self, frames, size=1, fps=8):
        super().__init__()

        # Making Window Transparent / Adding properties(flags, attributes)
        mainWidget.setWindowFlags(self, 
                                  QtCore.Qt.Window | 
                                  QtCore.Qt.Tool | 
                                  QtCore.Qt.WindowStaysOnTopHint | 
                                  QtCore.Qt.FramelessWindowHint)
        mainWidget.setAttribute(self, QtCore.Qt.WA_TranslucentBackground)
        mainWidget.setAttribute(self, QtCore.Qt.WA_ShowWithoutActivating)
        mainWidget.setAttribute(self, QtCore.Qt.WA_TransparentForMouseEvents)

        self.frames = frames
        self.setSize(size)
        self.index = 0

        # Making the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(int(1000/fps))

    def setSize(self, scale=1):
        # Sets the size of the asset to the desired scale
        self.scale=scale
        target_scale = self.scale * self.frames[0].size()
        self.resize(target_scale)
        self.setFixedSize(target_scale) #Sets window scale to sprite scale
        self.update() #No idea what this does ._.

    def sizeHint(self, scale):
        return scale * self.frames[0].size()
    
    def next_frame(self):
        self.index = (self.index + 1) % len(self.frames) #Resets index after it hits the amount of frames
        self.update()


    def paintEvent(self, event):
        # Drawing the pixmap
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(self.rect(), self.frames[self.index])