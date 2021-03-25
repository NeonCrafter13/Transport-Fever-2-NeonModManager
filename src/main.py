#! /usr/bin/env python3

# Entrypoint to the Application
import configparser
import os
import shutil
import sys
import subprocess
import mod_finder
import modlist
import search
import images
from mod import Mod
from os.path import expanduser
from freezeutils import find_data_file as f

from PyQt5.QtWidgets import (
    QStatusBar, QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QMainWindow,
    QAction,
    QGridLayout,
    QScrollArea,
    QLabel,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QObject, Qt, pyqtSignal

app = QApplication(sys.argv)

if False:  # Change this to True if you are building the .deb file.
    os.chdir("/usr/share/Tpf2NeonModManager")

setting_up = False
configfound = False

if not os.path.isfile(f("settings.ini")):
    import setup

    setup = setup.Setup_Window()
    setting_up = True


class ErrorBox(QMessageBox):
    def __init__(self, error: str):
        super().__init__()
        self.setStyleSheet(style)
        self.setIcon(QMessageBox.Critical)
        self.setText(error)
        self.setStandardButtons(QMessageBox.Close)
        self.setWindowTitle("ERROR")
        self.show()


class Signals(QObject):
    status_bar_message = pyqtSignal(str)


sig = Signals()

if not setting_up:
    config = configparser.ConfigParser()
    a = config.read(os.path.abspath(f("settings.ini")))

    try:
        Width = int(config["GRAPHICS"]["imagesize"])
    except KeyError:
        Width = 384
    try:
        style = config["GRAPHICS"]["modernstyle"]
        if style.lower().replace(" ", "") == "true":
            with open(f("Aqua.css"), "r") as style:
                style = style.read()
        else:
            style = ""
    except KeyError:
        style = ""

    try:
        externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
        steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])
        userdataModsDirectory = os.path.normpath(config["DIRECTORY"]["userdatamods"])
        stagingAreaModsDirectory = os.path.normpath(config["DIRECTORY"]["stagingareamods"])
        sevenZip = os.path.normpath(config["DIRECTORY"]["7-zipInstallation"])
        import modinstaller

        global mods

        language = config["LANGUAGE"]["language"]

        if os.path.isdir(externalModsDirectory) and os.path.isdir(steamModsDirectory) and os.path.isdir(
                userdataModsDirectory) and os.path.isdir(stagingAreaModsDirectory):
            mods = mod_finder.getAllMods(
                externalModsDirectory, steamModsDirectory, userdataModsDirectory, stagingAreaModsDirectory, language)
        else:
            os.remove(f('settings.ini'))
            e = ErrorBox("Mod-Directories are incorrect")
        if sys.platform == "win32":
            if not os.path.isdir(sevenZip):
                os.remove(f('settings.ini'))
                e = ErrorBox("The configured 7-zip path is invalid.")
        elif sys.platform in ("linux", "darwin"):
            if shutil.which('7z') is None:
                e = ErrorBox("7-zip is not installed.")
        configfound = True
    except:
        error = ErrorBox("Could not find settings.ini")
        configfound = False
        import setup

        setup = setup.Setup_Window()
        setting_up = True


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

        UnusedLabel = QLabel("Installed Mods that aren't on the list:")
        UnusedLabel.setStyleSheet("color: #ff6f00; background-color: #a0a0a0;")
        TV.addWidget(UnusedLabel)

        TV.addLayout(self.unusedV)

        self.setLayout(self.h)
        self.ListMods()
        self.show()

    def ListMods(self):
        self.onList = []
        for item in self.list:
            result = search.find_mod_compare(mods, item["name"])
            if result:
                self.InstalledV.addWidget(ModBox(*result))
                self.onList.append(result[1])
            else:
                # Create Mod Instance
                mod = Mod(item["name"], None, item["source"], False,
                          False, False, item["authors"], None)
                self.NotInstalledV.addWidget(ModBox(mod, None))

        for i in range(len(mods)):
            if i not in self.onList:
                self.unusedV.addWidget(ModBox(mods[i], i))


class InstallModWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setGeometry(50, 50, 500, 500)
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
                sig.status_bar_message.emit("Installing Mod")
                modinstaller.install(link)
                a = True

            if a:
                sig.status_bar_message.emit(
                    "New Installed Mod will only be shown after restart")
        else:
            event.ignore()
        self.close()

    def openFile(self):
        fd = QFileDialog()
        f_dir = fd.getOpenFileName(
            self,
            "Install Mod",
            expanduser("~"),
            "(*.rar *.zip *.7z)"
        )

        if f_dir[0] != "":
            sig.status_bar_message.emit("Installing Mod")
            modinstaller.install(f_dir[0])
            sig.status_bar_message.emit(
                "New Installed Mod will only be shown after restart")
        self.close()

    def openFolder(self):
        fd = QFileDialog()
        f_dir = fd.getExistingDirectory(
            self,
            "Install Mod",
            expanduser("~"),
            fd.ShowDirsOnly
        )

        if f_dir != "":
            sig.status_bar_message.emit("Installing Mod")
            modinstaller.install(f_dir)
            sig.status_bar_message.emit(
                "New Installed Mod will only be shown after restart")
        self.close()


class RPanel(QWidget):
    def __init__(self, mod):
        super().__init__()
        self.mod: Mod = mod
        self.initMe()

    def initMe(self):
        mod = self.mod
        Layout = QVBoxLayout()

        # Name
        Layout.addWidget(QLabel(str(mod.name)))

        # Image
        Image = QLabel()

        if mod.image:
            pixmap = QPixmap(mod.image)
        else:
            pixmap = QPixmap(f("images/no_image.png"))

        pixmap = pixmap.scaledToWidth(Width, mode=Qt.SmoothTransformation)
        Image.setPixmap(pixmap)
        Layout.addWidget(Image)

        # Authors
        separator = ', '
        if mod.authors:
            Layout.addWidget(QLabel(f"Authors: {separator.join(mod.authors)}"))
        else:
            Layout.addWidget(QLabel("Authors: not detected"))

        # source
        Layout.addWidget(QLabel(f"source: {str(mod.source)}"))

        # minorVersion
        Layout.addWidget(QLabel(f"minorVersion: {str(mod.minorVersion)}"))

        # hasSettings
        Layout.addWidget(QLabel(f"hasOptions: {str(mod.options)}"))

        # Category Image
        if mod.category_image is not None:
            try:
                images.invert_image(mod.category_image)
                success = True
            except:
                success = False
            if success:
                Image = QLabel()
                pixmap = QPixmap(f("Image_negative.jpg"))
                Image.setPixmap(pixmap)
                Image.setToolTip("Category")
                Layout.addWidget(Image)

        # Open in Explorer Button
        Open = QPushButton("Open in Explorer")
        Open.clicked.connect(self.open)
        Layout.addWidget(Open)

        # Uninstall
        Uninstall = QPushButton("Uninstall Mod")
        Uninstall.clicked.connect(self.uninstall)
        Layout.addWidget(Uninstall)

        self.setLayout(Layout)

    def open(self):
        if sys.platform == "linux":
            commands = ["xdg-open", "gnome-open", "nautilus"]
            fail = True
            for i in commands:
                try:
                    subprocess.Popen([i, self.mod.location])
                    fail = False
                    break
                except FileNotFoundError as e:
                    continue
            if fail is True:
                self.e = ErrorBox("Your file explorer is at the moment not supported!")
        elif sys.platform == "win32":
            subprocess.Popen(r'explorer /open,"' + self.mod.location + '"')
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', self.mod.location])

    def uninstall(self):
        if not self.mod.uninstall():
            self.error = ErrorBox("Mod couldn't be uninstalled")
        else:
            self.error = ErrorBox("Uninstalled Mods will be listed if Program is not restarted")


class ModBox(QWidget):
    def __init__(self, mod, id):
        super().__init__()
        self.id = id
        self.initMe(mod)

    def initMe(self, mod):
        Layout = QHBoxLayout()
        Layout.addWidget(QLabel(mod.name))
        Layout.addWidget(QLabel(str(mod.minorVersion)))
        Layout.addWidget(QLabel(mod.source))
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

        for mod in mods:
            a = QListWidgetItem(mod.name)
            a.mod = mod
            self.scrollcontent.addItem(a)

        scroll.setWidget(self.scrollcontent)

        self.scrollcontent.itemSelectionChanged.connect(self.update_RPanel)

        self.mod_info = RPanel(mods[0])
        self.h.addWidget(self.mod_info)
        self.mod_info.show()

        searchbox = SearchBox(self)
        self.v.addWidget(searchbox)
        searchbox.show()

        self.v.addLayout(self.h)
        self.setLayout(self.v)
        # self.show()

    def update_RPanel(self):
        self.mod_info.setParent(None)
        self.mod_info.pixmap = None
        items = self.scrollcontent.selectedItems()
        if not items:
            return
        item = items[0]
        self.mod_info = RPanel(item.mod)
        self.h.addWidget(self.mod_info)
        self.mod_info.show()

    def update_RPanel_With_Search(self, keyword):
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
        sig.status_bar_message.connect(self.set_status_bar_info)
        self.initMe()

    def initMe(self):

        self.state = QStatusBar(self)  # Create Statusbar

        self.setStatusBar(self.state)

        ExportModlist = QAction("export modlist", self)
        ExportModlist.setShortcut("Ctrl+E")
        ExportModlist.setStatusTip("export modlist")
        ExportModlist.triggered.connect(self.export_modlist)

        ImportModlist = QAction("Compare modlist", self)
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

        open_settings = QAction("Open Settings", self)
        open_settings.setStatusTip("Open Settings")
        open_settings.triggered.connect(self.open_Settings)

        settings = menubar.addMenu("Settings")
        settings.addAction(open_settings)

        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Tpf2 NeonModManager")

        self.setWindowIcon(QIcon(f("images/icon.png")))

        self.mainwidget = MainWidget()
        self.setCentralWidget(self.mainwidget)

        self.show()

    def set_status_bar_info(self, e):  # Set text of the statusbar
        self.state.showMessage(e)

    def export_modlist(self):

        sig.status_bar_message.emit("Choosing folder for modlist.csv")

        fd = QFileDialog()
        f_dir = fd.getExistingDirectory(
            self,
            "Chose Folder for modlist.csv",
            expanduser("~"),
            fd.ShowDirsOnly
        )
        if f_dir == "":
            return

        sig.status_bar_message.emit("Exporting modlist")
        modlist.export_modlist(mods, f_dir)
        sig.status_bar_message.emit("Modlist exported")

    def compare_modlist(self):

        sig.status_bar_message.emit("Chose your modlist.csv")

        fd = QFileDialog()
        f_dir = fd.getOpenFileName(
            self,
            "Chose your modlist.csv",
            expanduser("~"),
            "csv (*.csv)"
        )
        if f_dir[0] == "":
            return

        sig.status_bar_message.emit("Starting import of modlist.csv")
        list = modlist.import_modlist(mods, f_dir[0])
        if list:
            self.compare = CompareMods(list)
            sig.status_bar_message.emit("modlist imported")
        else:
            self.error = ErrorBox("Couldn't find the Modlist")
            sig.status_bar_message.emit("Couldn't find the Modlist")

    def install_mod(self):
        self.installPopup = InstallModWindow()
        self.installPopup.show()

    def open_Settings(self):
        import setup
        self.settings = setup.Settings()


if configfound and (not setting_up):
    if os.path.isdir(externalModsDirectory) and os.path.isdir(steamModsDirectory) and os.path.isdir(
            userdataModsDirectory) and os.path.isdir(stagingAreaModsDirectory):
        w = Window()

sys.exit(app.exec_())
