# Entrypoint to the Aplication
import configparser
import os,sys, subprocess
import mod_finder, modlist, modinstaller, search
from os.path import expanduser

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QAction, QGridLayout, QScrollArea, QLabel, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])

app = QApplication(sys.argv)

class ErrorBox(QMessageBox):
    def __init__(self,error: str):
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setText(error)
        self.setStandardButtons(QMessageBox.Close)
        self.setWindowTitle("ERROR")
        self.show()


global Mods

if os.path.isdir(externalModsDirectory) and os.path.isdir(steamModsDirectory):
    Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
else:
    e = ErrorBox("Mod-Directories are incorrect")

class InstallModWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setGeometry(50,50,500,500)
        self.setWindowTitle("Mod Installer")
        self.initMe()

    def initMe(self):
        Layout = QVBoxLayout()

        Layout.addWidget(QLabel("Drop your Mod in here"))

        btn1 = QPushButton("Select a file here")
        btn1.clicked.connect(self.openFile)
        Layout.addWidget(btn1)

        btn2 = QPushButton("Select a folder here")
        btn2.clicked.connect(self.openFolder)
        Layout.addWidget(btn2)

        self.setLayout(Layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(os.path.normpath(url.toLocalFile()))
            a = False
            for link in links:
                modinstaller.install(link)
                a = True

            if a:
                global Mods
                Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
                w.reload()
                self.setParent = None
        else:
            event.ignore()

    def openFile(self):
        fd = QFileDialog()
        f_dir =fd.getOpenFileName(
            self,
            "Install Mod",
            expanduser("~"),
            "(*.rar,*.zip)"
            )

        if f_dir[0] != "":
            modinstaller.install(f_dir[0])
            global Mods
            Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
            w.reload()

            self.setParent = None

    def openFolder(self):
        fd = QFileDialog()
        f_dir =fd.getExistingDirectory(
            self,
            "Install Mod",
            expanduser("~"),
            fd.ShowDirsOnly
            )

        if f_dir != "":
            modinstaller.install(f_dir)
            global Mods
            Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
            w.reload()

            self.setParent = None

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

        Width = 384

        # Image
        if Mod.image:
            Image = QLabel()
            pixmap = QPixmap(Mod.image)
            pixmap = pixmap.scaledToWidth(Width)
            Image.setPixmap(pixmap)
            Layout.addWidget(Image)
        else:
            Image = QLabel()
            pixmap = QPixmap("images/no_image.png")
            pixmap = pixmap.scaledToWidth(Width)
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
            self.error = ErrorBox("Mod couldn´t be uninstalled")
        else:
            global Mods
            Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)
            w.reload()

class ModBox(QWidget):
    def __init__(self, Mod, id):
        super().__init__()
        self.id = id
        self.initMe(Mod)

    def initMe(self, Mod):
        Layout = QHBoxLayout()
        Layout.addWidget(QLabel(Mod.name))
        Layout.addWidget(QLabel(str(Mod.minorVersion)))
        """
        authorString = ""
        if Mod.authors == None:
            Layout.addWidget(QLabel(Mod.authors))
        else:
            for author in Mod.authors:
                authorString = authorString + author + ", "
            Layout.addWidget(QLabel(authorString))
        """
        self.setLayout(Layout)

class SearchBox(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout()
        self.textbox = QLineEdit()

        self.h.addWidget(self.textbox)

        self.button = QPushButton('Search')
        self.h.addWidget(self.button)
        self.button.clicked.connect(self.search)

        self.setLayout(self.h)



    def search(self):
        keyword = self.textbox.text()

        result = search.find_mod(Mods, keyword)

        if result:
            self.parent.update_RPanal_With_Search(*result)
        else:
            self.error = ErrorBox("Could not find a Mod with matching name!")

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.v = QVBoxLayout()
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

        searchbox = SearchBox(self)
        self.v.addWidget(searchbox)
        searchbox.show()

        self.v.addLayout(self.h)
        self.setLayout(self.v)
        # self.show()

    def update_RPanal(self, event, a):
        self.mod_info.setParent(None)
        self.mod_info.pixmap = None
        self.mod_info = RPanal(Mods[a.id], a.id)
        self.h.addWidget(self.mod_info)
        self.mod_info.show()

    def update_RPanal_With_Search(self, Mod, id):
        self.mod_info.setParent(None)
        self.mod_info.pixmap = None
        self.mod_info = RPanal(Mod, id)
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
        mod = menubar.addMenu("Mod")
        mod.addAction(ExportModlist)
        mod.addAction(ImportModlist)
        mod.addAction(InstallMod)

        steamMods = QAction("Set Steammods location", self)
        steamMods.setStatusTip("Set Steammods location")
        steamMods.triggered.connect(self.setSteamMods)

        externalMods = QAction("Set externalmods location", self)
        externalMods.setStatusTip("Set externalmods location")
        externalMods.triggered.connect(self.setExternalMods)

        settings = menubar.addMenu("Settings")
        settings.addAction(steamMods)
        settings.addAction(externalMods)

        self.setGeometry(50,50,500,500)
        self.setWindowTitle("Tpf2 NeonModManager")

        self.setWindowIcon(QIcon("images/icon.png"))

        self.mainwidget = MainWidget()
        self.setCentralWidget(self.mainwidget)

        self.show()

    def export_modlist(self):
        modlist.export_modlist(Mods)

    def import_modlist(self):
        modlist.import_modlist(Mods)

    def install_mod(self):
        self.installPopup = InstallModWindow()
        self.installPopup.show()

    def setSteamMods(self):
        fd = QFileDialog()
        f_dir =fd.getExistingDirectory(
            self,
            "Open steammods folder",
            expanduser("~"),
            fd.ShowDirsOnly
            )

        if f_dir != "":
            config.set('DIRECTORY', 'steamMods', f_dir)
            # Writing our configuration file to 'example.ini'
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)

    def setExternalMods(self):
        fd = QFileDialog()
        f_dir =fd.getExistingDirectory(
            self,
            "Open externalmods folder",
            expanduser("~"),
            fd.ShowDirsOnly
            )

        if f_dir != "":
            config.set('DIRECTORY', 'externalMods', f_dir)
            # Writing our configuration file to 'example.ini'
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)

    def reload(self):
        self.mainwidget.setParent = None
        self.mainwidget = MainWidget()
        self.setCentralWidget = self.mainwidget

if os.path.isdir(externalModsDirectory) and os.path.isdir(steamModsDirectory):
    w = Window()

sys.exit(app.exec_())
