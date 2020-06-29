# Entrypoint to the Aplication
import configparser
import os,sys, subprocess
import mod_finder, modlist

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QAction, QGridLayout, QScrollArea, QLabel
from PyQt5.QtGui import QIcon

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])

Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
app = QApplication(sys.argv)

class ModBox(QWidget):
    def __init__(self, Mod):
        super().__init__()
        self.initMe(Mod)

    def initMe(self, Mod):
        Layout = QHBoxLayout()
        Layout.addWidget(QLabel(Mod.name))
        Layout.addWidget(QLabel(str(Mod.minorVersion)))
        Layout.addWidget(QLabel(Mod.authors))
        self.setLayout(Layout)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        h = QHBoxLayout()
        # mod_window = QGridLayout()

        scroll = QScrollArea()
        h.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollcontent = QWidget(scroll)


        mod_layout =  QVBoxLayout()
        scrollcontent.setLayout(mod_layout)

        i = 0
        for mod in Mods:
            a = ModBox(mod)
            mod_layout.addWidget(a)
            a.show()

        scroll.setWidget(scrollcontent)

        # h.addLayout(mod_box)
        B2 = QPushButton("2")
        B2.clicked.connect(self.test)
        h.addWidget(B2)
        self.setLayout(h)
        self.show()
    def test(self):
        subprocess.Popen(r'explorer /open,"'+ externalModsDirectory +'"')

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

        mainwidget = MainWidget()
        self.setCentralWidget(mainwidget)

        self.show()

    def export_modlist(self):
        modlist.export_modlist(Mods)

    def import_modlist(self):
        modlist.import_modlist(Mods)

    def install_mod(self):
        print("install mod")

w = Window()

sys.exit(app.exec_())
