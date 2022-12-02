# Transport-Fever-2-NeonModManager
A Mod-Manager for Transport Fever 2 written in Python.

:uk:
### What you can do with this Application:

List all installed Mods,
Search your installed Mods,
Open a Mod in Explorer,
Uninstall a Mod,
export modlists,
compare modlists with installed mods.
To run this application you need 7-Zip.



### Information for Modders:

If your Mod is not detected correct create a File called Mod.json in your Mod as in the Example:https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/blob/v1.3/example/mod.json

:de:
### Funktionen:

Auflisten aller installierten Mods,
Suche der installierten Mods,
Öffnen der Mod,
Deinstallieren der Mod,
Exportiere Modlisten,
vergleiche Modlisten mit installierten Mods.


Ihr benötigt 7-Zip um dieses Programm zu verwenden.



### Information für Modder:

Falls eure Mod nicht richtig erkannt wird könnt ihr dass beheben in dem ihr eine Mod.json anlegt wie in diesem Beispiel:

https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/blob/v1.3/example/mod.json und diesen in eure Mod packt.


## Installation

:uk:
### Windows

For installation under Windows download the Windows [release](https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/releases/latest) via Github. You also need to install 7-zip.

After that Extract the zip file and start main.exe. You will see entries in which you can type the path to the correct folders, or you can click on the button on the right of the entry for opening the directory. When you did this for all entries click on Continue. After that click on Continue. Restart the Program afterwards.

### Linux

#### Debian based Systems (Ubuntu, Mint, etc.) & Fedora Systems

Go to the last  [release](https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/releases/latest) and download the .rpm/.deb file. (depending on your os) 

Click on the file and hit install. You will be required to type in your Password. Start the Program. You will see entry in which you can type the path to the correct folder, or you click on the button on the right of the entry for opening the directory. When you did this for all entries click on Continue. After that click on Continue. Restart the Program afterwards.

### General Instructions
Install Python3.8 or newer and pip. You also need to install 7-zip. I recommend the package "p7zip".

Clone the repository. Open a Terminal and enter:

`git clone https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager.git'`

Navigate into the folder. Enter:

`cd Transport-Fever-2-NeonModManager`

Install all the dependencies. Enter:

`pip install -r requirements.txt` * You might need run pip3 instead; You might need to install PyQt5 via a separate package. *

Navigate into src. Enter:
`cd src`

Start the program. Enter:
`python3 main.py` * If you want make a .desktop file, so that you can start the Program from your menu system (General Instructions https://www.maketecheasier.com/create-desktop-file-linux/ (Please note that you made need to do something a little bit different)), change Line 44 in main.py to "if True:". *

:de:
### Windows

Für eine Installation auf Windows downloaden Sie den [release](https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/releases/latest) via Github. Sie benötigen des weiteren auch noch das Programm 7-zip.

Nach dem Herunterladem, extrahieren sie die .zip Datei, und starten sie "main.exe". Sie werden ein Eingabefeld sehen, in dem sie den Pfad zu dem jeweiligen Ordner angeben, alternativ können Sie den Ordner mit einem Klick auf den rechten Button auswählen. Wenn sie dies für alle Einträge getan haben dürcken sie auf Continue. Nocheinmal auf Continue drücken. Anschließend das Programm neu starten.

### Linux

#### Debian basierende Systeme (Ubuntu, Mint, etc.) & Fedora Systems

Gehen Sie auf den letzten [release](https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/releases/latest) und downloaden Sie die .rpm/.deb Datei. (Je nach Betriebsystem) 

Öffnen sie die Datei, und drücken sie installieren. Sie werden ihr Passwort eingeben müssen. Starten sie das Programm. Sie werden ein Eingabefeld sehen, in dem sie den Pfad zu dem jeweiligen Ordner angeben, alternativ können Sie den Ordner mit einem Klick auf den rechten Button auswählen. Wenn sie dies für alle Einträge getan haben dürcken sie auf Continue. Nocheinmal auf Continue drücken. Anschließend das Programm neu starten.

### General Instructions
Installieren Sie Python3.8 oder neuer und pip. Sie benötigen außerdem  7-zip. Ich empfehle ihnen das Paket: "p7zip".

Klonen sie das reposetory. Öffnen Sie eine Konsole und geben Sie ein:

`git clone https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager.git'`

Navigieren Sie in den Ordner. Geben Sie ein:

`cd Transport-Fever-2-NeonModManager`

Install all the dependencies. Geben Sie ein:

`pip install -r requirements.txt` * Evntl. müssen sie stattdessen "pip3" ausführen; Evntl. müssen sie "PyQt5" über ein Paket extra installieren *

Navigieren Sie in den Ordner "src". Geben Sie ein:
`cd src`

Starten sie das Programm. Geben Sie ein:
`python3 main.py` * Falls sie eine .desktop Datei hinzufügen wollen, sodass Sie dass Pragramm von dem Menü aus starten können, so ändern sie bitte Zeile 44 von main.py zu "if True:".*

