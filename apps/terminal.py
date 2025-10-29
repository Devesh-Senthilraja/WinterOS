from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
import subprocess

from .common import apply_style, create_button

class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        controls = QGridLayout()
        layout.addLayout(controls, 0, 0)

        address_label = QLabel("ProximaOS:~", self)
        address_label.setStyleSheet("font: bold 15px 'Arial';")
        controls.addWidget(address_label, 0, 0)

        self.commandLine = QLineEdit(self)
        apply_style(self.commandLine, font_size=15)
        self.commandLine.setFixedSize(900, 50)
        controls.addWidget(self.commandLine, 0, 1)

        runButton = create_button("Run", slot=self.runCommand, size=(100, 50), parent=self)
        controls.addWidget(runButton, 0, 2)

        viewer = QTextEdit(self)
        apply_style(viewer, font_size=15)
        viewer.setFixedSize(1105, 645)
        layout.addWidget(viewer, 1, 0)

        self.commandOutput = viewer

    def runCommand(self):
        command = self.commandLine.text()
        self.commandLine.clear()

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.commandOutput.append("ProximaOS:~ " + command)

        cmdResults, cmdErrors = process.communicate()
        if cmdResults:
            self.commandOutput.append(cmdResults.decode())
        if cmdErrors:
            self.commandOutput.append(cmdErrors.decode())