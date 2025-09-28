import os
import sys
from os.path import expanduser
from PyQt6.QtCore import QCoreApplication, QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox
)
import configparser
from freezeutils import find_data_file as f


class Signals(QObject):
    submit = pyqtSignal()
    next_page = pyqtSignal()


sig = Signals()

config = configparser.ConfigParser()


class Install_Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.v = QVBoxLayout(self)

        self.content = QVBoxLayout()
        self.v.addLayout(self.content)

        self.continue_btn = QPushButton("Continue")
        self.continue_btn.clicked.connect(self.next_page)
        self.v.addWidget(self.continue_btn)

        self.setLayout(self.v)

    def next_page(self, *arg):
        sig.submit.emit()


class PathEntry(QWidget):
    def __init__(self, labeltext: str, tooltip: str, opentitle: str) -> None:
        super().__init__()
        self.labeltext = labeltext
        self.btntooltip = tooltip
        self.opentitle = opentitle
        self.build_gui()

    def build_gui(self):
        self.h = QHBoxLayout()
        self.label = QLabel(self.labeltext)
        self.text = QLineEdit()

        self.btn = QPushButton("⚯")
        self.btn.clicked.connect(self.setPath)

        self.text.setToolTip(self.btntooltip)
        self.btn.setToolTip(self.btntooltip)

        self.h.addWidget(self.label)
        self.h.addWidget(self.text)
        self.h.addWidget(self.btn)
        self.setLayout(self.h)

    def setPath(self, *arg):
        fd = QFileDialog()
        fd.setFileMode(fd.FileMode.Directory)
        f_dir = fd.getExistingDirectory(
            self,
            self.opentitle,
            expanduser("~")
        )
        if f_dir != "":
            self.text.setText(f_dir)


class First(Install_Window):
    def __init__(self) -> None:
        super().__init__()
        self.fill_content()

    def fill_content(self):
        # Steam Mods
        self.steam = PathEntry(
            "Set Steam Mods",
            "Example: /steamapps/workshop/content/1066780",
            "Open Steam Mods Folder"
        )
        self.content.addWidget(self.steam)

        # Common Mods in settings.ini external
        self.common = PathEntry(
            "Set Common Mods",
            "Example: /steamapps/common/Transport Fever 2/mods",
            "open Common Mods Folder"
        )
        self.content.addWidget(self.common)

        # Userdata Mods
        self.userdata = PathEntry(
            "Set Userdata Mods",
            "Example: /userdata/436684792/1066780/local/mods",
            "open userdata Mods Folder"
        )
        self.content.addWidget(self.userdata)

        # Stagingarea Mods
        self.stagingarea = PathEntry(
            "Set Stagingarea",
            "Example: /userdata/436684792/1066780/local/staging_area",
            "open staging_area Folder"
        )
        self.content.addWidget(self.stagingarea)

        # 7-Zip installation
        if sys.platform == "win32":
            self.sevenzip = PathEntry(
                "Set 7-Zip Installation",
                r"Example: C:\Program Files\7-Zip",
                "open 7-zip installation folder"
            )
            self.content.addWidget(self.sevenzip)

        # Connect Signal
        sig.submit.connect(self.submit)

    def submit(self):
        config.add_section('DIRECTORY')
        config.set('DIRECTORY', 'externalmods', self.common.text.text())
        config.set('DIRECTORY', 'steammods', self.steam.text.text())
        config.set('DIRECTORY', 'userdatamods', self.userdata.text.text())
        config.set('DIRECTORY', 'stagingareamods', self.stagingarea.text.text())
        if sys.platform == "win32":
            config.set('DIRECTORY', '7-zipInstallation', self.sevenzip.text.text())
        elif sys.platform == "linux":
            config.set('DIRECTORY', '7-zipInstallation', "/usr")
        elif sys.platform == "darwin":
            config.set('DIRECTORY', '7-zipInstallation', "/usr/local/bin")

        config.add_section("GRAPHICS")
        config.set("GRAPHICS", "modernstyle", "False")
        config.set("GRAPHICS", "imagesize", "384")

        config.add_section("LANGUAGE")
        config.set("LANGUAGE", "language", "en")
        config.set("LANGUAGE", "uiLanguage", "english")

        with open(f('settings.ini'), 'w') as configfile:
            config.write(configfile)

        sig.next_page.emit()


class Second(Install_Window):
    def __init__(self) -> None:
        super().__init__()
        self.build_gui()

    def build_gui(self):
        self.content.addWidget(QLabel("Setup successful click on Continue to close the app."))
        self.content.addWidget(
            QLabel("Restart the app afterwards"))

        sig.submit.connect(self.exit)

    def exit(self):
        QCoreApplication.quit()


class Setup_Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initMe()

    def initMe(self):
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle("Tpf2 NeonModManager")

        self.setWindowIcon(QIcon("images/icon.png"))

        self.mainwidget = First()
        self.setCentralWidget(self.mainwidget)
        self.show()

        sig.next_page.connect(self.next)

    def next(self):
        self.mainwidget = Second()
        self.setCentralWidget(self.mainwidget)
        self.show()


class FormEntry(QWidget):
    def __init__(self, label: str, entry) -> None:
        super().__init__()
        self.h = QHBoxLayout(self)

        self.h.addWidget(QLabel(label))
        self.data = entry
        self.h.addWidget(self.data)

        self.setLayout(self.h)


class Settings(Install_Window):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Settings")
        self.continue_btn.setText("Apply and close")
        self.continue_btn.setToolTip("will close the application")

        config.read(f("settings.ini"))

        self.commonmodsdir = os.path.normpath(
            config['DIRECTORY']['externalMods'])
        self.steammodsdir = os.path.normpath(
            config["DIRECTORY"]["steamMods"])
        self.userdatamodsdir = os.path.normpath(
            config["DIRECTORY"]["userdatamods"])
        self.stagingareadir = os.path.normpath(
            config["DIRECTORY"]["stagingareamods"])

        self.modernstylebf = config["GRAPHICS"]["modernstyle"]
        self.imagesizebf = config["GRAPHICS"]["imagesize"]
        self.languagebf = config["LANGUAGE"]["language"]
        try:
            self.UIlanguagebf = config["LANGUAGE"]["uiLanguage"]
        except KeyError:
            self.UIlanguage = "english"


        self.continue_btn.setToolTip("will close the app you will need to restart it")
        self.fill_content()

    def fill_content(self):
        # Steam Mods
        self.steam = PathEntry(
            "Set Steam Mods",
            "Example: /steamapps/workshop/content/1066780",
            "Open Steam Mods Folder"
        )
        self.steam.text.setText(self.steammodsdir)
        self.content.addWidget(self.steam)

        # Common Mods in settings.ini external
        self.common = PathEntry(
            "Set Common Mods",
            "Example: /steamapps/common/Transport Fever 2/mods",
            "open Common Mods Folder"
        )
        self.common.text.setText(self.commonmodsdir)
        self.content.addWidget(self.common)

        # Userdata Mods
        self.userdata = PathEntry(
            "Set Userdata Mods",
            "Example: /userdata/436684792/1066780/local/mods",
            "open userdata Mods Folder"
        )
        self.userdata.text.setText(self.userdatamodsdir)
        self.content.addWidget(self.userdata)

        # Stagingarea Mods
        self.stagingarea = PathEntry(
            "Set Stagingarea",
            "Example: /userdata/436684792/1066780/local/staging_area",
            "open staging_area Folder"
        )
        self.stagingarea.text.setText(self.stagingareadir)
        self.content.addWidget(self.stagingarea)

        UIlanguage_combo = QComboBox()
        UIlanguage_combo.addItem("English", "english")
        UIlanguage_combo.addItem("Deutsch", "german")
        self.UIlanguage = FormEntry("UI language", UIlanguage_combo)
        self.UIlanguage.data.setCurrentIndex(
            self.UIlanguage.data.findData(self.UIlanguagebf))
        self.content.addWidget(self.UIlanguage)

        self.language = FormEntry("Mod Name language", QLineEdit())
        self.language.data.setText(self.languagebf)
        self.content.addWidget(self.language)

        self.modernstyle = FormEntry("modernstyle", QCheckBox())
        t = QCheckBox()
        if self.modernstylebf == "True":
            self.modernstyle.data.setChecked(True)
        elif self.modernstylebf == "False":
            self.modernstyle.data.setChecked(False)
        self.content.addWidget(self.modernstyle)

        self.imagesize = FormEntry("imagesize", QLineEdit())
        self.imagesize.data.setValidator(QIntValidator())
        self.imagesize.data.setText(self.imagesizebf.replace(" ", ""))
        self.content.addWidget(self.imagesize)

        # Connect Signal
        sig.submit.connect(self.submit)

        self.show()

    def submit(self, *arg):
        config.set('DIRECTORY', 'externalmods', self.common.text.text())
        config.set('DIRECTORY', 'steammods', self.steam.text.text())
        config.set('DIRECTORY', 'userdatamods', self.userdata.text.text())
        config.set('DIRECTORY', 'stagingareamods', self.stagingarea.text.text())

        t = QCheckBox()

        config.set("GRAPHICS", "modernstyle", str(self.modernstyle.data.isChecked()))
        config.set("GRAPHICS", "imagesize", self.imagesize.data.text())

        config.set("LANGUAGE", "language", self.language.data.text())
        config.set("LANGUAGE", "uiLanguage", self.UIlanguage.data.itemData(self.UIlanguage.data.currentIndex()))


        with open(f('settings.ini'), 'w') as configfile:
            config.write(configfile)

        # Quit App
        QCoreApplication.quit()
