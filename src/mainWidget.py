from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication
from PySide6.QtCore import QTimer, Signal

class mainWidget(QtWidgets.QWidget):
    clicked = Signal()
    hovered = Signal()
    unhovered = Signal()
    mouseMove = Signal()

    def __init__(self, frames, size=1, fps=8, pixelArt=False):
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

        self.setFrames(frames)
        self.setSize(size)
        self.index = 0
        self.setPixelArt(pixelArt)
        self.setFps(fps)

        # Making the timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(int(1000/self.fps))

    def mousePressEvent(self, event):
        self.clicked.emit()
        return super().mousePressEvent(event)
 
    def mouseMoveEvent(self, event):
        self.mouseMove.emit()
        return super().mouseMoveEvent(event)

    def enterEvent(self, event):
        self.hovered.emit()
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.unhovered.emit()
        return super().leaveEvent(event)

    def setFps(self, fps):
        self.fps = fps
        self.update()

    def setFrames(self, frames):
        self.frames = frames
        self.update()

    def setPixelArt(self, pixelArt):
        self.pixelArt = pixelArt
        self.update()

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
        painter.setRenderHint(QPainter.SmoothPixmapTransform, not(self.pixelArt))
        painter.drawPixmap(self.rect(), self.frames[self.index])