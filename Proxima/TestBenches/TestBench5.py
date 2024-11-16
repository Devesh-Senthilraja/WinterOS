import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTextEdit, QLineEdit, QPushButton, QLabel

class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parentFrame = parent
        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)

        # Controls frame
        controls = QGridLayout()
        layout.addLayout(controls, 0, 0)

        address_label = QLabel("WinterOS:~", self)
        address_label.setStyleSheet("font: bold 15px 'Arial';")
        controls.addWidget(address_label, 0, 0)

        self.commandLine = QLineEdit(self)
        self.commandLine.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        self.commandLine.setFixedSize(900, 50)
        controls.addWidget(self.commandLine, 0, 1)

        runButton = QPushButton("Run", self)
        runButton.setStyleSheet("background-color: #d9d9d9; font: bold 20px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        runButton.setFixedSize(100, 50)
        runButton.clicked.connect(self.runCommand)
        controls.addWidget(runButton, 0, 2)

        # Viewer frame
        viewer = QTextEdit(self)
        viewer.setStyleSheet("background-color: #f0f0f0; font: bold 15px 'Arial'; border: 1px solid lightgrey; border-radius: 10px;")
        viewer.setFixedSize(1105, 635)
        layout.addWidget(viewer, 1, 0)

        self.commandOutput = viewer

    def runCommand(self):
        command = self.commandLine.text()
        self.commandLine.clear()

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.commandOutput.append("WinterOS:~ " + command)

        cmdResults, cmdErrors = process.communicate()
        self.commandOutput.append(cmdResults.decode())
        self.commandOutput.append(cmdErrors.decode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Terminal()
    win.show()
    sys.exit(app.exec_())
