import sys
import os
import json
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel, QCheckBox, QSlider, QFileDialog, QPushButton, QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QComboBox, QDoubleSpinBox
from PySide6.QtGui import QPixmap, QPainter, QGuiApplication, QFont
from PySide6.QtCore import Qt
from pathlib import Path

class configWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        with open("config.json", "r") as f:
            self.settings = json.load(f)
            f.close()

        self.setWindowTitle("PanelBuddy Configuration")

        configWidget.setWindowFlags(self, QtCore.Qt.Window)
        self.layout = QFormLayout()

        labelFont = QFont("Arial", 12)
        titleFont = QFont("Arial", 18)

        # Title
        titleLabel = QLabel("PanelBuddy Configuration")
        titleLabel.setFont(titleFont)

        # Force x11 check box
        if sys.platform.startswith("linux"):
            self.x11CheckBox = QCheckBox("Force x11")
            self.x11CheckBox.setFont(labelFont)
            self.x11CheckBox.setChecked(self.settings["force_x11"])
            self.x11CheckBox.stateChanged.connect(self.x11Change)

        # Assets path selector
        assets_label = QLabel("Select assets directory:")
        assets_label.setFont(labelFont)
        browseButton = QPushButton("Browse assets directory")
        browseButton.setFont(labelFont)
        browseButton.clicked.connect(self.fileDialogBox) # For dialog
        
        self.assetsDirEdit = QLineEdit() # For manual changing a line
        self.assetsDirEdit.setFont(labelFont)
        self.assetsDirEdit.editingFinished.connect(self.assetsDirEditOnChange)
        self.assetsDirEdit.setText(self.settings["assets_path"])

        # Widget Placement Dropdown
        placement_label = QLabel("Window Location: ")
        placement_label.setFont(labelFont)

        self.placement_dropdown = QComboBox()
        self.placement_dropdown.setFont(labelFont)
        self.placement_dropdown.addItems(["bottom-left", "bottom-right"])
        self.placement_dropdown.currentTextChanged.connect(self.placement_dropdown_text_change)

        # Margins from edge of screen
        margins_label = QLabel("Margins (x,y):")
        margins_label.setFont(labelFont)
        self.X_marginsSpinbox = QDoubleSpinBox()
        self.Y_marginsSpinbox = QDoubleSpinBox()

        self.X_marginsSpinbox.setSingleStep(0.5)
        self.Y_marginsSpinbox.setSingleStep(0.5)
        self.X_marginsSpinbox.valueChanged.connect(self.X_spinbox_change)
        self.Y_marginsSpinbox.valueChanged.connect(self.Y_spinbox_change)
        self.X_marginsSpinbox.setFont(labelFont)
        self.Y_marginsSpinbox.setFont(labelFont)

        # Size/scale slider
        size_label = QLabel("Size: ")
        size_label.setFont(labelFont)
        self.sizeSpinbox = QDoubleSpinBox()
        self.sizeSpinbox.setSingleStep(0.1)
        self.sizeSpinbox.valueChanged.connect(self.size_slider_change)

        # Pixel art checkbox
        self.pixelArtCheckBox = QCheckBox("Pixel Art")
        self.pixelArtCheckBox.setFont(labelFont)
        self.pixelArtCheckBox.setChecked(self.settings["pixel_art"])
        self.pixelArtCheckBox.stateChanged.connect(self.pixelArtChange)


        # Adding everything into the layout
        self.layout.setVerticalSpacing(10)

        self.layout.addRow(titleLabel)
        self.layout.addItem(QSpacerItem(0, 17, QSizePolicy.Minimum, QSizePolicy.Fixed)) #Spacer

        if sys.platform.startswith("linux"): self.layout.addRow(self.x11CheckBox)
        
        self.layout.addItem(QSpacerItem(0, 13, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.layout.addRow(size_label, self.sizeSpinbox)

        self.layout.addItem(QSpacerItem(0, 13, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.layout.addRow(assets_label)
        self.layout.addRow(self.assetsDirEdit, browseButton)

        self.layout.addItem(QSpacerItem(0, 13, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.layout.addRow(placement_label, self.placement_dropdown)

        self.layout.addItem(QSpacerItem(0, 13, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.layout.addRow(margins_label)
        self.layout.addRow(self.X_marginsSpinbox, self.Y_marginsSpinbox)
        
        self.layout.addItem(QSpacerItem(0, 13, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.layout.addRow(self.pixelArtCheckBox)


        self.setLayout(self.layout)

    def size_slider_change(self, value):
        self.settings["size"] = value
        self.save()

    def pixelArtChange(self):
        self.settings["pixel_art"] = self.pixelArtCheckBox.isChecked()
        self.save()

    def X_spinbox_change(self, value):
        self.settings["margins"][0]=value
        self.save()
    
    def Y_spinbox_change(self, value):
        self.settings["margins"][1]=value
        self.save()

    def placement_dropdown_text_change(self, text):
        self.settings["widget_placement"] = str(text)
        self.save()

    def fileDialogBox(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a directory")
        if dir_name:
            path = Path(dir_name)
            self.assetsDirEdit.setText(str(path))
            self.assetsDirEditOnChange()     

    def assetsDirEditOnChange(self):
        self.settings["assets_path"] = self.assetsDirEdit.text()
        self.save()

    def x11Change(self):
        self.settings["force_x11"] = self.x11CheckBox.isChecked()
        self.save()

    def save(self):
        with open("config.json", "w") as f:
            json.dump(self.settings, f, indent=4)
            f.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = configWidget()

    #widget.setFixedSize(350, 500) # Fix dis

    sys.exit(app.exec())