import sys
from os.path import expanduser
from PyQt5.QtCore import QCoreApplication, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
)
import configparser

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

class PathEnty(QWidget):
    def __init__(self, buttontext: str, tooltip: str, opentitle: str) -> None:
        super().__init__()
        self.buttontext = buttontext
        self.btntooltip = tooltip
        self.opentitle = opentitle
        self.build_gui()

    def build_gui(self):
        self.h = QHBoxLayout()
        btn = QPushButton(self.buttontext)
        btn.setToolTip(self.btntooltip)
        btn.clicked.connect(self.setPath)
        self.label = QLineEdit()
        self.h.addWidget(self.label)
        self.h.addWidget(btn)
        self.setLayout(self.h)

    def setPath(self, *arg):
        fd = QFileDialog()
        f_dir = fd.getExistingDirectory(
            self,
            self.opentitle,
            expanduser("~"),
            fd.ShowDirsOnly
        )
        if f_dir != "":
            self.label.setText(f_dir)


class First(Install_Window):
    def __init__(self) -> None:
        super().__init__()
        self.fill_content()

    def fill_content(self):
        # Steam Mods
        self.steam = PathEnty(
            "Set Steam Mods",
            "Example: /steamapps/workshop/content/1066780",
            "Open Steam Mods Folder"
        )
        self.content.addWidget(self.steam)

        # Common Mods in settings.ini external
        self.common = PathEnty(
            "Set Common Mods",
            "Example: /steamapps/common/Transport Fever 2/mods",
            "open Common Mods Folder"
        )
        self.content.addWidget(self.common)

        # Userdata Mods
        self.userdata = PathEnty(
            "Set Userdata Mods",
            "Example: /userdata/436684792/1066780/local/mods",
            "open userdata Mods Folder"
        )
        self.content.addWidget(self.userdata)

        # Stagingarea Mods
        self.stagingarea = PathEnty(
            "Set Stagingarea",
            "Example: /userdata/436684792/1066780/local/staging_area",
            "open staging_area Folder"
        )
        self.content.addWidget(self.stagingarea)

        # 7-Zip installation
        if sys.platform == "win32":
            self.sevenzip = PathEnty(
                "Set 7-Zip Installation",
                r"Example: C:\Program Files\7-Zip",
                "open 7-zip installation folder"
            )
            self.content.addWidget(self.sevenzip)

        # Connect Signal
        sig.submit.connect(self.submit)

    def submit(self):
        config.add_section('DIRECTORY')
        config.set('DIRECTORY', 'externalmods', self.common.label.text())
        config.set('DIRECTORY', 'steammods', self.steam.label.text())
        config.set('DIRECTORY', 'userdatamods', self.userdata.label.text())
        config.set('DIRECTORY', 'stagingareamods', self.stagingarea.label.text())
        if sys.platform == "win32":
            config.set('DIRECTORY', '7-zipInstallation', self.sevenzip.label.text())
        elif sys.platform == "linux":
            config.set('DIRECTORY', '7-zipInstallation', "/usr")

        config.add_section("GRAPHICS")
        config.set("GRAPHICS", "modernstyle", "True")
        config.set("GRAPHICS", "imagesize", "384")

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

        sig.next_page.emit()

class Second(Install_Window):
    def __init__(self) -> None:
        super().__init__()
        self.build_gui()

    def build_gui(self):
        self.content.addWidget(QLabel("Setup succesfull click on Continue to close the app."))
        self.content.addWidget(
            QLabel("Restart the app afterwards"))

        sig.submit.connect(self.exit)

    def exit(self):
        QCoreApplication.quit()

class Stetup_Window(QMainWindow):
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
