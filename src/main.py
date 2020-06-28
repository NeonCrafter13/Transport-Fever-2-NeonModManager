# Entrypoint to the Aplication
import configparser
import os,sys
import mod_finder, modlist

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QAction
from PyQt5.QtGui import QIcon

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])

Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
app = QApplication(sys.argv)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):

        ExportModlist = QAction("export modlist",self)
        ExportModlist.setShortcut("Ctrl+E")
        ExportModlist.setStatusTip("export modlist")
        ExportModlist.triggered.connect(self.export_modlist)

        ImportModlist = QAction("import modlist",self)
        ImportModlist.setShortcut("Ctrl+O")
        ImportModlist.setStatusTip("import modlist")
        ImportModlist.triggered.connect(self.import_modlist)

        InstallMod = QAction("install mod", self)
        InstallMod.setShortcut("Ctrl+I")
        InstallMod.setStatusTip("install mod")
        InstallMod.triggered.connect(self.install_mod)

        menubar = self.menuBar()
        file = menubar.addMenu("File")
        file.addAction(ExportModlist)
        file.addAction(ImportModlist)
        file.addAction(InstallMod)

        self.setGeometry(50,50,500,500)
        self.setWindowTitle("Tpf2 NeonModManager")
        # w.setWindowIcon(QIcon("test.png"))
        self.show()

    def export_modlist(self):
        modlist.export_modlist(Mods)

    def import_modlist(self):
        modlist.import_modlist(Mods)

    def install_mod(self):
        print("install mod")

w = Window()

sys.exit(app.exec_())
