# Entrypoint to the Aplication
import configparser
import os,sys, subprocess
import mod_finder, modlist, search
from mod import Mod
from os.path import expanduser

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMainWindow, QAction, QGridLayout, QScrollArea, QLabel, QFileDialog, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)


class ErrorBox(QMessageBox):
    def __init__(self,error: str):
        super().__init__()
        self.setStyleSheet(style)
        self.setIcon(QMessageBox.Critical)
        self.setText(error)
        self.setStandardButtons(QMessageBox.Close)
        self.setWindowTitle("ERROR")
        self.show()


config = configparser.ConfigParser()
config.read("settings.ini")

try:
    Width = int(config["GRAPHICS"]["imagesize"])
except:
    Width = 384
try:
    style = config["GRAPHICS"]["imagesize"]
    if style:
        with open("Aqua.qss", "r") as style:
            style = style.read()
    else:
        style = ""
except:
    style = ""

try:
    externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
    steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])
    userdataModsDirectory = os.path.normpath(config["DIRECTORY"]["userdatamods"])
    stagingAreamodsDirectory = os.path.normpath(config["DIRECTORY"]["stagingareamods"])
    sevenzip = os.path.normpath(config["DIRECTORY"]["7-zipInstallation"])
    import modinstaller

    global Mods

    if os.path.isdir(externalModsDirectory) and os.path.isdir(steamModsDirectory) and os.path.isdir(userdataModsDirectory) and os.path.isdir(stagingAreamodsDirectory):
        Mods = mod_finder.getAllMods(externalModsDirectory, steamModsDirectory, userdataModsDirectory, stagingAreamodsDirectory)
    else:
        e = ErrorBox("Mod-Directories are incorrect")
    if not os.path.isdir(sevenzip):
        e = ErrorBox("Sevenzip Path incorrect")
    configfound = True
except:
    error = ErrorBox("Could not find settings.ini")
    configfound = False

class CompareMods(QWidget):
    def __init__(self, list):
        super().__init__()
        self.list = list
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Compare Mods")
        self.setStyleSheet(style)
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout()
        scroll = QScrollArea()
        self.h.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollcontent = QWidget(scroll)

        scroll.setWidget(scrollcontent)

        TV = QVBoxLayout()
        scrollcontent.setLayout(TV)

        self.NotInstalledV = QVBoxLayout()
        self.InstalledV = QVBoxLayout()
        self.unusedV = QVBoxLayout()

        NotInstalledLabel = QLabel("Not installed Mods:")
        NotInstalledLabel.setStyleSheet("color: red; background-color: #a0a0a0;")
        TV.addWidget(NotInstalledLabel)

        TV.addLayout(self.NotInstalledV)

        InstalledLabel = QLabel("Installed Mods:")
        InstalledLabel.setStyleSheet("color: green; background-color: #a0a0a0;")
        TV.addWidget(InstalledLabel)

        TV.addLayout(self.InstalledV)

        UnusedLabel = QLabel("Installed Mods that aren´t one the list:")
        UnusedLabel.setStyleSheet("color: #ff6f00; background-color: #a0a0a0;")
        TV.addWidget(UnusedLabel)

        TV.addLayout(self.unusedV)

        self.setLayout(self.h)
        self.ListMods()
        self.show()

    def ListMods(self):
        self.onList = []
        for item in self.list:
            result = search.find_mod_compare(Mods, item["name"])
            if result:
                self.InstalledV.addWidget(ModBox(*result))
                self.onList.append(result[1])
            else:
                #Create Mod Instance
                mod = Mod(item["name"], None, item["source"], False, False, False, item["authors"])
                self.NotInstalledV.addWidget(ModBox(mod, None))

        for i in range(len(Mods)):
            if not i in self.onList:
                self.unusedV.addWidget(ModBox(Mods[i],i))

class InstallModWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setGeometry(50,50,500,500)
        self.setWindowTitle("Mod Installer")
        self.setStyleSheet(style)
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
                self.error = ErrorBox("New Installed Mod will only be shown after restart")
        else:
            event.ignore()

    def openFile(self):
        fd = QFileDialog()
        f_dir =fd.getOpenFileName(
            self,
            "Install Mod",
            expanduser("~"),
            "(*.rar *.zip *.7z)"
            )

        if f_dir[0] != "":
            modinstaller.install(f_dir[0])
            self.error = ErrorBox("New Installed Mod will only be shown after restart")


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
            self.error = ErrorBox("New Installed Mod will only be shown after restart")


            self.setParent = None

class RPanal(QWidget):
    def __init__(self, Mod):
        super().__init__()
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
            self.error = ErrorBox("Uninstalled Mods will be listed if Programm is not restarted")

class ModBox(QWidget):
    def __init__(self, Mod, id):
        super().__init__()
        self.id = id
        self.initMe(Mod)

    def initMe(self, Mod):
        Layout = QHBoxLayout()
        Layout.addWidget(QLabel(Mod.name))
        Layout.addWidget(QLabel(str(Mod.minorVersion)))
        Layout.addWidget(QLabel(Mod.source))
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

        self.parent.update_RPanal_With_Search(keyword)


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
        self.scrollcontent = QListWidget(scroll)

        for mod in Mods:
            a = QListWidgetItem(mod.name)
            a.mod = mod
            self.scrollcontent.addItem(a)

        scroll.setWidget(self.scrollcontent)

        self.scrollcontent.itemSelectionChanged.connect(self.update_RPanal)

        self.mod_info = RPanal(Mods[0])
        self.h.addWidget(self.mod_info)
        self.mod_info.show()

        searchbox = SearchBox(self)
        self.v.addWidget(searchbox)
        searchbox.show()

        self.v.addLayout(self.h)
        self.setLayout(self.v)
        # self.show()

    def update_RPanal(self):
        self.mod_info.setParent(None)
        self.mod_info.pixmap = None
        items = self.scrollcontent.selectedItems()
        if not items: return
        item = items[0]
        self.mod_info = RPanal(item.mod)
        self.h.addWidget(self.mod_info)
        self.mod_info.show()

    def update_RPanal_With_Search(self, keyword):
        items = self.scrollcontent.findItems(keyword, Qt.MatchContains)
        if not items:
            self.error = ErrorBox("No Mod found with matching name")
        else:
            item = items[0]
            item.setSelected(True)
            self.scrollcontent.scrollToItem(item, QAbstractItemView.PositionAtTop)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(style)
        self.initMe()

    def initMe(self):

        ExportModlist = QAction("export modlist",self)
        ExportModlist.setShortcut("Ctrl+E")
        ExportModlist.setStatusTip("export modlist")
        ExportModlist.triggered.connect(self.export_modlist)

        ImportModlist = QAction("Compare modlist",self)
        ImportModlist.setShortcut("Ctrl+O")
        ImportModlist.setStatusTip("Compare modlist")
        ImportModlist.triggered.connect(self.compare_modlist)

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

    def compare_modlist(self):
        list = modlist.import_modlist(Mods)
        if list:
            self.compare = CompareMods(list)
        else:
            self.error = ErrorBox("Couldn´t find the Modlist")

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


if configfound:
    if os.path.isdir(externalModsDirectory) and os.path.isdir(steamModsDirectory) and os.path.isdir(userdataModsDirectory) and os.path.isdir(stagingAreamodsDirectory):
        w = Window()

sys.exit(app.exec_())
