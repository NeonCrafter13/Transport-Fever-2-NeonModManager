# Entrypoint to the Aplication
import configparser
import os,sys, subprocess
import mod_finder, modlist

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QAction, QGridLayout, QScrollArea, QLabel
from PyQt5.QtGui import QIcon, QPixmap

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])

Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
app = QApplication(sys.argv)

class RPanal(QWidget):
    def __init__(self, Mod, id):
        super().__init__()
        self.id = id
        self.Mod = Mod
        self.initMe()

    def initMe(self):
        Mod = self.Mod
        Layout = QVBoxLayout()

        #Name
        Layout.addWidget(QLabel(str(Mod.name)))

        # Image
        if Mod.image:
            Image = QLabel()
            pixmap = QPixmap(Mod.image)
            pixmap = pixmap.scaledToWidth(256)
            Image.setPixmap(pixmap)
            Layout.addWidget(Image)
        else:
            Image = QLabel()
            pixmap = QPixmap("images/no_image.png")
            pixmap = pixmap.scaledToWidth(256)
            Image.setPixmap(pixmap)
            Layout.addWidget(Image)

        #Authors
        separator = ', '
        if Mod.authors:
            Layout.addWidget(QLabel(f"Authors: {separator.join(Mod.authors)}"))
        else:
            Layout.addWidget(QLabel(f"Authors: not detected"))

        # source
        Layout.addWidget(QLabel(f"source: {str(Mod.source)}"))

        # minorVersion
        Layout.addWidget(QLabel(f"minorVersion: {str(Mod.minorVersion)}"))

        # hasSettings
        Layout.addWidget(QLabel(f"hasOptions: {str(Mod.options)}"))

        # Open in Explorer Button
        Open = QPushButton("Open in Expolorer")
        Open.clicked.connect(self.open)
        Layout.addWidget(Open)

        # Uninstall
        Uninstall = QPushButton("Uninstall Mod")
        Uninstall.clicked.connect(self.uninstall)
        Layout.addWidget(Uninstall)

        self.setLayout(Layout)

    def open(self):
        subprocess.Popen(r'explorer /open,"'+ self.Mod.location +'"')

    def uninstall(self):
        if not self.Mod.uninstall():
            print("ERROR")
class ModBox(QWidget):
    def __init__(self, Mod, id):
        super().__init__()
        self.id = id
        self.initMe(Mod)

    def initMe(self, Mod):
        Layout = QHBoxLayout()
        Layout.addWidget(QLabel(Mod.name))
        Layout.addWidget(QLabel(str(Mod.minorVersion)))
        authorString = ""
        if Mod.authors == None:
            Layout.addWidget(QLabel(Mod.authors))
        else:
            for author in Mod.authors:
                authorString = authorString + author + ", "
            Layout.addWidget(QLabel(authorString))
        self.setLayout(Layout)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout()
        # mod_window = QGridLayout()

        scroll = QScrollArea()
        self.h.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollcontent = QWidget(scroll)


        mod_layout =  QVBoxLayout()
        scrollcontent.setLayout(mod_layout)

        i = -1
        for mod in Mods:
            i = i + 1
            a = ModBox(mod, i)
            a.mouseReleaseEvent = lambda event, a=a: self.update_RPanal(event, a)
            mod_layout.addWidget(a)

        scroll.setWidget(scrollcontent)

        self.mod_info = RPanal(Mods[0],0)
        self.h.addWidget(self.mod_info)
        self.mod_info.show()
        self.setLayout(self.h)
        self.show()

    def update_RPanal(self, event, a):
        self.mod_info.setParent(None)
        self.mod_info.pixmap = None
        self.mod_info = RPanal(Mods[a.id], a.id)
        self.h.addWidget(self.mod_info)
        self.mod_info.show()

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
