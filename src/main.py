# Entrypoint to the Aplication
import configparser
import os,sys
import mod_finder

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtGui import QIcon

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])

Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
app = QApplication(sys.argv)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.setGeometry(50,50,500,500)
        self.setWindowTitle("Tpf2 NeonModManager")
        # w.setWindowIcon(QIcon("test.png"))
        self.show()



w = Window()

sys.exit(app.exec_())
